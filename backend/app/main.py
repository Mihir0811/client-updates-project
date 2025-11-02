from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .core.config import settings
from .core.database import create_tables
from .routes import auth_routes, task_routes, format_routes

# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    description="Backend API for Client Updates Automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix=settings.api_v1_str)
app.include_router(task_routes.router, prefix=settings.api_v1_str)
app.include_router(format_routes.router, prefix=settings.api_v1_str)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Client Updates Backend API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_tables()
    print("🚀 Client Updates Backend started successfully!")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔧 Environment: {'Development' if settings.debug else 'Production'}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Client Updates Backend shutting down...")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )