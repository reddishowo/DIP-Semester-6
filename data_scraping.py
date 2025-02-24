import requests
import json
import time
import re

# Function to detect English text - moved to the beginning
def is_english(text):
    english_pattern = re.compile(r'^[a-zA-Z0-9\s\.,!?\'\"()-_:;]+$')
    words = text.split()
    if not words:
        return False
    
    english_words = 0
    for word in words:
        if english_pattern.match(word):
            english_words += 1
    
    return (english_words / len(words)) >= 0.7

# App ID for Apex Legends
app_id = "1172470"
all_reviews = []
cursor = "*"
max_pages = 100  

for page in range(max_pages):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&num_per_page=100&cursor={cursor}&language=english&review_type=all&purchase_type=all&filter=all"
   
    print(f"Fetching page {page+1} with URL: {url}")
    response = requests.get(url)
   
    if response.status_code == 200:
        try:
            data = response.json()
           
            # Print some debug info about the response
            total_reviews = data.get("query_summary", {}).get("total_reviews", 0)
            print(f"Total reviews according to query summary: {total_reviews}")
           
            reviews = data.get("reviews", [])
           
            if not reviews:
                print("No more reviews found.")
                break
               
            # Only add English reviews
            english_reviews = []
            for review in reviews:
                review_text = review.get("review", "")
                # Check if review is in English
                if review_text and is_english(review_text):
                    english_reviews.append(review)
            
            all_reviews.extend(english_reviews)
            print(f"Fetched {len(english_reviews)} English reviews out of {len(reviews)}. Total collected: {len(all_reviews)}")
           
            # Get cursor for next page
            cursor = data.get("cursor", "")
            print(f"Next cursor: {cursor}")
           
            if not cursor:
                print("No cursor for next page.")
                break
               
            # Add a short delay to avoid rate limiting
            time.sleep(2)
           
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            break
    else:
        print(f"Failed to get response. Status: {response.status_code}, Text: {response.text[:200]}")
        break

# Save all collected English reviews
with open("apex_legends_english_reviews.txt", "w", encoding="utf-8") as file:
    for review in all_reviews:
        user_id = review.get("author", {}).get("steamid", "N/A")
        review_text = review.get("review", "No review provided")
        file.write(f"User ID: {user_id}\nReview: {review_text}\n\n")

print(f"Successfully saved {len(all_reviews)} English reviews")