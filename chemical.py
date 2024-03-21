import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

llm_url = os.getenv("LLM_URL")
model = os.getenv("LLM")

# country = sys.argv[1]

schema = {
    "name":{
        "type":"string",
        "description":"Name of Element"
    },
    "notation":{
        "type":"string",
        "description":"Notation of element in periodc table"
    },
    "atomic_number":{
        "type":"integer",
        "description":"Atomic number of element in periodic table"
    }
}

payload = {
    "model":f"{model}",
    "messages":[
        {
            "role":"system",
            "content":f"You are a helpful AI assistant. if and only if the user enters name of a chemical element, you will return the notation of entered element in the periodic table and atomic number of entered element and the output must be in JSON using the schema defined here: {schema}. if user enteres anything else, answer normally"
        },
        {
            "role":"user",
            "content":"carbon"
        },
        {
            "role":"assistant",
            "content":"{\"name\":\"Carbon\",\"notation\":\"C\",\"atomic_number\":\"4\"}"
        },
        {
            "role":"user",
            "content":"wood"
        }
    ],
    "format":"json",
    "stream":False
}
response = requests.post(f"{llm_url}/api/chat",json=payload)

cityInfo = json.loads(response.json()['message']['content'])

print(cityInfo)