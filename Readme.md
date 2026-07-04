# Financial Policy RAG Agent — in progress.

## what it does?

- It uses RAG to anser questions related to Indian financial policy.
- RAG understands the context, compares the static DB and live search results and gives the output.
- Currently iam using ChromaDB to store the data in-memory.
- It uses pypdf to extrat the text and send it to ChromaDB to store.
- for now /query endpoint just takes the query from user.

## How to run?

1. create the virtual environment
2. activate the virtual environment
3. Clone the repo
4. `pip install -r requirements.txt`
4. `python chromaDB.py` 


