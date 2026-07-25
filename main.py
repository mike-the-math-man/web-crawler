import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report


async def main_async():
    print("run main.py <URL> <max_concurrency> <max_pages>")
    if len(sys.argv) <2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    print(f"starting crawl of: {sys.argv[1]}")    # -v
    if len(sys.argv) == 2:
        page_data = await crawl_site_async(sys.argv[1])
    if len(sys.argv) == 3:
        page_data = await crawl_site_async(sys.argv[1], int(sys.argv[2]))
    if len(sys.argv) == 4:
        page_data = await crawl_site_async(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    #for page in page_data.values():
        #print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")
    write_json_report(page_data)
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main_async())
    

#https://learnwebscraping.dev/practice/ecommerce/
#https://learnwebscraping.dev/practice/ecommerce/products/ashenfang-longsword-fan-1001/
