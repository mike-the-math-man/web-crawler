from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
#import requests
import asyncio
import aiohttp

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int = 5, max_pages: int = 40):
        self.base_url = base_url #(the starting URL)
        self.base_domain = urlsplit(base_url).netloc #(the domain name)
        self.page_data = {} #(our dictionary of page data, keyed by normalized URL)
        self.lock = asyncio.Lock() #(an asyncio.Lock to safely update page_data)
        self.max_concurrency = max_concurrency #(to limit the number of requests allowed at once)
        self.semaphore = asyncio.Semaphore(max_concurrency) #(an asyncio.Semaphore - pass it the value of max_concurrency)
        self.session: aiohttp.ClientSession  #(an aiohttp.ClientSession for making HTTP requests)
        self.max_pages = max_pages 
        self.should_stop = False
        self.all_tasks = set()
        self.claimed_urls = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, url):
        if self.should_stop:
            return False
        if urlsplit(url).netloc != self.base_domain:
            return False
        norm = normalize_url(url)
        async with self.lock:
            if self.should_stop:
                return False
            if norm in self.claimed_urls:
                return False
            if len(self.page_data) >= self.max_pages:
                if not self.should_stop:
                    self.should_stop = True
                    print("Reached maximum number of pages to crawl")
                    for task in self.all_tasks:
                        if not task.done():
                            task.cancel()
                return False
            self.claimed_urls.add(norm)
            return True

    async def get_html(self, url):
        if self.session is None:
            return None
        headers = {"User-Agent": "BootCrawler/1.0"}
        try:
            async with self.session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                content_type = resp.headers.get("Content-Type", "") 
                if content_type.split(";")[0].strip() != "text/html":
                    raise TypeError
                return await resp.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def crawl_page(self, current_url=None):
            if self.should_stop:
                return
            if current_url == None:
                current_url = self.base_url
           
            base_split_result = urlsplit(self.base_url)
            base_netloc = base_split_result.netloc
            current_split_result = urlsplit(current_url)
            current_netloc = current_split_result.netloc
            if base_netloc != current_netloc:
                return
            if not await  self.add_page_visit(current_url):
                return
            if self.should_stop:
                return
            norm_curr_url = normalize_url(current_url)
            async with self.semaphore:
                print(f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})")
                #curr_url_html = get_html(current_url)
                html = await self.get_html(current_url)
                if html is None:
                    return
                rich_page_data = extract_page_data(html,current_url)
                
                #html = await self.get_html(current_url)
            #print(f"crawling: {current_url}")
            
                async with self.lock:
                    self.page_data[norm_curr_url] = rich_page_data
                next_urls = rich_page_data["outgoing_links"]
            #tasks: list[asyncio.Task[None]] = []
            if self.should_stop:
                return
            for url in next_urls:
                #tasks.append(asyncio.create_task(self.crawl_page(url)))
                new_tasks = asyncio.create_task(self.crawl_page(url))
                #tasks.append(new_tasks)
                self.all_tasks.add(new_tasks)
            #if tasks:
                #try:
                    #await asyncio.gather(*tasks)
                #finally:
                    #for task in tasks:
                        #self.all_tasks.discard(task)
            #print("cleaning up", asyncio.current_task())
        #return self.page_data

    async def crawl(self):
        await self.crawl_page()
        while True:
            tasks = list(self.all_tasks)
            if not tasks:
                break
            results = await asyncio.gather(*tasks, return_exceptions=True)
            self.all_tasks.difference_update(tasks)   # don't rely on finally
            for r in results:
                if isinstance(r, asyncio.CancelledError):
                    continue
                if isinstance(r, Exception):
                    print(f"task failed: {r!r}")
        return self.page_data




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
            if not isinstance(tag, Tag):
                continue
            href = tag.get("href")
            if isinstance(href, str) and href:
                return_list.append(urljoin(base_url, href))
    return return_list


def get_images_from_html(html, base_url):
    return_list = []
    soup = BeautifulSoup(html, 'html.parser')
    tags_list = soup.find_all('img')
    if tags_list:
        for tag in tags_list:
            if not isinstance(tag, Tag):
                continue
            src = tag.get("src")
            if isinstance(src, str) and src:
                try:
                    absolute_url = urljoin(base_url, src)
                    return_list.append(absolute_url)
                except Exception as e:
                    print(f"{str(e)}: {src}")
            #return_list.append(urljoin(base_url,tag.get("src")))
    return return_list

def extract_page_data(html: str, page_url: str):
    dict = PageData(url=page_url, #normalize_url()
                    heading=get_heading_from_html(html),
                    first_paragraph=get_first_paragraph_from_html(html),
                    outgoing_links=get_urls_from_html(html,page_url),
                    image_urls=get_images_from_html(html,page_url)
                    )
    return dict

async def crawl_site_async(base_url, max_concurrency=5, max_pages=40):
    async with AsyncCrawler(base_url,max_concurrency, max_pages) as crawler_var:
        return await crawler_var.crawl()
    
