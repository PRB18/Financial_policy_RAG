from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from chromaDB import collection
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv("travily.env")
#this is the "state"
#it stores messages list and context
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "convorsation history", operator.add]
    context : list[str]
    live_response : list[dict]



#this is a "node"
#this node retrieves from the db
#takes "state" from AgentSate as an input parameter and return the updated state
def retrirve_from_db(state: AgentState):
    print("retrieving from the chromaDB....")
    #imported the chromadb with collections(at line 5) and the query text is the question from the user
    #this triggers the chromadb to fetch the similar data from the db
    """ChromaDB uses embeddings — it converts your question into a 
    vector (list of numbers representing meaning) and finds the chunks in your 
    knowledge base whose vectors are closest to it mathematically."""
    #for now the state isnt being updated.
    context = collection.query(
        query_texts = [state["messages"][-1].content],
        n_results = 2
    )
    #print("results:",context["documents"])
    #updates the state by adding the context["documents"] to the messages list
    #since we used 'operator.add' in the state definition , it will add the new message to the existing list of messages

    return {"context": context["documents"][0]}


#this node fetches the live data from the internet
def live_search(state: AgentState):
    print("Searching the web...")
    web_search_api = os.getenv("LIVE_SEARCH_API")
    client = TavilyClient(web_search_api)
    response = client.search(query=state["messages"][-1].content)
    return {"live_response" : response["results"]}

#this node comapres the static data from the db with the live data
def comaprision(state: AgentState):
    print("Comparing static and live data...")
    return {}


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
