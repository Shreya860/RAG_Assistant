import os
import requests
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader

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
    # We tweak the query automatically to look for software bugs
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
    """
    if not url:
        return []
    try:
        # html_to_text=True cleans the website code into clean words
        reader = SimpleWebPageReader(html_to_text=True)
        documents = reader.load_data(urls=[url])
        return documents
    except Exception as e:
        print(f"Web scraper encountered an error: {str(e)}")
        return []
if __name__ == "__main__":
    # TEST 1: Test the Google Search (Replace with your actual key to test)
    MY_SERPER_KEY = "1ddb75c2339fa17778fc73ddb7e658481538aaff"
    print("--- TESTING GOOGLE SEARCH ---")
    print(run_serper_search("PyJWT",MY_SERPER_KEY ))
    
    # TEST 2: Test the Web Scraper
    print("\n--- TESTING WEB SCRAPER ---")
    docs = scrape_documentation_url("https://pypi.org/project/requests/")
    if docs:
        print("Success! Scraped Text Sample:")
        print(docs[0].text[:300]) # Prints the first 300 characters

if __name__ == "__main__":
    print("\n--- TESTING WEB SCRAPER ---")
    docs = scrape_documentation_url("https://pypi.org/project/requests/")
    if docs:
        print("Success! Scraped Text Sample:")
        print(docs[0].text[:300])
    else:
        print("Scraper returned no data.")