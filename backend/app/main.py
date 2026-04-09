from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .routes import auth, workspace, vacancies, candidates, resumes, links, analysis, invites

app = FastAPI(
    title="MockIT API",
    description="A recruiter tool for managing vacancies, candidates, and AI analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(workspace.router)
app.include_router(vacancies.router)
app.include_router(candidates.router)
app.include_router(resumes.router)
app.include_router(links.router)
app.include_router(analysis.router)
app.include_router(invites.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MockIT API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
