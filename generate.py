#Generate a response from ollama based on a prompt (index is taken from local storage)
# from llama_index.core import Settings
# from llama_index.llms.ollama import Ollama
# from llama_index.core import StorageContext, load_index_from_storage
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# storage_context = StorageContext.from_defaults(persist_dir="index")
# Settings.llm = Ollama(model="phi",request_timeout=300)
# Settings.embed_model = HuggingFaceEmbedding()
# index = load_index_from_storage(storage_context)
# query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
# def prompt(data:str):
#     streaming_response = query_engine.query(data)
#     for i in streaming_response.response_gen:
#         print(i,end="")



#Generate a response from ollama based on a prompt (index is taken from chroma vector index)
import chromadb
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex,Settings
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(model="llama2",request_timeout=300, base_url="https://45ec-34-125-114-25.ngrok-free.app")
Settings.embed_model = HuggingFaceEmbedding()

db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("paulgragm")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
)

# Query Data from the persisted index
query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)

def prompt(data:str):
    streaming_response = query_engine.query(data)
    for i in streaming_response.response_gen:
        print(i,end="")