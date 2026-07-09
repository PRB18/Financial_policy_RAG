# Financial Policy RAG Agent — in progress.

## what it does?

- It uses RAG to anser questions related to Indian financial policy.
- RAG understands the context, compares the static DB and live search results and gives the output.
- Currently iam using ChromaDB to store the data in-memory.
- It uses pypdf to extrat the text and send it to ChromaDB to store.
- for now /query endpoint just takes the query from user.

## tech stack

- **LangGraph** — for building the agent graph
- **LangChain** — core message types and utilities
- **ChromaDB** — in-memory vector store
- **pypdf** — to read and extract text from PDFs
- **FastAPI + Uvicorn** — for the /query endpoint

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

- it consists of a state which stores the conversation history in the form of sequence of list of messages
- it had 3 node
- node1: retrieve data from the db
- node2 : searched the web live
- node3 : compares the static storage and the live search results
- the graph is compiled and run well until now

## Progress so far

- the agent retrieves and gives the output but live search and comparision is still not added
- the query is hardcoded for now, later will be connected with fastapi and the query will be taken from  the user
- llm will be added later 
- the result should be more accurate.
- used travily api to fetch live data.