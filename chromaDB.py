from pdfread import pages_id
from pdfread import pages_list
import chromadb
#setting up the client
chroma_client = chromadb.Client()

#create or get the collection
#is is like an sheet inside excel
collection = chroma_client.get_or_create_collection(name="sample_data")

#insert of add data
collection.upsert(
    ids=pages_id,
    documents= pages_list
)

