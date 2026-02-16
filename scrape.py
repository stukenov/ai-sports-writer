"""
Web Scraper for Sports News
Scrapes football news articles from Eurosport.
"""
import requests
import re
import os
from bs4 import BeautifulSoup

def scrape_eurosport_football(url, directory, completed_directory):
    ensure_directory_exists(directory)
    ensure_directory_exists(completed_directory)
    links = get_filtered_links(url)
    if not all_files_exist(links, completed_directory):
        scrape_links_content(links, directory, completed_directory)
    else:
        print("All files already exist in the completed directory. Stopping the program.")

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def get_response(url):
    return requests.get(url)

def check_response_status(response):
    return response.status_code == 200

def get_filtered_links(url):
    link_pattern = re.compile(r'https?://[^\s]+')
    response = get_response(url)
    if check_response_status(response):
        links = extract_links(response.text, link_pattern)
        return filter_links(links, url)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

def extract_links(content, link_pattern):
    return link_pattern.findall(content)

def filter_links(links, base_url):
    return [link.rstrip('"') for link in links if link.startswith(base_url) and link.endswith('story.shtml"')]

def all_files_exist(links, completed_directory):
    return all(is_file_present(completed_directory, extract_news_id(link)) for link in links)

def scrape_links_content(links, directory, completed_directory):
    for link in links:
        news_id = extract_news_id(link)
        if not news_id:
            print(f'Could not extract news ID from {link}')
            continue
        if not is_file_present(completed_directory, news_id):
            content_text = fetch_content_text(link)
            if content_text:
                save_content(directory, content_text, news_id)
            else:
                print(f'Content not found in {link}')
        else:
            print(f'File for {news_id} already exists. Skipping download.')

def is_file_present(directory, news_id):
    filename = f'{news_id}.txt'
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)

def fetch_content_text(url):
    response = get_response(url)
    if check_response_status(response):
        return extract_content_text(response.text)
    else:
        print(f'Failed to retrieve {url}. Status code: {response.status_code}')
        return None

def extract_content_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find('div', id='content')
    if content_div:
        return content_div.get_text(separator=' ', strip=True)
    return None

def extract_news_id(url):
    match = re.search(r'_sto(\d+)/story\.shtml', url)
    return match.group(1) if match else 'unknown'

def save_content(directory, content_text, news_id):
    filename = f'{news_id}.txt'
    file_path = os.path.join(directory, filename)
    write_content_to_file(file_path, content_text)
    print(f'Saved {filename}')

def write_content_to_file(file_path, content_text):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_text)


def main():
    """Main function to run the scraper."""
    url = 'https://www.eurosport.com/football/'
    directory = 'content/scraped'
    completed_directory = 'content/completed'
    scrape_eurosport_football(url, directory, completed_directory)


if __name__ == "__main__":
    main()
