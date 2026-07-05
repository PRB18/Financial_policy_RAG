from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END

#this is the "state"
#it stores messages list and context
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "convorsation history"]


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


workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrirve_from_db)
workflow.add_node("live_search", live_search)
workflow.add_node("compare", comaprision)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "live_search")
workflow.add_edge("live_search", "compare")
workflow.add_edge("compare", END)

agent = workflow.compile()
print("Graph compiled successfully")

result = agent.invoke({
    "messages": [HumanMessage(content="What is the current repo rate?")]
})
print(result)
