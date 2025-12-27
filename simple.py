import requests
import json
import csv
from concurrent.futures import ThreadPoolExecutor
import threading

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

with open("finalized_url.json", "r", encoding="utf-8") as f:
    all_urls = json.load(f)

results = []

# Thread-safe lock for writing to file
write_lock = threading.Lock()

f_csv = open("trustpilot_data.csv", "a", newline='', encoding="utf-8")
writer = csv.writer(f_csv)
writer.writerow([
        "displayName", "email", "phone", "website",
        "address", "city", "zipCode", "country"
    ])
    

def scraper(all_urls):
    for base_url in all_urls:
        page = 1
        while True:
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}page={page}" if "?" in base_url else f"{base_url}?page={page}"
            try:
                response = requests.get(url, headers=headers)
                data = response.json()
                businesses = data["pageProps"]["businessUnits"]["businesses"]
                if len(businesses) > 0:
                    for i in businesses:
                        # print(i)
                        results.append([
                            i.get("displayName", "N/A") or "N/A",
                            i.get("contact", {}).get("email", "N/A") or "N/A",
                            i.get("contact", {}).get("phone", "N/A") or "N/A",
                            i.get("contact", {}).get("website", "N/A") or "N/A",
                            i.get("location", {}).get("address", "N/A") or "N/A",
                            i.get("location", {}).get("city", "N/A") or "N/A",
                            i.get("location", {}).get("zipCode", "N/A") or "N/A",
                            i.get("location", {}).get("country", "N/A") or "N/A"
                        ])
                else:
                    break
                page += 1
            except Exception:
                break
        
        writer = csv.writer(f_csv)
        writer.writerows(results)

# Run scraping in threads
with ThreadPoolExecutor(max_workers=800) as executor:
    executor.map(lambda args: scraper(*args), [(all_urls,)])

print("---------------------------------------Scraping completed.-------------------------------------------------------------------")