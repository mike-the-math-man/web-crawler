from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(url):
    split_result = urlsplit(url)
    path = split_result.path
    if path[-1] == "/":
        path = path[:-1]
    return f"{split_result.netloc}{path}".lower()

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text(strip=True)
        
    h2_tag = soup.find('h2')
    if h2_tag:
        return h2_tag.get_text(strip=True)

    return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    main_tag = soup.find('main')
    if main_tag:
        p_tag = main_tag.find('p')
        if p_tag:
            return p_tag.get_text(strip=True)
    p_tag = soup.find('p')
    if p_tag:
        return p_tag.get_text(strip=True)

    return ""