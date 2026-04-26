import requests
import json

def fetch_live_prices(product_name):
    # 1. Your API Key goes here
    API_KEY = "5da0a19ae73fd392a7f438094f03c8193624a42c777e53eae643a14560d26f1a" 
    
    # 2. We set up the parameters for the API. 
    # engine: google_shopping (where we want to search)
    # gl: 'in' (Country: India)
    # hl: 'en' (Language: English)
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "gl": "in",
        "hl": "en",
        "api_key": API_KEY
    }

    print(f"📡 Sending request to SerpApi for '{product_name}'...")
    
    # 3. Make the actual request to the internet
    response = requests.get("https://serpapi.com/search", params=params)
    
    # 4. Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Google Shopping results are stored in the 'shopping_results' list
        if "shopping_results" in data:
            results = data["shopping_results"]
            print(f"✅ Found {len(results)} items!")
            
            # 5. Let's print out the top 5 results to see what they look like
            print("-" * 40)
            for item in results[:5]: 
                title = item.get("title", "No Title")
                price = item.get("price", "No Price")
                store = item.get("source", "Unknown Store")
                print(f"Store: {store} | Price: {price}")
                print(f"Product: {title[:60]}...") # Limit title length for easy reading
                print("-" * 40)
        else:
            print("⚠️ The API worked, but no shopping results were found for this item.")
    else:
        print(f"❌ API Error: {response.status_code}")
        print("Check your API key!")

# ==========================================
# TEST THE ENGINE
# ==========================================
if __name__ == "__main__":
    # Let's test it with a generic product
    fetch_live_prices("Sony WH-1000XM4 headphones")