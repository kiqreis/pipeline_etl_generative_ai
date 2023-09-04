import pandas as pd
import requests
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

sdw2023_api_url = os.getenv('LINK')
openai_api_key = "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"

openai.api_key = openai_api_key

df = pd.read_csv("SDW2023.csv")
user_ids = df['UserID'].tolist()


def get_user(id):
    response = requests.get(f"{sdw2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You must act like a banking marketing expert"
            },
            {
                "role": "user",
                "content": f"Create a personalized message for {user['name']} about the importance of investments (maximum of 200 characters)"
            }
        ]
    )

    return completion.choices[0].message.content.strip("\"")


users = [user for id in user_ids if (user := get_user(id)) is not None]

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander/-dev-week-2023-api/icons/credit.svg",
        "description": news
    })


def update_user(user):
    response = requests.put(
        f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}")
