from selenium import webdriver
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome()  
driver.get('https://www.trustpilot.com/categories') 

# Find all <a> tags
a_tags = driver.find_elements(By.XPATH, "//*/a")

# Extract href attributes
urls = [a.get_attribute('href') for a in a_tags if a.get_attribute('href')]
selected_urls = urls[10:220]

# print(selected_urls)

# Save the selected URLs to a JSON file
with open('selected_urls.json', 'w') as f:
    json.dump(selected_urls, f, indent=2)

driver.quit()

# Load the original URLs
with open('selected_urls.json', 'r') as f:
    original_urls = json.load(f)

# Extract the category slug and build new URLs
base_url = "https://www.trustpilot.com/_next/data/categoriespages-consumersite-2.943.0/categories/{}.json?page={}"
category_slugs = [url.rstrip('/').split('/')[-1] for url in original_urls]
new_urls = [base_url.format(slug, "") for slug in category_slugs]  # "" leaves {} for page

# Save the new URLs to a JSON file
with open('formatted_urls.json', 'w') as f:
    json.dump(new_urls, f, indent=2)

.