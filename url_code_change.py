import json
import re

# Load URLs from JSON file
with open('finalized_url.json', 'r') as f:
    urls = json.load(f)

# Update the version in each URL
updated_urls = [
    re.sub(r'categoriespages-consumersite-2\.943\.0', 'categoriespages-consumersite-2.966.0', url)
    for url in urls
]

# Save the updated URLs back to the JSON file
with open('finalized_url.json', 'w') as f:
    json.dump(updated_urls, f, indent=2)

print("URLs updated successfully.")