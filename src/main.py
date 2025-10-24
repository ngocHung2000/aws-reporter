from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

from routers import ec2, rds
from utils.config import Config

app = FastAPI(
    title="AWS Reporter API",
    description="Cross-account AWS resource reporting API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ec2.router, prefix="/api/v1")
app.include_router(rds.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AWS Reporter API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)