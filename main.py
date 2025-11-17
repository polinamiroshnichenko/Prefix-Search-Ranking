from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from search_kernel.smart_search import smart_search

app = FastAPI(title="Prefix Search API")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.3

@app.get("/")
def root():
    return {"message": "Prefix Search API is running"}

@app.post("/search")
def search_endpoint(req: SearchRequest):
    if not req.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = smart_search(req.query, threshold=req.threshold)
    return {"query": req.query, "top_results": results[:req.top_k]}

