from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api_router

app = FastAPI()
app.title = "TruCtrl"
app.version = "0.1.0"

# Allow Vite/Vue dev server and production origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://127.0.0.1:5173", 
        "http://127.0.0.1:5174",
        "https://*.digitaloceanspaces.com",
        "https://*.ondigitalocean.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TruCtrl API"}

app.include_router(api_router)