"""
Content Summarizer
Uses OpenAI GPT-4 to summarize scraped sports articles.
"""
import glob
import json
import openai
import os
from utils import OpenAIKeyLoader

def list_text_files(directory):
    """Return a list of text files in the given directory."""
    return glob.glob(f"{directory}/*.txt")

def read_file(file_path):
    """Read and return the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_json_file(file_path, data):
    """Write data to a file in JSON format."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def summarize_text(text, prompt, api_key):
    """Summarize the text using OpenAI API and return the summary."""
    client = openai.OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content

def main():
    directory = "content/scraped"
    output_directory = "content/summarized"
    prompt = (
        "You are a helpful assistant. Your task is to summarize the following news article for a sports portal, "
        "ensuring the summary is no more than 200 words and free from unnecessary words and artifacts from internet download. "
        "Provide the summary in JSON format with 'title' and 'content' parameters."
    )
    api_key = OpenAIKeyLoader().get_api_key()

    text_files = list_text_files(directory)
    for file_path in text_files:
        try:
            text_content = read_file(file_path)
            summary = summarize_text(text_content, prompt, api_key)
            summary_json = json.loads(summary)
            # Extract the filename without the extension and add the new extension
            base_filename = os.path.basename(file_path)
            summary_filename = os.path.splitext(base_filename)[0] + ".json"
            summary_file_path = os.path.join(output_directory, summary_filename)
            write_json_file(summary_file_path, summary_json)
            print(f"Summary saved to {summary_file_path}")
        except Exception as e:
            print(f"An error occurred while summarizing the file {file_path}: {e}")

if __name__ == "__main__":
    main()
