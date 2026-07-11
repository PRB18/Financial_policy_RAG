from langchain_core.messages import HumanMessage
from fastapi import FastAPI, HTTPException , Path , status
from typing import Optional
from pydantic import BaseModel
from agent import agent


app=FastAPI()

class Request(BaseModel):
    query: str


@app.get("/")
def index():
    return{"messgae":"this is the home page"}

@app.post("/query")
def query(question: Request):
    #the question entered by the user is sent to the graph to process
    result = agent.invoke({"messages":[HumanMessage(content=question.query)]})
    #the final answer is extracted from the graph and returned to the user
    return {"answer": result["comparision_result"]}
    
