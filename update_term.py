import os
import random
from bs4 import BeautifulSoup
import requests
from pexels_api import API

# --- CONFIGURATION ---
# The relative path from this bot's location to your portfolio's location
PORTFOLIO_REPO_PATH = "../AdrianAguilar2024.github.io"
PORTFOLIO_HTML_FILE = f"{PORTFOLIO_REPO_PATH}/index.html"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# --- 1. SCRAPE THE TECH TERM ---
# REPLACE IT WITH THIS NEW VERSION
def get_tech_term():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

        # THIS IS THE NEW URL for the dictionary index
        url = "https://techterms.com/definition/"
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # THIS IS THE NEW SELECTOR for finding links on the new page
        term_links = soup.select('div#dictionary_content td a')
        
        if not term_links:
            print("Could not find term links on the page.")
            return None, None

        random_term_link = random.choice(term_links)['href']
        # The links on this page are already full URLs, so we don't need to add the domain
        term_url = random_term_link
        
        term_response = requests.get(term_url, headers=headers, timeout=10)
        term_response.raise_for_status()
        
        term_soup = BeautifulSoup(term_response.text, 'html.parser')
        title = term_soup.find('h1', class_='page-title').text.strip()
        definition = term_soup.find('div', class_='term-definition').find('p').text.strip()
        
        print(f"Successfully scraped: {title}")
        return title, definition
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status code: {http_err.response.status_code}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
        random_term_link = random.choice(term_links)['href']
        term_url = f"https://techterms.com{random_term_link}"
        term_response = requests.get(term_url, timeout=10)
        term_soup = BeautifulSoup(term_response.text, 'html.parser')
        title = term_soup.find('h1', class_='page-title').text.strip()
        definition = term_soup.find('div', class_='term-definition').find('p').text.strip()
        print(f"Successfully scraped: {title}")
        return title, definition
    except Exception as e:
        print(f"Error scraping term: {e}")
        return None, None

# --- 2. GET A RELEVANT IMAGE ---
def get_term_image(query):
    if not PEXELS_API_KEY:
        print("Pexels API Key not found.")
        return "https://via.placeholder.com/800x400"
    try:
        api = API(PEXELS_API_KEY)
        api.search(query, page=1, results_per_page=1)
        if not api.get_entries():
            print(f"No image found for '{query}'. Using a generic tech image.")
            api.search("technology", page=random.randint(1, 10), results_per_page=1)
            if not api.get_entries():
                return "https://via.placeholder.com/800x400"
        photo = api.get_entries()[0]
        image_url = photo.original
        print(f"Found image for '{query}': {image_url}")
        return image_url
    except Exception as e:
        print(f"Error getting image from Pexels: {e}")
        return "https://via.placeholder.com/800x400"

# --- 3. UPDATE THE HTML FILE ---
def update_portfolio(title, definition, image_url):
    try:
        with open(PORTFOLIO_HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tag = soup.find(id='tech-term-image')
        title_tag = soup.find(id='tech-term-title')
        def_tag = soup.find(id='tech-term-definition')
        if not all([img_tag, title_tag, def_tag]):
            print("Error: Could not find all required IDs in the HTML file.")
            return
        img_tag['src'] = image_url
        img_tag['alt'] = f"Image related to {title}"
        title_tag.string = title
        def_tag.string = definition
        with open(PORTFOLIO_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("Successfully updated index.html!")
    except Exception as e:
        print(f"Error updating HTML file: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    term_title, term_def = get_tech_term()
    if term_title and term_def:
        search_query = term_title.split('(')[0].strip()
        term_image_url = get_term_image(search_query)
        update_portfolio(term_title, term_def, term_image_url)
