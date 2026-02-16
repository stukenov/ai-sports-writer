"""
Content Translator
Translates summarized sports articles from English to Russian using OpenAI GPT-4.
"""
import glob
import json
import os
from openai import OpenAI
from utils import OpenAIKeyLoader

def list_files(directory, extension):
    return glob.glob(f"{directory}/*.{extension}")

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def translate_text(text, prompt, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content

def process_translation(directory, api_key, prompt):
    json_files = list_files(directory, 'json')
    for file_path in json_files:
        try:
            json_content = read_json_file(file_path)
            json_string = json.dumps(json_content, ensure_ascii=False)
            translation = translate_text(json_string, prompt, api_key)
            translation_json = json.loads(translation)
            # Extract the filename without the extension
            base_filename = os.path.basename(file_path)
            # Create a new file path in the 'translated' directory with the original filename
            translation_file_path = os.path.join("content/translated", base_filename)
            write_json_file(translation_file_path, translation_json)
            print(f"Translation saved to {translation_file_path}")
        except json.JSONDecodeError:
            print(f"The file {file_path} is not a valid JSON file.")
        except Exception as e:
            print(f"An error occurred while processing the file {file_path}: {e}")

if __name__ == "__main__":
    PROMPT = (
        "You are a helpful assistant. Your task is to translate to Russian language the following news article for a sports portal. "
        "Correctly translate the names of teams and players. Try to use competent Russian language. "
        "Provide the translation in JSON format with 'title' and 'content' parameters."
    )
    API_KEY = OpenAIKeyLoader().get_api_key()
    process_translation("content/summarized", API_KEY, PROMPT)