import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv  # Requires: pip install python-dotenv
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader

# Load environment variables from the .env file at startup
load_dotenv()

def run_serper_search(query: str, serper_api_key: str) -> str:
    """
    Searches Google for live issues/vulnerabilities about a package.
    """
    if not serper_api_key:
        return "No Serper API key found. Skipping live internet search."
    
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    # Automatically tweak the query to look for software bugs
    payload = {
        "q": f"{query} open source package bug security vulnerability",
        "num": 4
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json()
            search_context = []
            
            if "organic" in results:
                for item in results["organic"]:
                    search_context.append(f"Source: {item.get('link', '')}\nContext: {item.get('snippet', '')}\n---")
            
            return "\n".join(search_context) if search_context else "No new bugs found on the web."
        return f"Serper Error: Status code {response.status_code}"
    except Exception as e:
        return f"Search connection failed: {str(e)}"


def scrape_documentation_url(url: str) -> list:
    """
    Scrapes a documentation webpage and reads the raw text.
    Validates against allowed base domains to prevent SSRF while supporting subdomains.
    """
    if not url:
        return []
        
    # Define your trusted base domains
    ALLOWED_BASE_DOMAINS = ("pypi.org", "readthedocs.org", "readthedocs.io", "github.com")
    
    try:
        # Extract the netloc (domain name) from the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Strip out port numbers if they exist (e.g., 'localhost:8080' -> 'localhost')
        if ":" in domain:
            domain = domain.split(":")[0]
            
        # Securely check if the domain is exactly allowed, or ends with an allowed subdomain (.pypi.org)
        # This prevents attackers from bypassing with domains like 'fake-github.com'
        is_allowed = domain in ALLOWED_BASE_DOMAINS or domain.endswith(tuple(f".{d}" for d in ALLOWED_BASE_DOMAINS))
        
        if not is_allowed:
            print(f"Security Alert: Blocked unauthorized scrap request to domain '{domain}'")
            return []
            
        # html_to_text=True cleans the website code into clean words
        reader = SimpleWebPageReader(html_to_text=True)
        documents = reader.load_data(urls=[url])
        return documents
        
    except Exception as e:
        print(f"Web scraper encountered an error: {str(e)}")
        return []


if __name__ == "__main__":
    # Fetch the API key safely from your environment variables
    api_key = os.getenv("MY_SERPER_KEY", "")
    
    # TEST 1: Test the Google Search
    print("--- TESTING GOOGLE SEARCH ---")
    print(run_serper_search("PyJWT", api_key))
    
    # TEST 2: Test the Web Scraper
    print("\n--- TESTING WEB SCRAPER ---")
    docs = scrape_documentation_url("https://pypi.org/project/requests/")
    if docs:
        print("Success! Scraped Text Sample:")
        print(docs[0].text[:300])  # Prints the first 300 characters
    else:
        print("Scraper returned no data.")