# import requests

# query_params = {}
# query_params["user_id"] = None
# response = requests.get("https://ems-be.plutos.one/api/v1/polls/5/previous/entertainment", params=query_params, timeout=5)

# json_res = response.json()

# print(json_res.get('data')[1]['question'])

from generate import intent_classification,get_poll_category

print(get_poll_category("give me lifestyle polls"))