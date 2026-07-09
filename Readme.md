# Financial Policy RAG Agent — in progress.

## what it does?

- It uses RAG to answer questions related to Indian financial policy.
- RAG understands the context, compares the static DB and live search results and gives the output.
- Currently using ChromaDB to store the data in-memory.
- It uses pypdf to extract the text and send it to ChromaDB to store.
- for now /query endpoint just takes the query from user.

## tech stack

- **LangGraph** — for building the agent graph
- **LangChain** — core message types and utilities
- **ChromaDB** — in-memory vector store
- **pypdf** — to read and extract text from PDFs
- **FastAPI + Uvicorn** — for the /query endpoint
- **Tavily** — for live web search
- **python-dotenv** — for loading API keys from .env file

## project structure

| file | what it does |
|---|---|
| `agent.py` | defines the langgraph agent — nodes, edges, state |
| `chromaDB.py` | sets up chromadb client and upserts the pdf data |
| `pdfread.py` | reads the pdf and extracts pages as a list |
| `query.py` | fastapi app with the /query endpoint |
| `requirements.txt` | all the dependencies |
| `financial_knowledge_base.pdf` | the main pdf being chunked and stored |

## How to run?

1. Clone the repo
2. create the virtual environment
3. activate the virtual environment
4. `pip install -r requirements.txt`
5. `python chromaDB.py` 
6. `python agent.py`

## example usage

invoke the agent directly:

```python
result = agent.invoke({
    "messages": [HumanMessage(content="What is the current repo rate?")]
})
```

hit the /query endpoint (once fastapi is running with `uvicorn query:app`):

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the current repo rate?"}'
```

## What the agent does?

- it consists of a state with 3 fields: `messages` (conversation history), `context` (ChromaDB results), and `live_response` (Tavily results)
- it has 3 nodes
- node1: retrieves data from ChromaDB
- node2: searches the web live using Tavily
- node3: compares the static storage and the live search results
- the graph is compiled and all 3 nodes run successfully

## Progress so far

- all 3 nodes are working — ChromaDB retrieval and Tavily live search are both returning results
- the compare node is still empty — comparison logic and LLM not added yet
- the query is hardcoded for now, later will be connected with FastAPI
- LLM will be added to the compare node to generate a final answer