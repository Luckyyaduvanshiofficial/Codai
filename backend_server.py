"""
CodaiPro - FastAPI Backend Server
Optimized for exam environment and offline use
"""

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

app = FastAPI(title="CodaiPro Backend", version="2.0")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance (lazy loaded)
model = None
model_lock = threading.Lock()

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
    """Find first available .gguf model"""
    models_dir = Path(__file__).parent / "models"
    
    # Priority order: Phi-3.5 > DeepSeek > Qwen > others
    priority_models = [
        "Phi-3.5-mini-instruct-q4.gguf",
        "phi-3.5-mini-instruct-q4_k_m.gguf",
        "deepseek-coder-6.7b-instruct.Q4_K_M.gguf",
        "qwen2.5-coder-3b-instruct-q4_k_m.gguf",
    ]
    
    # Check priority models first
    for model_name in priority_models:
        model_path = models_dir / model_name
        if model_path.exists():
            return str(model_path)
    
    # Fallback: any .gguf file
    models = list(models_dir.glob("*.gguf"))
    return str(models[0]) if models else None

def get_model() -> Llama:
    """Get or initialize model (lazy loading with thread safety)"""
    global model
    
    if model is not None:
        return model
    
    with model_lock:
        # Double-check after acquiring lock
        if model is not None:
            return model
        
        model_path = find_model()
        if not model_path:
            raise RuntimeError("No .gguf model found in models/ folder")
        
        logger.info(f"Loading model: {model_path}")
        
        # OPTIMIZED SETTINGS per recommendations
        model = Llama(
            model_path=model_path,
            n_ctx=4096,  # Larger context window
            n_threads=max(1, os.cpu_count() - 1),  # Use all but one core
            n_batch=512,  # Optimized batch size
            n_gpu_layers=0,  # CPU only (exam environment)
            use_mmap=True,  # Memory-mapped files (faster loading)
            use_mlock=True,  # Keep model in RAM (faster inference)
            verbose=False,
            f16_kv=True,  # Use fp16 for key/value cache
            logits_all=False,  # Only last token (faster)
        )
        
        logger.info("Model loaded successfully!")
        return model

def pre_warm_model():
    """Pre-warm model in background on startup"""
    try:
        logger.info("Pre-warming model in background...")
        get_model()
        logger.info("Model pre-warmed!")
    except Exception as e:
        logger.error(f"Failed to pre-warm model: {e}")

@app.on_event("startup")
async def startup_event():
    """Pre-load model on startup"""
    threading.Thread(target=pre_warm_model, daemon=True).start()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "model_loaded": model is not None,
        "version": "2.0"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    model_path = find_model()
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": model_path,
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
        
        # Build prompt with system context
        system_prompt = request.system_prompt or "You are an expert programming assistant. Provide accurate, efficient code with clear explanations."
        
        full_prompt = f"""<|system|>
{system_prompt}</s>
<|user|>
{request.prompt}</s>
<|assistant|>
"""
        
        # Default stop sequences
        stop_sequences = request.stop or [
            "</s>", 
            "<|user|>", 
            "<|system|>",
            "User:",
            "Human:",
            "\n\n\n\n"
        ]
        
        # Generate with optimized parameters
        response = llm(
            full_prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=50,
            repeat_penalty=1.15,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            stop=stop_sequences,
            echo=False,
            stream=False
        )
        
        result_text = response['choices'][0]['text'].strip()
        tokens_used = response['usage']['total_tokens']
        
        return CompletionResponse(
            text=result_text,
            tokens_used=tokens_used,
            model_name=Path(find_model()).name
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
