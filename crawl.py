from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url):
    split_result = urlsplit(url)
    path = split_result.path
    if len(path)>0 and path[-1] == "/":
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


def get_urls_from_html(html, base_url):
    return_list = []
    soup = BeautifulSoup(html, 'html.parser')
    tags_list = soup.find_all('a')
    if tags_list:
        for tag in tags_list:
            return_list.append(urljoin(base_url,tag.get("href")))
    return return_list


def get_images_from_html(html, base_url):
    return_list = []
    soup = BeautifulSoup(html, 'html.parser')
    tags_list = soup.find_all('img')
    if tags_list:
        for tag in tags_list:
            return_list.append(urljoin(base_url,tag.get("src")))
    return return_list

def extract_page_data(html: str, page_url: str):
    dict = PageData(url=page_url, #normalize_url()
                    heading=get_heading_from_html(html),
                    first_paragraph=get_first_paragraph_from_html(html),
                    outgoing_links=get_urls_from_html(html,page_url),
                    image_urls=get_images_from_html(html,page_url)
                    )
    return dict