import json

with open("datasets/refined_ner_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

new_dataset = []
for input in dataset:
    q = " ".join(input["tokens"])
    if "How many" in q or "Tell me" in q or "number of" in q or "count of" in q:
        input["intent"] = "COUNT_ALERTS"
    elif "Were there any" in q or "Has there" in q or "Were there" in q or "less than" in q:
        input["intent"] = "CHECK_ALERTS"
    elif "Give me" in q or "Show me" in q:
        input["intent"] = "SHOW_ALERTS"
    elif "When" in q:
        input["intent"] = "TIME_ALERTS"
    else:
        input["intent"] = "UNKNOWN"

for i in dataset:
    if i["intent"] == "CHECK_ALERTS":
        print(" ".join(i["tokens"]), i["intent"])
        # new_dataset.append(i)

with open("datasets/intent_ner_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)
