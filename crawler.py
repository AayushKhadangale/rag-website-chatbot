import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
HEADERS = {
   "User-Agent": "Mozilla/5.0 (RAG-Chatbot)"
}
def crawl_website(base_url, max_depth=2, max_pages=10):
   visited = set()
   pages = []
   def crawl(url, depth):
       if depth > max_depth or url in visited or len(pages) >= max_pages:
           return
       visited.add(url)
       try:
           res = requests.get(url, headers=HEADERS, timeout=10)
           if "text/html" not in res.headers.get("Content-Type", ""):
               return
           soup = BeautifulSoup(res.text, "html.parser")
           # Remove junk
           for tag in soup(["script", "style", "noscript", "img"]):
               tag.decompose()
           title = soup.title.string if soup.title else ""
           headings = " ".join(h.get_text(" ", strip=True) for h in soup.find_all(["h1","h2","h3"]))
           body = soup.get_text(" ", strip=True)
           full_text = f"{title}\n{headings}\n{body}".strip()
           if full_text:
               pages.append(full_text)
           for link in soup.find_all("a", href=True):
               next_url = urljoin(url, link["href"])
               if urlparse(next_url).netloc == urlparse(base_url).netloc:
                   crawl(next_url, depth + 1)
       except Exception:
           pass
   crawl(base_url, 0)
   return pages
