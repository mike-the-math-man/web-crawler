import json

def write_json_report(page_data, filename="report.json"):
    f =open(filename, "w", encoding="utf-8")
    pages = sorted(page_data.values(), key=lambda p: p["url"])
    json.dump(pages,f,indent=2)