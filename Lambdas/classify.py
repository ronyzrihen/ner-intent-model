
from transformers import pipeline
# from query_creation import lambda_handler


def lambda_handler(event, context):
    print(event)
    text = event['text']
    language = event['language']
    nlp = pipeline("ner", model="/mnt/model", tokenizer="/mnt/model", aggregation_strategy="simple")
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
        if current_entity and entity["entity_group"] == current_entity["entity_group"]:
            if entity["start"] == current_entity["end"]:
                current_entity["word"] += entity["word"]
            else:
                current_entity["score"] = current_entity["score"] / sub_words_count
                sub_words_count = 1
                merged_entities.append(current_entity)
                current_entity = entity.copy()

            current_entity["end"] = entity["end"] 
            current_entity["score"] = (current_entity["score"] + entity["score"])
            sub_words_count += 1
        else:
            if current_entity:
                merged_entities.append(current_entity)
            current_entity = entity.copy()
    if current_entity:
        merged_entities.append(current_entity)

    return merged_entities
