import csv
import json
import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
MODEL = os.getenv("MODEL", "llama-3.1-8b-instant")
INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input.csv"
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else "output.json"


def ask_llm(review_text):
    prompt = (
        "Определи тональность и тему отзыва. "
        'Верни только JSON вида {"sentiment":"positive|negative|neutral","topic":"..."}. '
        f"\n\nОтзыв: {review_text}"
    )

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        },
        timeout=60,
    )

    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)


if __name__ == "__main__":
    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = ask_llm(row["review"])
            rows.append(
                {
                    "id": row["id"],
                    "review": row["review"],
                    "result": result,
                }
            )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
