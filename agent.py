from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from chromaDB import collection
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq

load_dotenv("API.env")
#this is the "state"
#it stores messages list and context
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "convorsation history", operator.add]
    context : list[str]
    live_response : list[dict]
    comparision_result : str



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
    #the query text is the question from the user which is stored in the state object 'messages'
    response = client.search(query=state["messages"][-1].content)
    #the response from travily is returned to the state object 'live_response'
    #this is list of dictionaries
    return {"live_response" : response["results"]}

#this node comapres the static data from the db with the live data
def comaprision(state: AgentState):
    print("Comparing static and live data...")
    #using groq api key
    groq_api = os.getenv("GROQ_API")
    client = Groq(api_key=groq_api)
    #a clear prompt to the llm on what it should be doing
    prompt_text = f"""
    You are an expert Financial Policy RAG Agent.
    The user asked: "{state['messages'][-1].content}"

    [SOURCE 1: STATIC OFFICIAL DATABASE]
    {state['context']}

    [SOURCE 2: LIVE WEB SEARCH]
    {state['live_response']}

    INSTRUCTIONS:
    Do not just blindly match text. You must analyze the data from both sources using the following steps:
    1. Terminology Check: Identify if both sources are talking about the same underlying metric, even if they use different words (e.g., "GST" vs "Goods and Services Tax").
    2. Fact Extraction: What is the specific number, rate, or rule stated in Source 1? What is it in Source 2?
    3. Conflict Resolution: Do the facts agree? 
       - If yes, synthesize a clear answer.
       - If no (e.g., Source 1 says 6.50% and Source 2 says 5.25%), treat Source 2 as the updated reality. 
    4. Final Output: State the current correct answer clearly. If there was a conflict, explicitly explain that the official database was outdated and provide the updated live web figure.

    Provide your final, professional answer based on this logic. Do not output your internal thinking steps, just the final response for the user.
    """
    chat_compilation = client.chat.completions.create(
        messages=[
            { "role" : "user",
            "content": prompt_text
            },
        ],
        model="llama-3.3-70b-versatile",    
    )
    return {"comparision_result" : chat_compilation.choices[0].message.content}

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


#this block of code only executes if the python script is run directly
#if imported it wont run
if __name__ == "__main__":
    result = agent.invoke({
        "messages": [HumanMessage(content="What is the fiscal deficit target for FY 2026-27?")]
    })
    print(result["messages"][-1].content)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(result["context"])
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(result["live_response"])
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(result["comparision_result"])


