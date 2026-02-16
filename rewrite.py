"""
Content Rewriter
Refines and rewrites translated articles to improve clarity and readability.
"""
import glob
import json
from openai import OpenAI

def get_all_json_files(directory):
    json_files = glob.glob(f"{directory}/*.json")
    return json_files

PROMPT = (
    "Прими роль редактора. Твоя задача переписать правильно эту новость, не используй лишнюю и сложную терминологию. "
    "Подробнее разъясняй некоторые моменты, избегай внешних и англоязычных терминов которые не используются в жизни и совсем не популярны. "
    "Исправь граматические и смысловые ошибки, используй популярные и простые слова "
    "Предоставь ответ в JSON формате с полями 'title' и 'content'"
)
from utils import OpenAIKeyLoader
API_KEY = OpenAIKeyLoader().get_api_key()
def get_openai_response(text, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content

json_files = get_all_json_files("content/translated")
for file_path in json_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
            json_string = json.dumps(json_content, ensure_ascii=False)
            rewrite = get_openai_response(json_string, API_KEY)
            rewrite_json = json.loads(rewrite)
            rewrite_file_path = f"content/rewrited/{file_path.split('/')[-1]}"
            with open(rewrite_file_path, 'w', encoding='utf-8') as rewrite_file:
                json.dump(rewrite_json, rewrite_file, ensure_ascii=False, indent=4)
            print(f"Rewrite saved to {rewrite_file_path}")
    except json.JSONDecodeError:
        print(f"The file {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred while processing the file {file_path}: {e}")

