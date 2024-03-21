import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

llm_url = os.getenv("LLM_URL")
model = os.getenv("LLM")

def multiply(a:int,b:int)->int:
    """This function multiplies two numbers and returns the result"""
    return a * b

schema = {
    "a":{
        "type":"integer",
        "description":"First number eneterd by user"
    },
    "b":{
        "type":"integer",
        "description":"second number entered by the user"
    },
    "result":{
        "type":"integer",
        "description":"result when the two numbers entered by the user are multiplied"
    }
}

payload = {
    "model":f"{model}",
    "messages":[
        {
            "role":"system",
            "content":f"You are a helpful AI assistant. When the user asks to multiply two numbers, you are goint to extract the two numbers and pass them in this pyhton function: {multiply} and return the result . output in JSON using the schema defined here: {schema}"
        },
        {
            "role":"user",
            "content":"what is 3*999?"
        },
        {
            "role":"assistant",
            "content":"{\"a\":\"3\",\"b\":\"999\",\"result\":\"2997\"}"
        },
        {
            "role":"user",
            "content":f"what is 8 * 95?"
        }
    ],
    "stream":False
}
response = requests.post(f"{llm_url}/api/chat",json=payload)

ans = response.json()['message']['content']

print(ans)