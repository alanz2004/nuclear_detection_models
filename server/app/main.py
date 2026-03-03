from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import models

app = FastAPI(title="ML Model Info API", version="1.0")

# CORS configuration
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(models.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the ML Model Info API. Use /models to list or get info."
    }