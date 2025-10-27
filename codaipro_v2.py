"""
CodaiPro v2.1 - Enhanced Stability
Architecture: CustomTkinter (Frontend) + FastAPI (Backend)
Optimized for exam environment and offline use
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import re
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime
import pyperclip
import requests
import time

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Backend server config
BACKEND_URL = "http://127.0.0.1:8765"
backend_process = None

class CodeBlock(ctk.CTkFrame):
    """Custom widget for displaying code with copy button"""
    def __init__(self, parent, code, language="python"):
        super().__init__(parent, corner_radius=8, fg_color=("gray85", "gray20"))
        
        # Language label
        lang_frame = ctk.CTkFrame(self, fg_color=("gray75", "gray25"), corner_radius=0)
        lang_frame.pack(fill="x", padx=0, pady=0)
        
        lang_label = ctk.CTkLabel(
            lang_frame,
            text=f"📝 {language}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray20", "gray80")
        )
        lang_label.pack(side="left", padx=10, pady=3)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            lang_frame,
            text="📋 Copy",
            command=lambda: self.copy_code(code),
            width=70,
            height=24,
            font=ctk.CTkFont(size=10),
            fg_color=("blue", "blue"),
            hover_color=("darkblue", "darkblue")
        )
        copy_btn.pack(side="right", padx=5, pady=3)
        
        # Code display
        code_text = ctk.CTkTextbox(
            self,
            height=min(len(code.split('\n')) * 20, 400),
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
            fg_color=("gray90", "gray15")
        )
        code_text.pack(fill="both", expand=True, padx=2, pady=2)
        code_text.insert("1.0", code)
        code_text.configure(state="disabled")
    
    def copy_code(self, code):
        """Copy code to clipboard"""
        try:
            pyperclip.copy(code)
            messagebox.showinfo("Copied!", "Code copied to clipboard!")
        except:
            self.clipboard_clear()
            self.clipboard_append(code)
            messagebox.showinfo("Copied!", "Code copied to clipboard!")

class MessageBubble(ctk.CTkFrame):
    """Enhanced message bubble with better formatting"""
    def __init__(self, parent, role, text):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", padx=5, pady=5)
        
        # Different styling for roles
        if role == "user":
            bg_color = ("#3b82f6", "#2563eb")
            text_color = "white"
            anchor = "e"
            icon = "👤 You"
        elif role == "assistant":
            bg_color = ("gray70", "gray25")
            text_color = ("black", "white")
            anchor = "w"
            icon = "🤖 CodaiPro"
        else:  # system
            bg_color = ("#f59e0b", "#d97706")
            text_color = "white"
            anchor = "w"
            icon = "⚠️ System"
        
        # Main bubble
        bubble = ctk.CTkFrame(self, corner_radius=12, fg_color=bg_color)
        bubble.pack(anchor=anchor, padx=10, fill="x" if role == "assistant" else "none")
        
        # Header with icon and timestamp
        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(8, 4))
        
        icon_label = ctk.CTkLabel(
            header,
            text=icon,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=text_color
        )
        icon_label.pack(side="left")
        
        time_label = ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%H:%M"),
            font=ctk.CTkFont(size=9),
            text_color=text_color if role != "assistant" else ("gray40", "gray60")
        )
        time_label.pack(side="right")
        
        # Parse and display content
        self.render_content(bubble, text, text_color, role)
    
    def render_content(self, parent, text, text_color, role):
        """Render text with code block detection"""
        code_pattern = r'```(\w+)?\n(.*?)```'
        parts = re.split(code_pattern, text, flags=re.DOTALL)
        
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        
        i = 0
        while i < len(parts):
            if i % 3 == 0 and parts[i].strip():
                label = ctk.CTkLabel(
                    content_frame,
                    text=parts[i].strip(),
                    font=ctk.CTkFont(size=13),
                    text_color=text_color,
                    wraplength=600,
                    justify="left",
                    anchor="w"
                )
                label.pack(fill="x", pady=4)
            elif i % 3 == 2:
                language = parts[i-1] if parts[i-1] else "code"
                code = parts[i].strip()
                code_block = CodeBlock(content_frame, code, language)
                code_block.pack(fill="x", pady=6)
            i += 1

class SettingsPanel(ctk.CTkFrame):
    """Settings sidebar panel"""
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=10)
        self.app = app
        
        title = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Generation parameters
        self.create_section("Generation Settings")
        
        # Temperature
        temp_label = ctk.CTkLabel(self, text="🌡️ Temperature", font=ctk.CTkFont(size=11))
        temp_label.pack(padx=15, pady=(5, 0))
        
        self.temp_slider = ctk.CTkSlider(
            self,
            from_=0.0,
            to=1.0,
            number_of_steps=20,
            command=lambda v: self.temp_value.configure(text=f"{v:.2f}")
        )
        self.temp_slider.set(0.1)
        self.temp_slider.pack(padx=15, pady=2, fill="x")
        
        self.temp_value = ctk.CTkLabel(self, text="0.10", font=ctk.CTkFont(size=10))
        self.temp_value.pack()
        
        # Max tokens
        tokens_label = ctk.CTkLabel(self, text="📏 Max Length", font=ctk.CTkFont(size=11))
        tokens_label.pack(padx=15, pady=(10, 0))
        
        self.tokens_slider = ctk.CTkSlider(
            self,
            from_=100,
            to=3000,
            number_of_steps=58,
            command=lambda v: self.tokens_value.configure(text=f"{int(v)}")
        )
        self.tokens_slider.set(1200)
        self.tokens_slider.pack(padx=15, pady=2, fill="x")
        
        self.tokens_value = ctk.CTkLabel(self, text="1200", font=ctk.CTkFont(size=10))
        self.tokens_value.pack()
        
        # System prompt
        self.create_section("System Instructions")
        
        self.system_prompt = ctk.CTkTextbox(
            self,
            height=120,
            font=ctk.CTkFont(size=11),
            wrap="word"
        )
        self.system_prompt.pack(padx=15, pady=5, fill="x")
        self.system_prompt.insert("1.0", "You are an expert programming assistant. Provide accurate, efficient code. Be concise.")
        
        # Actions
        self.create_section("Actions")
        
        save_btn = ctk.CTkButton(
            self,
            text="💾 Save Chat",
            command=app.save_conversation,
            fg_color="green",
            hover_color="darkgreen"
        )
        save_btn.pack(padx=15, pady=5, fill="x")
        
        clear_btn = ctk.CTkButton(
            self,
            text="🗑️ Clear All",
            command=app.clear_chat,
            fg_color="red",
            hover_color="darkred"
        )
        clear_btn.pack(padx=15, pady=5, fill="x")
        
        # Stats
        self.create_section("Statistics")
        
        self.stats_label = ctk.CTkLabel(
            self,
            text="Messages: 0\nTokens: ~0",
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        self.stats_label.pack(padx=15, pady=5)
    
    def create_section(self, title):
        label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        label.pack(padx=15, pady=(15, 5), anchor="w")
    
    def update_stats(self, message_count, token_estimate):
        self.stats_label.configure(text=f"Messages: {message_count}\nTokens: ~{token_estimate:,}")

class CodaiProV2(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CodaiPro v2.1 - Enhanced Stability")
        self.geometry("1400x800")
        
        self.conversation_history = []
        self.is_generating = False
        self.total_tokens = 0
        self.backend_ready = False
        
        self.create_widgets()
        
        # Start backend server
        self.after(100, self.start_backend)
    
    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = SettingsPanel(self, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Main content
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(main_frame, height=70, corner_radius=10)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(
            header,
            text="🚀 CodaiPro v2.1",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.status_label = ctk.CTkLabel(
            header,
            text="⏳ Starting backend...",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        self.progress_bar = ctk.CTkProgressBar(header, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        self.progress_bar.start()
        
        # Chat display
        self.chat_frame = ctk.CTkScrollableFrame(
            main_frame,
            corner_radius=10,
            fg_color=("gray90", "gray13")
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Input area
        input_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_text = ctk.CTkTextbox(
            input_frame,
            height=100,
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.input_text.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_text.bind("<Control-Return>", lambda e: self.send_message())
        
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        self.send_button = ctk.CTkButton(
            button_frame,
            text="▶ Send",
            command=self.send_message,
            width=140,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.send_button.pack()
        
        self.add_welcome_message()
    
    def add_welcome_message(self):
        welcome = """👋 Welcome to CodaiPro v2.1!

