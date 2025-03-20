import json
import random
from datetime import datetime, timedelta

alert_zones = ["Ashdod - Port", "Tel Aviv", "Jerusalem", "Haifa", "Beer Sheva", "Eilat", "Netanya", "Rishon LeZion"]
titles = ["ירי רקטות וטילים", "חדירת כלי טיס עוין"]
categories = {1: "ירי רקטות וטילים", 2: "חדירת כלי טיס עוין"}
categories_en = {1: "Missile and Rocket Fire", 2: "Hostile Aircraft Intrusion"}

# הוספת תבניות נוספות לשאלות כדי ליצור גיוון נוסף
question_templates = [
    "How many {category} alerts were recorded in {location} in the last {days} days?",
    "Tell me the number of {category} alerts in {location} in the past {days} days.",
    "Were there any {category} alerts in {location} in the last {days} days?",
    "Give me the count of {category} alerts in {location} over the past {days} days.",
    "Can you check how many {category} alerts happened in {location} in the last {days} days?",
    "Please provide the number of {category} alerts recorded in {location} within the past {days} days.",
    "Did {location} experience any {category} alerts in the last {days} days?",
    "How frequent were {category} alerts in {location} in the previous {days} days?",
    "Check the records: how many {category} alerts occurred in {location} in the past {days} days?"
]
additional_question_templates = [
    "Were there any alerts in {location} in the last hour?",
    "How many alerts were recorded in {location} in the last {hours} hours?",
    "Can you tell me if there were any {category} alerts in {location} today?",
    "Show me the total {category} alerts in {location} in the past {hours} hours.",
    "Did any {category} alert happen in {location} in the last {hours} hours?",
    "Check for alerts in {location} within the previous {hours} hours.",
    "How many {category} alerts were reported in {location} in the last {hours} hours?",
    "Give me a count of {category} alerts in {location} over the past {hours} hours.",
    "Were there any {category} alerts recorded in {location} within the past {hours} hours?",
    "Has {location} experienced any {category} alerts today?",
    "Tell me if there have been any {category} alerts in {location} recently.",
    "I need to know the number of {category} alerts in {location} from the last {hours} hours.",
    "List the number of alerts that occurred in {location} in the last {hours} hours.",
]


def generate_dynamodb_query(question, location, start_date, category):
    return {
        "TableName": "missile_alert",
        "FilterExpression": "alertDate >= :start AND contains(data, :location) AND title = :title",
        "ExpressionAttributeValues": {
            ":start": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            ":location": location,
            ":title": category
        },
        "Select": "COUNT"
    }


# שילוב כל התבניות יחד
all_question_templates = question_templates + additional_question_templates

# יצירת הדאטהסט עם מגוון השאלות
expanded_dataset = []
for _ in range(200):  # מגדילים את מספר הדוגמאות
    location = random.choice(alert_zones)
    time_range = random.choice([random.randint(1, 365), random.randint(1, 24)])  # ימים או שעות
    is_days = time_range > 24
    start_date = datetime.now() - timedelta(days=time_range) if is_days else datetime.now() - timedelta(hours=time_range)
    category_id = random.choice([1, 2])
    category_en = categories_en[category_id]
    catagory = categories[category_id]
    # בחירת תבנית שאלה אקראית ושימוש בפרמטרים המתאימים
    question_template = random.choice(all_question_templates)
    question = question_template.format(category=category_en, location=location, days=time_range, hours=time_range)

    # יצירת שאילתא מתאימה
    dynamodb_query = generate_dynamodb_query(question, location, start_date, catagory)

    # הוספת הדוגמא למערך
    expanded_dataset.append({
        "messages": [
            {"role": "system", "content": "you are a dynamodb query generator that turns every input into the corresponding dynamodb request"},
            {"role": "user", "content": question},
            {"role": "assistant", "content": json.dumps(dynamodb_query)}
        ]
    })

# שמירה לקובץ JSON עם השאלות המגוונות
expanded_dataset_path = "./datasets/dynamodb_finetune_dataset.json"
with open(expanded_dataset_path, "w", encoding="utf-8") as f:
    json.dump(expanded_dataset, f, indent=4, ensure_ascii=False)

expanded_dataset_path
