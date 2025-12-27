import requests
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
import logging

# Configure logging
logging.basicConfig(filename="all_logs",level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

all_urls = []

with open("accurate_urls.txt", 'r', encoding="utf-8") as file:
    for line in file:
        url = line.strip()
        all_urls.append(url)

# Thread-safe lock for writing to file
write_lock = threading.Lock()

# Open the file once, outside the scraper
f_csv = open('W_numbers.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(f_csv)
writer.writerow(["Name","Phone","Email",'Whatsapp Number','Category', 'Location', "Zip Code", "City", "State"])

def scraper(url):
    logging.info(f"Scraping URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_results = data["list"]['out']['base']['results']
            for i in all_results:
                name = i.get('ds_ragsoc', 'N/A')
                number = i.get('ds_ls_telefoni', 'N/A')
                email = i.get('ds_ls_email', 'N/A')
                w_number = i.get('ds_ls_telefoni_whatsapp', 'N/A')
                category = i.get('ds_cat', 'N/A')
                location = i.get('addr', 'N/A')
                zip_code = i.get('ds_cap', 'N/A')
                city = i.get('loc', 'N/A')
                state = i.get('reg', 'N/A')
                 # Ensure only one thread writes at a time
                with write_lock:
                    writer.writerow([name, number, email, w_number, category, location, zip_code, city, state])
    except Exception as e:
        pass

# Prepare all tasks
tasks = []

# Run scraping in threads
with ThreadPoolExecutor(max_workers=500) as executor:
    executor.map(lambda args: scraper(*args), [(url,) for url in all_urls])

# Close the file after all threads are done
f_csv.close()

print("............Scraping completed for all categories and locations..................")

