
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agents.claimwise_graph import ask_claimwise

app = FastAPI(
    title="ClaimWise API",
    description=(
        "GenAI-powered insurance claims and "
        "policy intelligence assistant."
    ),
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question about an insurance claim or policy",
    )


class QuestionResponse(BaseModel):
    question: str
    route: str
    answer: str
    sources: list[dict] = Field(default_factory=list)


@app.get("/")
def home():
    return {
        "message": "Welcome to the ClaimWise API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "ClaimWise",
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        result = ask_claimwise(request.question)

        return QuestionResponse(
            question=result["question"],
            route=result["route"],
            answer=result["answer"],
            sources=result.get("sources", []),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        # Keep internal exception details out of the API response.
        print(f"ClaimWise API error: {error}")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the question.",
        ) from error
