from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END

#this is the "state"
#it stores messages list and context
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "conversation history"]


#this is a "node"
#this node retrieves from the db
#takes "state" from AgentSate as an input parameter and return the updated state
def retrirve_from_db(state: AgentState):
    print("retrieving from the chromaDB....")
    return {"messages": state["messages"]}

#this node fetches the live data from the internet
def live_search(state: AgentState):
    print("Searching the web...")
    return {"messages": state["messages"]}

#this node comapres the static data from the db with the live data
def comaprision(state: AgentState):
    print("Comparing static and live data...")
    return {"messages": state["messages"]}


