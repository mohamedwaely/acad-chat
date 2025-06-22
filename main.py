from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy import text
from app import models
from app.db import engine
from app.routes import router

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    return {
        "message": "The Project is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

with engine.connect() as connection:
    connection.execute(text("CREATE INDEX IF NOT EXISTS projects_embedding_idx ON projects USING hnsw (embedding vector_cosine_ops)"))
    connection.commit()

app.include_router(router)

if __name__=="__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)