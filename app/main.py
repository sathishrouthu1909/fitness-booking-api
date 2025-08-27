from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, classes, bookings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Studio Booking API",
    description="A comprehensive API for booking fitness classes with JWT authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(classes.router)
app.include_router(bookings.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Fitness Studio Booking API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2025-08-26"}