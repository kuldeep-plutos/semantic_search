#This code creates a index from files (in data folder) and saves it (in index folder). This index can be directly used by llama index for REG
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Settings.embed_model = HuggingFaceEmbedding()
# documents = SimpleDirectoryReader('data').load_data(show_progress=True)

# print(f"{'*'*50}Vectorization Started")
# index = VectorStoreIndex.from_documents(documents)
# print(f"{'*'*50}Vectorization Done")

# index.storage_context.persist(persist_dir="index")



#The following code converts data into vector and stores it in cromadb (vector database)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

# create client and a new collection
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("plutosONE")

#Define embedding
Settings.embed_model = HuggingFaceEmbedding()

#Load Documents
documents = SimpleDirectoryReader('data').load_data(show_progress=True)

# set up ChromaVectorStore and load in data
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
print(f"{'*'*50}Vectorization Started")
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
print(f"{'*'*50}Vectorization Done")