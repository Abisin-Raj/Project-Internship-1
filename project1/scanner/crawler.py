import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.to_visit = [base_url]

    def crawl(self):
        # loop through all the pages we found and keep goin
        while self.to_visit:
            url = self.to_visit.pop(0)
            if url in self.visited_urls:
                continue
            
            try:
                response = requests.get(url, timeout=5)
                self.visited_urls.add(url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href and href.startswith('http'):
                            if href not in self.visited_urls:
                                self.to_visit.append(href)
            except Exception as e:
                print(f"Error crawling {url}: {e}")
        
    def extract_forms(self, url):
        # uses beatifulsoup to grab all the forms from the pagee
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.find_all('form')
        except Exception as e:
            print(f"Error extracting forms from {url}: {e}")
        return []

    def get_form_details(self, form):
        details = {}
        action = form.attrs.get("action")
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            inputs.append({"type": input_type, "name": input_name})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details
