import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "img", "noscript", "iframe"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""
    headings = " ".join(
        h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])
    )
    text = soup.get_text(separator=" ", strip=True)

    return f"{title}\n{headings}\n{text}"


def crawl_website(start_url, max_depth=2):
    visited = set()
    data = []

    base_domain = urlparse(start_url).netloc
    queue = [(start_url, 0)]

    while queue:
        url, depth = queue.pop(0)

        if url in visited or depth > max_depth:
            continue

        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            content_type = response.headers.get("Content-Type", "")

            if "text/html" not in content_type:
                continue

            html = response.text
            cleaned_text = clean_html(html)
            data.append(cleaned_text)

            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if urlparse(next_url).netloc == base_domain:
                    queue.append((next_url, depth + 1))

        except Exception:
            continue

    return data

