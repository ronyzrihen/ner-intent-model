
import re
from requests import get


def lambda_handler(event, context):
    entities = event['entities']
    query_params = {}
    for entity in entities:
        entity["word"] = re.sub('[^A-Za-z0-9 ]+', '', entity["word"])
        if entity["score"] < 0.5:
            print("score too low, skipping entity")
            continue
        query_params[entity["entity_group"]] = entity["word"]
    response = get_query(query_params)
    



def get_query(query_params):
    base_url = "https://api.example.com/search"
    response = get(base_url, params=query_params)
    return response.json()

