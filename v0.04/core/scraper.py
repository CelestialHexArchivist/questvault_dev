import requests
from bs4 import BeautifulSoup
import re
import time

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def parse_item_list(base_url, callback=None):
    content = fetch_page_content(base_url)
    if not content:
        if callback:
            callback("Failed to fetch page content")
        return []

    soup = BeautifulSoup(content, "html.parser")
    items = []

    links = soup.select('a[href^="/wiki/"]')
    for link in links:
        item_name = link.text.strip()
        item_url = link.get("href")
        if not item_url or "Category:" in item_url or re.search(r"#.*", item_url):
            continue

        items.append((item_name, base_url + item_url.lstrip('/')))
        if callback:
            callback(f"Found item: {item_name}")

    return items

def scrape_item_details(item_name, item_url, callback=None):
    content = fetch_page_content(item_url)
    if not content:
        if callback:
            callback(f"Failed to fetch details for {item_name}")
        return None

    soup = BeautifulSoup(content, "html.parser")
    description = None
    category = None

    description_element = soup.find("p")
    if description_element:
        description = description_element.text.strip()

    category_element = soup.find("a", href=re.compile("/wiki/Category:"))
    if category_element:
        category = category_element.text.strip()

    if callback:
        callback(f"Scraped details for {item_name}")

    return {
        "name": item_name,
        "description": description,
        "category": category,
    }
