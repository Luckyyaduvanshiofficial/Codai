"""
CodaiPro - FastAPI Backend Server
Optimized for exam environment and offline use
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn
import os
import threading
from pathlib import Path
from typing import Optional, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance (lazy loaded)
model = None
model_path: Optional[str] = None
model_lock = threading.Lock()

DEFAULT_SYSTEM_PROMPT = "You are an expert programming assistant. Provide accurate, efficient code with clear explanations."


def pre_warm_model():
    """Pre-warm model in background on startup"""
    try:
        logger.info("Pre-warming model in background...")
        get_model()
        logger.info("Model pre-warmed!")
    except Exception as e:
        logger.error(f"Failed to pre-warm model: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load model in background on startup (replaces deprecated on_event)"""
    threading.Thread(target=pre_warm_model, daemon=True).start()
    yield

app = FastAPI(title="CodaiPro Backend", version="2.1", lifespan=lifespan)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # "*" origins are incompatible with credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 1200
    temperature: float = 0.1
    top_p: float = 0.95
    stop: Optional[List[str]] = None
    system_prompt: Optional[str] = None

class CompletionResponse(BaseModel):
    text: str
    tokens_used: int
    model_name: str

def find_model() -> Optional[str]:
    """Find best available .gguf model in the models/ folder"""
    models_dir = Path(__file__).parent / "models"

    gguf_files = sorted(models_dir.glob("*.gguf")) if models_dir.exists() else []
    if not gguf_files:
        return None

    # Preference by model family (case-insensitive substring match, so any
    # quantization/filename variant of a recommended model still ranks first)
    preferred_families = [
        "phi-3.5",
        "qwen2.5-coder-7b",
        "qwen2.5-coder-3b",
        "deepseek-coder",
    ]

    for family in preferred_families:
        for path in gguf_files:
            if family in path.name.lower():
                return str(path)

    # Fallback: first .gguf found
    return str(gguf_files[0])

def get_model() -> Llama:
    """Get or initialize model (lazy loading with thread safety)"""
    global model, model_path

    if model is not None:
        return model

    with model_lock:
        # Double-check after acquiring lock
        if model is not None:
            return model

        path = find_model()
        if not path:
            raise RuntimeError("No .gguf model found in models/ folder")

        logger.info(f"Loading model: {path}")

        # OPTIMIZED SETTINGS per recommendations
        # CODAIPRO_GPU_LAYERS: set > 0 to offload layers to GPU when the
        # CUDA build of llama-cpp-python is installed (see INSTALL_GPU_SUPPORT.bat)
        model = Llama(
            model_path=path,
            n_ctx=4096,  # Larger context window
            n_threads=max(1, os.cpu_count() - 1),  # Use all but one core
            n_batch=512,  # Optimized batch size
            n_gpu_layers=int(os.environ.get("CODAIPRO_GPU_LAYERS", "0")),  # 0 = CPU only
            use_mmap=True,  # Memory-mapped files (faster loading)
            use_mlock=True,  # Keep model in RAM (faster inference)
            verbose=False,
            logits_all=False,  # Only last token (faster)
        )

        model_path = path
        logger.info("Model loaded successfully!")
        return model

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "model_loaded": model is not None,
        "version": "2.1"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    path = model_path or find_model()
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": path,
        "cpu_count": os.cpu_count()
    }

@app.post("/complete", response_model=CompletionResponse)
async def complete_code(request: CompletionRequest):
    """
    Generate code completion

    Optimized for:
    - Fast inference on CPU
    - Low latency
    - Accurate code generation
    """
    try:
        llm = get_model()

        system_prompt = request.system_prompt or DEFAULT_SYSTEM_PROMPT

        # create_chat_completion applies the chat template embedded in the
        # GGUF metadata, so Phi-3.5, Qwen and DeepSeek models all get their
        # correct prompt format (a single hardcoded template broke 2 of 3).
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.prompt},
        ]

        # Generate with optimized parameters (stop=None lets the model's EOS
        # token terminate generation naturally)
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=50,
            repeat_penalty=1.15,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            stop=request.stop,
            stream=False,
        )

        result_text = response['choices'][0]['message']['content'].strip()
        tokens_used = response['usage']['total_tokens']

        return CompletionResponse(
            text=result_text,
            tokens_used=tokens_used,
            model_name=Path(model_path).name if model_path else "unknown"
        )

    except Exception as e:
        logger.error(f"Completion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: CompletionRequest):
    """
    Chat endpoint (alias for complete)
    Kept for compatibility
    """
    return await complete_code(request)

def start_server(host: str = "127.0.0.1", port: int = 8765):
    """Start the FastAPI server"""
    logger.info(f"Starting CodaiPro Backend on {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=False  # Reduce noise
    )

if __name__ == "__main__":
    start_server()
