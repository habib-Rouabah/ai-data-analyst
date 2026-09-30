from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.pipeline import answer_question

app = FastAPI(title="AI Data Analyst")
app.mount("/static", StaticFiles(directory="static"), name="static")


class Question(BaseModel):
    question: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/ask")
def ask(payload: Question):
    return answer_question(payload.question)
