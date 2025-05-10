import os
import json
from transformers import pipeline

model_path = os.environ.get("MODEL_PATH", "intent_model")
nlp = pipeline("text-classification", model=model_path, tokenizer=model_path)


def lambda_handler(event, context):
    print(event)
    if event.get("body", ""):
        body = json.loads(event.get("body", "{}"))
        print(body)
        text = body.get("translated", "")
        language = body.get("language", "english")
    else:
        text = event.get("translated", "")
        language = event.get("language", "english")
        print("here: ", text, language)
    res = nlp(text)[0]
    res["language"] = language
    res["text"] = text
    print(res)
    return {
        "statusCode": 200,
        "body": res
    }
