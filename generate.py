#Generate a response from ollama based on a prompt
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

storage_context = StorageContext.from_defaults(persist_dir="index")
Settings.llm = Ollama(model="gemma:2b",request_timeout=300)
Settings.embed_model = HuggingFaceEmbedding()
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
def prompt(data:str):
    streaming_response = query_engine.query(data)
    for i in streaming_response.response_gen:
        print(i,end="")