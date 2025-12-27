import requests
import csv
import json

# Load all URLs from formatted_urls.json
with open("formatted_urls.json", 'r', encoding="utf-8") as file:
    all_urls = json.load(file)

with open('trustpilot_data.csv', 'w', newline='', encoding='utf-8') as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow([
        "displayName", "email", "phone", "website",
        "address", "city", "zipCode", "country"
    ])

    def extract_business_contacts(data):
        results = []
        seen = set()
        # 1. Extract from businessUnits.businesses (most complete)
        try:
            businesses = data["pageProps"]["businessUnits"]["businesses"]
            for biz in businesses:
                key = biz.get("businessUnitId") or biz.get("displayName")
                if key in seen:
                    continue
                seen.add(key)
                contact = biz.get("contact", {})
                location = biz.get("location", {})
                results.append({
                    "displayName": biz.get("displayName", ""),
                    "email": contact.get("email", "emails ended"),
                    "phone": contact.get("phone", ""),
                    "website": contact.get("website", ""),
                    "address": location.get("address", ""),
                    "city": location.get("city", ""),
                    "zipCode": location.get("zipCode", ""),
                    "country": location.get("country", "")
                })
        except Exception as e:
            print("Extraction error (businessUnits):", e)
        # 2. Also extract from recentlyReviewedBusinessUnits (skip duplicates)
        try:
            businesses = data["pageProps"].get("recentlyReviewedBusinessUnits", [])
            for biz in businesses:
                key = biz.get("businessUnitId") or biz.get("displayName")
                if key in seen:
                    continue
                seen.add(key)
                contact = biz.get("contact", {})
                location = biz.get("location", {})
                results.append({
                    "displayName": biz.get("displayName", ""),
                    "email": contact.get("email", ""),
                    "phone": contact.get("phone", ""),
                    "website": contact.get("website", ""),
                    "address": location.get("address", ""),
                    "city": location.get("city", ""),
                    "zipCode": location.get("zipCode", ""),
                    "country": location.get("country", "")
                })
        except Exception as e:
            print("Extraction error (recentlyReviewed):", e)
        return results

    def has_emails(data):
        # Check for any non-empty email in businessUnits or recentlyReviewedBusinessUnits
        try:
            for biz in data["pageProps"]["businessUnits"]["businesses"]:
                if biz.get("contact", {}).get("email"):
                    return True
        except Exception:
            pass
        try:
            for biz in data["pageProps"].get("recentlyReviewedBusinessUnits", []):
                if biz.get("contact", {}).get("email"):
                    return True
        except Exception:
            pass
        return False

    def scraper(base_url):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(base_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for item in extract_business_contacts(data):
                    # Only write if at least one contact field is present
                    if any([item["email"], item["phone"], item["website"], item["address"], item["city"], item["zipCode"], item["country"]]):
                        fields = [
                            item["displayName"],
                            item["email"],
                            item["phone"],
                            item["website"],
                            item["address"],
                            item["city"],
                            item["zipCode"],
                            item["country"]
                        ]
                        writer.writerow([field if field else "N/A" for field in fields])
                if not has_emails(data):
                    return
            else:
                print("Failed to fetch:", base_url)
                return
        except Exception as e:
            print("Request error:", e)
            return

        for page in range(2, 200):
            if "?" in base_url:
                url = f"{base_url}&page={page}"
            else:
                url = f"{base_url}?page={page}"
            try:
                response = requests.get(url, headers=headers)
                print(response.status_code)
                if response.status_code == 200:
                    data = response.json()
                    for item in extract_business_contacts(data):
                        # Only write if at least one contact field is present
                        if any([item["email"], item["phone"], item["website"], item["address"], item["city"], item["zipCode"], item["country"]]):
                            fields = [
                                item["displayName"],
                                item["email"],
                                item["phone"],
                                item["website"],
                                item["address"],
                                item["city"],
                                item["zipCode"],
                                item["country"]
                            ]
                            writer.writerow([field if field else "N/A" for field in fields])
                    if not has_emails(data):
                        break
                else:
                    print("Failed to fetch:", url)
                    break
            except Exception as e:
                print("Request error:", e)
                break

    for url in all_urls:
        scraper(url)

print("............Scraping completed for all Trustpilot urls..................")