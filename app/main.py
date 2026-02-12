from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_graph

app = FastAPI()

graph = build_graph()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def handle_ticket(req: ChatRequest):
    result = graph.invoke({"userQuery": req.message})
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)