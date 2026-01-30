"""
FastAPI Main Application
Gen Counselling AI for Good - Genetic Risk Assessment Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict, ocr, diseases

# Initialize FastAPI app
app = FastAPI(
    title="Genetic Risk Coach API",
    description="AI-powered genetic risk assessment and health coaching platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==========================================
# CORS Configuration
# ==========================================
# Allow frontend to make requests from different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:3000",  # Alternative React dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://gen-counselling-ai-for-good.onrender.com",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ==========================================
# Include Routers
# ==========================================
app.include_router(predict.router, prefix="/api")
app.include_router(ocr.router, prefix="/api")
app.include_router(diseases.router, prefix="/api")

# ==========================================
# Health Check Endpoint
# ==========================================
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "healthy",
        "service": "Genetic Risk Coach API",
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Genetic Risk Coach API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# ==========================================
# Application Startup Event
# ==========================================
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print("🚀 Genetic Risk Coach API starting up...")
    print("📚 API documentation available at: http://localhost:8000/docs")
    print("❤️  Health check available at: http://localhost:8000/health")

# ==========================================
# Application Shutdown Event
# ==========================================
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    print("👋 Genetic Risk Coach API shutting down...")

# ==========================================
# Run Instructions
# ==========================================
# Development:
#   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
#
# Production:
#   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
#
# With custom port:
#   uvicorn app.main:app --reload --port 8080
