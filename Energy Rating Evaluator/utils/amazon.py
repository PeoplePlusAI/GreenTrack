import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import random

def most_relevant_amazon_product(query):
    encoded_query = urllib.parse.quote(f"{query} amazon")
    url = f"https://www.google.com/search?q={encoded_query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Search Failed"
    soup = BeautifulSoup(response.content, 'html.parser')
    search_results = soup.find_all('div', class_='yuRUbf')
    pattern = r'https://www\.amazon\.in/[^/]+/dp/[^/]+'
    for result in search_results:
        link = result.find('a')
        if link:
            href = link['href']
            if re.match(pattern, href):
                return href
    return "Search Failed"

def product_info(amazon_product_url):
    # List of user agents to rotate
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]

    # Comprehensive set of headers
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',  # Do Not Track Request Header
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    try:
        response = requests.get(amazon_product_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except requests.RequestException as e:
        return f"An error occurred: {e}"

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

print(product_info("https://www.amazon.in/Samsung-Inverter-Convertible-Anti-Bacteria-AR18CYNZABE/dp/B0BRQD9Y92"))


