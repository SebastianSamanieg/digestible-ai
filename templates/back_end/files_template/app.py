'''
import asyncio
import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.routes import reset_utils, koralia_utils
from core.workers.worker_loop import worker_loop

# ═══════════════════════════════════════════════════════════════════════════════
# ↔️ API CONFIGURATION VARIABLES
# ═══════════════════════════════════════════════════════════════════════════════
APP_VERSION = "1.0.0"
APP_NAME = "Kori - IA: API"
START_TIME = time.time()
app = FastAPI(
    title="koral-ia",
    version="1.0.0"
)
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# ↔️ MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════════
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 ROT STATUS
# ═══════════════════════════════════════════════════════════════════════════════
@app.get("/", tags=["Health"], summary="Service Status")
async def root_status():
    """Endpoint principal que muestra el estado del servicio"""
    return JSONResponse(
        status_code=200,
        content={
            "service": APP_NAME,
            "status": "operational",
            "version": APP_VERSION,
            "message": "Kori - IA funcionando correctamente"
        }
    )
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def start_worker():
    asyncio.create_task(worker_loop())

# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 ROUTER'S
# ═══════════════════════════════════════════════════════════════════════════════
app.include_router(reset_utils.router, prefix="/api/v1/chat")
app.include_router(koralia_utils.router, prefix="/api/v1/tools")
# ═══════════════════════════════════════════════════════════════════════════════
'''