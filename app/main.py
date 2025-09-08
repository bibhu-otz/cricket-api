from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.routers import players
from app.core.database import init_db

app = FastAPI(title="Cricket Players API", version="1.0.0")
origins = [
    "http://localhost:5500",
    "http://localhost:5173"
]
app.include_router(players.router, prefix="/api/players",
tags=["players"])

@asynccontextmanager
async def lifespan(app: FastAPI):
# Startup: Initialize the database
  init_db()
  yield
  # Shutdown: Cleanup if needed (e.g., close database pool)
  # No explicit cleanup needed for psycopg2 pool in this case
  app.lifespan = lifespan
  # Root endpoint to handle GET /
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
  return {"message": "Welcome to the Cricket Players API. Access/docs for API documentation."}
if __name__ == "__main__":
  uvicorn.run("app.main:app",host="localhost",port=8000,reload=True)