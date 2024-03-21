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
import os
from dotenv import load_dotenv
import json
from user_intent import classify,poll_category
import requests

load_dotenv()

llm_url = os.getenv("LLM_URL")
model = os.getenv("LLM")

Settings.llm = Ollama(model=model,request_timeout=300, base_url=llm_url)
Settings.embed_model = HuggingFaceEmbedding()

db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("plutosONE")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
)

# Query Data from the persisted index
query_engine = index.as_query_engine(streaming=True)
chat_engine = index.as_chat_engine(streaming=True)

schema = {
    "question":{
        "type":"string",
        "description":"User's question"
    },
    "relevent":{
        "type":"boolean",
        "description":"Check if user is talking abot voucher or polls"
    },
}

def intent_classification(text):
    payload = json.dumps({
        "model":f"{model}",
        "messages":[
            {
                "role":"system",
                "content":"You are a helpful AI assistant. User will say something, your task is to understand if user wants any offers or user want to play polls. if the user want offer you will return 'offer'. if user want to play polls you will return 'poll'. answer only in a single word always."
            },
            {
                "role":"user",
                "content":f"{text}"
            }
        ],
        "format":"json",
        "stream":False
    })

    res = chat_engine.chat(payload)
    return res

def get_poll_category(text):
    categories = ["sports",'entertainment','lifestyle']
    payload = json.dumps({
        "messages":[
            {
                "role":"system",
                "content":f"You are a helpful AI assistant. find best match for poll category the user want to play from this list:{categories}. answer in one word"
            },
            {
                "role":"user",
                "content":"give me lifestyle poll"
            },
            {
                "role":"assistant",
                "content":"lifestyle"
            },
            {
                "role":"user",
                "content":f"{text}"
            }
        ],
        "format":"json",
        "stream":False
    })
    try:
        res = chat_engine.chat(payload)
        print("llm cat extraction=======>",res)
        return res.response
    except Exception as e:
        print(e)
        return 'entertainment'
    
def prompt(data:str):
    #get user's intent (what he want to do)
    user_intent = classify(data)

    if user_intent == 'other':
        payload = json.dumps({
            "messages":[
                {
                    "role":"system",
                    "content":"You are a helpful AI assistant. When user asks any questions, you will answer from provided context info. Do not answer outside of provided context info"
                },
                {
                    "role":"user",
                    "content":f"{data}"
                }
            ]
        })
        query_engine.query(payload).print_response_stream()

    #User want to play polls
    elif user_intent == 'poll':
        #extract category
        # category = get_poll_category(data)
        # category=category.lower()
        # print("received category==============>",category)
        # #if category extraction is not successfull, defaulting to entertainment category
        # if category not in ["sports",'entertainment','lifestyle']:
        #     print('=========category defaulted=========')
        #     category = 'entertainment'
        category = poll_category(data)
        print("conditional category=======>",category)
        #api call to get polls of that category
        query_params = {}
        query_params["user_id"] = None
        response = requests.get(f"https://ems-be.plutos.one/api/v1/polls/5/previous/{category}", params=query_params, timeout=5)
        json_res = response.json()
        print(json_res.get('data')[1]['question'])
    #User want to browse offers
    else:
        payload = json.dumps({
            "messages":[
                {
                    "role":"system",
                    "content":f"You are a helpful AI assistant. User will ask you a question, assistant will return true if user is talking about a voucher. assistant will return true if user is talking about a poll, assistant will return false if user is not taking about poll or voucher. Output in JSON using the schema defined here: {schema}"
                },
                {
                    "role":"user",
                    "content":"show entertainment polls"
                },
                {
                    "role":"assistant",
                    "content":"{\"question\":\"show entertainment polls\",\"relevent\":\"True\"}"
                },
                {
                    "role":"user",
                    "content":f"{data}"
                }
            ],
            "format":"json",
            "stream":True
        })
        
        # streaming_response = query_engine.query(payload)
        # streaming_response.print_response_stream()
        res = chat_engine.chat(payload)
        print(res)