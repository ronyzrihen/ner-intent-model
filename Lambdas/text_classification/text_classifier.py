import os
import json
from transformers import pipeline


def lambda_handler(event, context):
    model_path = os.environ.get("MODEL_PATH", "intent_model")
    print(event)
    if event.get("body", ""):
        body = json.loads(event.get("body", "{}"))
        text = body.get("text", "")
        language = body.get("language", "english")
    else:
        text = event.get("text", "")
        language = event.get("language", "english")
    nlp = pipeline("text-classification", model=model_path, tokenizer=model_path)
    res = nlp(text)[0]
    res["language"] = language
    res["input"] = text

    return {
        "statusCode": 200,
        "body": res
    }
