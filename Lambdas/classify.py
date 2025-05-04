
from transformers import pipeline
import json
import wordninja
import os


def lambda_handler(event, context):
    model_path = os.environ.get("MODEL_PATH", "testing/ner_varied_model1")
    print(event)
    if event.get("body", ""):
        body = json.loads(event.get("body", "{}"))
        text = body.get("text", "")
        language = body.get("language", "english")
    else:
        text = event.get("text", "")
        language = event.get("language", "english")
    nlp = pipeline("ner", model=model_path, tokenizer=model_path, aggregation_strategy="simple")
    entities = nlp(text)
    for item in entities:
        item["score"] = float(item["score"])
    classifications = merge_subwords(entities)
    print(classifications)
    return {
        "statusCode": 200,
        "body": {"entities": classifications, "input": text, "language": language }
        }


def merge_subwords(ner_results):
    merged_entities = []
    current_entity = None
    sub_words_count = 1

    for entity in ner_results:
        if current_entity:
            if entity["entity_group"] == current_entity["entity_group"]:
                current_entity["word"] += entity["word"]
                current_entity["score"] += entity["score"]
                sub_words_count += 1
                continue
            current_entity["score"] = current_entity["score"] / sub_words_count
            current_entity["word"] = split_if_needed(current_entity["word"])
            merged_entities.append(current_entity)
            current_entity = entity.copy()
            sub_words_count = 1
            continue
        current_entity = entity.copy()
    current_entity["score"] = current_entity["score"] / sub_words_count
    current_entity["word"] = split_if_needed(current_entity["word"])
    print(current_entity["word"])
    merged_entities.append(current_entity)
    return merged_entities


def split_if_needed(word):
    parts = wordninja.split(word)
    return " ".join(parts) if len(parts) > 1 else word


# if __name__ == "__main__":
#     event = {
#         "text": "How many missile alerts were there in Tel Aviv three days ago",
#         "language": "hebrew"
#     }
#     context = {}
#     print(lambda_handler(event, context))
