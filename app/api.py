import os
import sys

# Add app folder to Python path
APP_DIR = os.path.dirname(os.path.abspath(__file__))

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from hybrid_coordinator import HybridCoordinator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="ARES-RAG X API",
    description="Enterprise RAG + SQL Hybrid AI API",
    version="1.0.0"
)


# Allow the frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Question to ask ARES-RAG X"
    )


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "ARES-RAG X API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ARES-RAG X API"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        coordinator = HybridCoordinator()

        answer = coordinator.process_query(question)

        return {
            "status": "success",
            "question": question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )