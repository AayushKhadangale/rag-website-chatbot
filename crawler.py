import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website(start_url, max_depth=1):
    visited = set()
    queue = [(start_url, 0)]
    pages = []

    base_domain = urlparse(start_url).netloc

    while queue:
        url, depth = queue.pop(0)
        if url in visited or depth > max_depth:
            continue

        visited.add(url)

        try:
            res = requests.get(url, timeout=10)
            if "text/html" not in res.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for tag in soup(["script", "style", "noscript", "img"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            if text:
                pages.append(text)

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if urlparse(next_url).netloc == base_domain:
                    queue.append((next_url, depth + 1))

        except Exception:
            continue

    return pages
