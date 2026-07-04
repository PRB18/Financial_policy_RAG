from fastapi import FastAPI, HTTPException , Path , status
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

class Request(BaseModel):
    query: str


@app.get("/")
def index():
    return{"messgae":"this is the home page"}

@app.post("/query")
def query(question: Request):
    return {"message": "this is where the query goes", "you_entered": question}
