import os
import random
import json # Import the json library
from pexels_api import API
from datetime import datetime

# --- CONFIGURATION ---
PORTFOLIO_REPO_PATH = "../AdrianAguilar2024.github.io"
PORTFOLIO_HTML_FILE = f"{PORTFOLIO_REPO_PATH}/index.html"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# --- 1. GET A TERM FROM OUR LOCAL JSON FILE ---
def get_tech_term():
    try:
        # Read our local dictionary of terms and definitions
        with open('definitions.json', 'r', encoding='utf-8') as f:
            terms_data = json.load(f)
        
        if not terms_data:
            print("Error: definitions.json is empty or not found.")
            return None, None
            
        # Pick a random term object from the list
        random_term_obj = random.choice(terms_data)
        title = random_term_obj['term']
        definition = random_term_obj['definition']
        
        print(f"Selected random term from local file: {title}")
        return title, definition
    except FileNotFoundError:
        print("Error: definitions.json not found. Please create it.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
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
        
        # We will use simple string replacement, which is safer than parsing the whole HTML
        # This looks for special "placeholder" comments in your HTML
        from bs4 import BeautifulSoup
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
