import sys
import os
import time
import threading
import tempfile
import atexit
import signal
import ctypes
import socket

# Enhanced single-instance protection for CodaiPro v2.1
# Multiple layers: Named Mutex + Process Check + Port Lock
_mutex = None
_mutex_name = "Local\\CodaiPro_v21_SingleInstance"
LOCK_FILE = None
PORT_LOCK_FILE = None


def _is_port_in_use(port):
    """Check if a port is already in use."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            return result == 0
    except Exception:
        return False


def acquire_single_instance():
    """Enhanced single-instance protection with multiple checks.
    
    Returns True if this process acquired the lock, False otherwise.
    """
    global _mutex, LOCK_FILE, PORT_LOCK_FILE
    
    # Layer 1: Check if port 8000 is already in use
    if _is_port_in_use(8000):
        print("=" * 60)
        print("  CodaiPro v2.1 is already running!")
        print("  (Backend server port 8000 is in use)")
        print("=" * 60)
        print("\nPlease close the existing instance first.")
        input("\nPress Enter to exit...")
        return False
    # Try using a named mutex (Windows)
    try:
        kernel32 = ctypes.windll.kernel32
        
        # Try to open existing mutex first
        MUTEX_ALL_ACCESS = 0x1F0001
        existing_mutex = kernel32.OpenMutexW(MUTEX_ALL_ACCESS, False, _mutex_name)
        
        if existing_mutex:
            # Mutex already exists - another instance is running
            kernel32.CloseHandle(existing_mutex)
            print("=" * 60)
            print("  CodaiPro v2.1 is already running!")
            print("  (Found existing mutex)")
            print("=" * 60)
            print("\nPlease close the existing instance first.")
            input("\nPress Enter to exit...")
            return False
        
        # No existing mutex - create a new one
        mutex = kernel32.CreateMutexW(None, True, _mutex_name)  # bInitialOwner=True
        last_error = ctypes.GetLastError()
        
        print(f"[DEBUG] CreateMutexW returned: {mutex}, LastError: {last_error}")
        
        if not mutex:
            # Failed to create mutex for some reason, fallback to lockfile
            print("[DEBUG] Mutex creation failed, falling back to lockfile")
            raise OSError("CreateMutexW returned NULL")

        # Even if we created it, check if it existed before (ERROR_ALREADY_EXISTS)
        ERROR_ALREADY_EXISTS = 183
        if last_error == ERROR_ALREADY_EXISTS:
            print("=" * 60)
            print("  CodaiPro v2.1 is already running!")
            print("  (Mutex race condition detected)")
            print("=" * 60)
            print("\nPlease close the existing instance first.")
            # Close the handle before exiting
            kernel32.ReleaseMutex(mutex)
            kernel32.CloseHandle(mutex)
            input("\nPress Enter to exit...")
            return False

        _mutex = mutex
        
        # Layer 2: Create process lockfile
        lock_path = os.path.join(tempfile.gettempdir(), "codaipro_v21.lock")
        try:
            with open(lock_path, 'w') as f:
                f.write(f"{os.getpid()}\n{time.time()}")
            LOCK_FILE = lock_path
        except Exception as e:
            print(f"Warning: Could not create lockfile: {e}")
            
        # Layer 3: Create port lockfile
        port_lock_path = os.path.join(tempfile.gettempdir(), "codaipro_v21_port8000.lock")
        try:
            with open(port_lock_path, 'w') as f:
                f.write(f"8000\n{os.getpid()}\n{time.time()}")
            PORT_LOCK_FILE = port_lock_path
        except Exception as e:
            print(f"Warning: Could not create port lockfile: {e}")

        # Register cleanup handlers
        atexit.register(release_single_instance)
        signal.signal(signal.SIGINT, _signal_handler)
        try:
            signal.signal(signal.SIGTERM, _signal_handler)
        except Exception:
            # Some Windows Python builds may not support SIGTERM
            pass

        return True
    except Exception as e:
        # If anything goes wrong with mutex, fallback to lockfile approach
        print(f"[DEBUG] Mutex exception: {e}, falling back to lockfile")
        return _acquire_lockfile()


def _acquire_lockfile():
    """Fallback lockfile-based single instance (less robust)."""
    global LOCK_FILE
    lock_path = os.path.join(tempfile.gettempdir(), "codaipro_v2.lock")
    if os.path.exists(lock_path):
        try:
            with open(lock_path, 'r') as f:
                pid = int(f.read().strip())
            # Check if process exists
            kernel32 = ctypes.windll.kernel32
            SYNCHRONIZE = 0x00100000
            process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
            if process != 0:
                kernel32.CloseHandle(process)
                print("=" * 50)
                print("  CodaiPro is already running!")
                print("=" * 50)
                print("\nPlease close the existing instance first.")
                input("\nPress Enter to exit...")
                return False
        except Exception:
            try:
                os.remove(lock_path)
            except Exception:
                pass

    try:
        with open(lock_path, 'w') as f:
            f.write(str(os.getpid()))
        LOCK_FILE = lock_path
        atexit.register(release_single_instance)
        return True
    except Exception as e:
        print(f"Warning: Could not create lock file: {e}")
        return True

    
def _signal_handler(signum, frame):
    """Ensure cleanup on signals."""
    release_single_instance()
    sys.exit(0)


def release_single_instance():
    """Release mutex and all lockfiles if held."""
    global _mutex, LOCK_FILE, PORT_LOCK_FILE
    try:
        if LOCK_FILE and os.path.exists(LOCK_FILE):
            try:
                os.remove(LOCK_FILE)
            except Exception:
                pass
            LOCK_FILE = None
    except Exception:
        pass
        
    try:
        if PORT_LOCK_FILE and os.path.exists(PORT_LOCK_FILE):
            try:
                os.remove(PORT_LOCK_FILE)
            except Exception:
                pass
            PORT_LOCK_FILE = None
    except Exception:
        pass

    try:
        if _mutex:
            kernel32 = ctypes.windll.kernel32
            kernel32.ReleaseMutex(_mutex)
            kernel32.CloseHandle(_mutex)
            _mutex = None
    except Exception:
        pass


def start_backend():
    """Start backend server in background thread and return the thread object."""
    try:
        import backend_server
        print("Starting backend server...")
        t = threading.Thread(target=backend_server.start_server, daemon=True)
        t.start()
        time.sleep(3)  # Wait a moment for backend to initialize
        print("Backend server started!")
        return t
    except Exception as e:
        print(f"Backend error: {e}")
        print("Continuing without backend...")
        return None

def main():
    """Main entry point"""
    print("=" * 60)
    print("  CodaiPro v2.1 - Enhanced Single Instance")
    print("=" * 60)
    print()

    # Acquire single-instance lock (mutex + lockfile fallback)
    if not acquire_single_instance():
        return

    # Start backend thread (returns thread or None)
    backend_thread = start_backend()

    # Run frontend
    try:
        import codaipro_v2
        print("Starting frontend GUI...")
        codaipro_v2.main()
    except Exception as e:
        print(f"Frontend error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
    finally:
        # Ensure single-instance resources are cleaned up
        release_single_instance()

if __name__ == "__main__":
    main()
