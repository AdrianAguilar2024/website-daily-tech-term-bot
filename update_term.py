import os
import random
from bs4 import BeautifulSoup
import requests
from pexels_api import API
from datetime import datetime

# --- CONFIGURATION ---
PORTFOLIO_REPO_PATH = "../AdrianAguilar2024.github.io"
PORTFOLIO_HTML_FILE = f"{PORTFOLIO_REPO_PATH}/index.html"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# --- 1. SCRAPE A TERM FROM THE "TECHNICAL" CATEGORY PAGE ---
def get_tech_term():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # YOUR NEW URL for the Technical category
        url = "https://techterms.com/category/technical"
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The selector for links on this category page
        term_links = soup.select('ul.termlist a')
        
        if not term_links:
            print("Could not find term links on the category page.")
            return None, None

        # Pick a random term from the list
        random_term_link = random.choice(term_links)['href']
        term_url = random_term_link # The links are already full URLs
        
        # Scrape the specific term's page
        term_response = requests.get(term_url, headers=headers, timeout=15)
        term_response.raise_for_status()
        
        term_soup = BeautifulSoup(term_response.text, 'html.parser')
        title = term_soup.find('h1', class_='page-title').text.strip()
        definition = term_soup.find('div', class_='term-definition').find('p').text.strip()
        
        print(f"Successfully scraped: {title}")
        return title, definition
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
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
            api.search("technology abstract", page=random.randint(1, 10), results_per_page=1)
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
def update_portfolio(title, definition, image_url, date_str):
    try:
        with open(PORTFOLIO_HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        img_tag = soup.find(id='tech-term-image')
        title_tag = soup.find(id='tech-term-title')
        date_tag = soup.find(id='tech-term-date')
        def_tag = soup.find(id='tech-term-definition')

        if not all([img_tag, title_tag, date_tag, def_tag]):
            print("Error: Could not find all the required IDs in the HTML file.")
            return

        img_tag['src'] = image_url
        img_tag['alt'] = f"Image related to {title}"
        title_tag.string = title
        date_tag.string = f"Updated: {date_str}"
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
        today_date = datetime.now().strftime("%B %d, %Y")
        search_query = term_title.split('(')[0].strip()
        term_image_url = get_term_image(search_query)
        update_portfolio(term_title, term_def, term_image_url, today_date)
