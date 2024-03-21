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
    "city":{
        "type":"string",
        "description":"Name of the city"
    },
    "lat":{
        "type":"float",
        "description":"Decimal latitude of the city"
    },
    "lon":{
        "type":"float",
        "description":"Decimal longitude of the city"
    }
}

payload = {
    "model":f"{model}",
    "messages":[
        {
            "role":"system",
            "content":f"You are a helpful AI assistant. The user will enter a country name and the assistant will return the deciaml latitude and decimal longitude of the capital of country. Output in JSON using the schema defined here: {schema}"
        },
        {
            "role":"user",
            "content":"india"
        },
        {
            "role":"assistant",
            "content":"{\"city\":\"Delhi\",\"lat\":\"28.61\",\"lon\":\"77.22\"}"
        },
        {
            "role":"user",
            "content":"jaipur"
        }
    ],
    "format":"json",
    "stream":False
}
response = requests.post(f"{llm_url}/api/chat",json=payload)

cityInfo = json.loads(response.json()['message']['content'])

print(cityInfo)