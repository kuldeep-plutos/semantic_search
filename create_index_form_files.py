#This code creates a index from files (in data folder) and saves it (in index folder). This index can be directly used by llama index for REG
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding()
documents = SimpleDirectoryReader('data').load_data(show_progress=True)

print(f"{'*'*50}Vectorization Started")
index = VectorStoreIndex.from_documents(documents)
print(f"{'*'*50}Vectorization Done")

index.storage_context.persist(persist_dir="index")