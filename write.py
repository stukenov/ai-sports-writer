"""
Database Writer
Publishes finalized articles to MySQL database and manages processed files.
"""
import glob
import json
import mysql.connector
import datetime

def get_all_json_files(directory):
    json_files = glob.glob(f"{directory}/*.json")
    return json_files

def insert_articles_to_db(json_files, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    article_data = json.load(file)
                    insert_query = (
                        "INSERT INTO `articles` "
                        "(`ru_title`, `ru_fulltxt`, `ru_pubdate`, `created_at`, `updated_at`) "
                        "VALUES (%s, %s, %s, %s, %s)"
                    )
                    data_to_insert = (
                        article_data.get('title'),
                        article_data.get('content'),
                        current_datetime,
                        current_datetime,
                        current_datetime
                    )
                    cursor.execute(insert_query, data_to_insert)
            except json.JSONDecodeError as e:
                print(f"An error occurred while decoding the file {file_path}: {e}")
            except Exception as e:
                print(f"An error occurred while processing the file {file_path}: {e}")
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

import os
import shutil

def move_processed_files_to_completed(json_files, completed_directory):
    ensure_directory_exists(completed_directory)
    for json_file in json_files:
        base = os.path.basename(json_file)
        new_filename = os.path.splitext(base)[0] + '.txt'
        new_filepath = os.path.join(completed_directory, new_filename)
        shutil.move(json_file, new_filepath)
        print(f"Moved processed file to {new_filepath}")

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

import glob

def delete_processed_files(file_names, directories):
    for directory in directories:
        for file_name in file_names:
            # Construct the file path with both possible extensions
            txt_file_path = os.path.join(directory, f"{os.path.splitext(file_name)[0]}.txt")
            json_file_path = os.path.join(directory, f"{os.path.splitext(file_name)[0]}.json")
            
            # Check if the file exists with .txt extension and delete
            if os.path.exists(txt_file_path):
                os.remove(txt_file_path)
                print(f"Deleted file: {txt_file_path}")
            
            # Check if the file exists with .json extension and delete
            if os.path.exists(json_file_path):
                os.remove(json_file_path)
                print(f"Deleted file: {json_file_path}")




from utils import MySQLConfigLoader
db_config = MySQLConfigLoader().get_config()

json_files = get_all_json_files('content/rewrited')

insert_articles_to_db(json_files, db_config)

move_processed_files_to_completed(json_files, 'content/completed')


# Get the base names of the processed json files
processed_file_names = [os.path.basename(json_file) for json_file in json_files]

# Directories to delete files from
directories_to_clean = ['content/scraped', 'content/summarized', 'content/translated', 'content/rewrited']

# Delete the processed files
delete_processed_files(processed_file_names, directories_to_clean)