**🆕 What's New:**
• FastAPI backend for better performance
• Optimized CPU inference
• Professional architecture
• Production-ready code

**💡 I can help you:**
• Write code (Python, JS, Java, C++, etc.)
• Explain complex algorithms
• Debug and fix errors
• Review and optimize code

Type your question below and let's code! 🚀"""
        
        MessageBubble(self.chat_frame, "assistant", welcome)
    
    def start_backend(self):
        """Start FastAPI backend server"""
        def start():
            global backend_process
            try:
                # Find backend script
                backend_script = Path(__file__).parent / "backend_server.py"
                
                if not backend_script.exists():
                    raise FileNotFoundError("backend_server.py not found!")
                
                # Start backend process
                backend_process = subprocess.Popen(
                    [sys.executable, str(backend_script)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                
                # Wait for backend to be ready
                max_retries = 30
                for i in range(max_retries):
                    try:
                        response = requests.get(f"{BACKEND_URL}/health", timeout=1)
                        if response.status_code == 200:
                            self.backend_ready = True
                            self.after(0, lambda: self.on_backend_ready())
                            return
                    except:
                        pass
                    time.sleep(1)
                
                raise TimeoutError("Backend failed to start in 30 seconds")
                
            except Exception as e:
                self.after(0, lambda: self.on_backend_error(str(e)))
        
        thread = threading.Thread(target=start, daemon=True)
        thread.start()
    
    def on_backend_ready(self):
        """Called when backend is ready"""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.status_label.configure(text="✅ Ready", text_color="green")
        self.send_button.configure(state="normal")
        MessageBubble(self.chat_frame, "system", "✅ Backend server ready! You can start chatting now.")
    
    def on_backend_error(self, error):
        """Called when backend fails"""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.status_label.configure(text="❌ Backend failed", text_color="red")
        MessageBubble(self.chat_frame, "system", f"ERROR: Backend failed to start!\n\n{error}\n\nPlease restart the application.")
    
    def send_message(self):
        """Send message to backend"""
        if self.is_generating or not self.backend_ready:
            return
        
        prompt = self.input_text.get("1.0", "end-1c").strip()
        if not prompt:
            return
        
        self.input_text.delete("1.0", "end")
        MessageBubble(self.chat_frame, "user", prompt)
        
        self.is_generating = True
        self.send_button.configure(state="disabled", text="⏳ Thinking...")
        self.status_label.configure(text="🤔 Generating...")
        
        def generate():
            try:
                # Get settings
                temperature = self.sidebar.temp_slider.get()
                max_tokens = int(self.sidebar.tokens_slider.get())
                system_prompt = self.sidebar.system_prompt.get("1.0", "end-1c").strip()
                
                # Call backend API
                response = requests.post(
                    f"{BACKEND_URL}/complete",
                    json={
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "system_prompt": system_prompt
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data["text"]
                    tokens = data["tokens_used"]
                    
                    self.total_tokens += tokens
                    
                    self.after(0, lambda: MessageBubble(self.chat_frame, "assistant", result))
                    
                    self.conversation_history.append({"role": "user", "content": prompt})
                    self.conversation_history.append({"role": "assistant", "content": result})
                    
                    self.after(0, lambda: self.sidebar.update_stats(
                        len(self.conversation_history),
                        self.total_tokens
                    ))
                else:
                    error_msg = f"Backend error: {response.status_code}"
                    self.after(0, lambda: MessageBubble(self.chat_frame, "system", error_msg))
                
            except Exception as e:
                self.after(0, lambda: MessageBubble(self.chat_frame, "system", f"Error: {str(e)}"))
            
            finally:
                self.is_generating = False
                self.after(0, lambda: self.send_button.configure(state="normal", text="▶ Send"))
                self.after(0, lambda: self.status_label.configure(text="✅ Ready"))
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
    
    def clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.conversation_history = []
        self.total_tokens = 0
        self.sidebar.update_stats(0, 0)
        self.add_welcome_message()
    
    def save_conversation(self):
        if not self.conversation_history:
            messagebox.showwarning("No Conversation", "Nothing to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "messages": self.conversation_history,
                        "total_tokens": self.total_tokens
                    }, f, indent=2)
                messagebox.showinfo("Success", "Saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {str(e)}")
    
    def on_closing(self):
        """Enhanced cleanup on exit - v2.1 complete shutdown"""
        try:
            print("CodaiPro v2.1 shutting down...")
            
            # Disable the close button immediately
            self.protocol("WM_DELETE_WINDOW", lambda: None)
            
            # Release single instance locks first
            try:
                import launcher
                launcher.release_single_instance()
                print("Released single instance locks")
            except Exception as e:
                print(f"Error releasing locks: {e}")
            
            # Stop backend process
            global backend_process
            if backend_process:
                try:
                    backend_process.terminate()
                    backend_process.wait(timeout=2)
                    print("Backend terminated")
                except:
                    try:
                        backend_process.kill()
                        print("Backend killed")
                    except:
                        pass
            
            # Destroy GUI
            try:
                self.destroy()
            except:
                pass
            
            try:
                self.quit()
            except:
                pass
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            # Enhanced exit strategy - multiple methods
            import os
            import sys
            print("Forcing complete exit...")
            
            # Method 1: os._exit (most reliable)
            try:
                os._exit(0)
            except:
                pass
            
            # Method 2: sys.exit (backup)
            try:
                sys.exit(0)
            except:
                pass
            
            # Method 3: Windows ExitProcess (last resort)
            try:
                import ctypes
                ctypes.windll.kernel32.ExitProcess(0)
            except:
                pass

def main():
    """Main entry point - single run, no loops"""
    try:
        app = CodaiProV2()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        import os
        os._exit(0)
    except Exception as e:
        print(f"Application error: {e}")
        import os
        os._exit(1)
    finally:
        # ENSURE we exit completely
        import os
        os._exit(0)

if __name__ == "__main__":
    main()
