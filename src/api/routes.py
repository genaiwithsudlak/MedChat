# src/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from ..llm.rag_chain import answer_query
from ..utils.logger import logger

router = APIRouter()

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: Optional[int] = Field(3, ge=1, le=10)
    temperature: Optional[float] = Field(0.0, ge=0.0, le=1.0)

@router.post("/query")
async def query_endpoint(payload: QueryRequest):
    try:
        res = answer_query(payload.query, top_k=payload.top_k, temperature=payload.temperature)
        return res
    except Exception as exc:
        logger.exception("Error answering query: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
