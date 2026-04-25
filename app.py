import streamlit as st
import requests
import re

# MUST BE THE FIRST COMMAND!
st.set_page_config(page_title="Live Price Aggregator", page_icon="⚡")

# ==========================================
# 1. THE ENGINE (Backend Logic)
# ==========================================
def fetch_live_prices(product_name):
    # PASTE YOUR SERPAPI KEY HERE
    API_KEY = st.secrets["SERPAPI_KEY"] 
    
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "gl": "in",      # Country: India
        "hl": "en",      # Language: English
        "api_key": API_KEY
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("shopping_results", [])
    return []

def clean_price_string(price_str):
    """
    Converts messy strings like '₹1,50,000.00' into a clean float '150000.00' 
    so the computer can do math on it.
    """
    try:
        # Removes everything except numbers and decimals
        clean_num = re.sub(r'[^\d.]', '', str(price_str))
        return float(clean_num)
    except:
        return float('inf') # If there's an error, make it artificially high so it doesn't win

# ==========================================
# 2. THE SHOWCASE (Frontend UI)
# ==========================================
st.title("⚡ Live Price Aggregator")
st.markdown("Search across Amazon, Flipkart, Croma, and more in real-time.")

# The Search Bar
user_query = st.text_input("What do you want to buy? (e.g., 'Oats', 'iPhone 15')")

if st.button("Find Lowest Price", type="primary") and user_query:
    
    # st.spinner shows a cool loading animation while waiting for the internet
    with st.spinner(f"Scouring the internet for {user_query}..."):
        
        # 1. Fetch the data
        results = fetch_live_prices(user_query)
        
        if not results:
            st.error("No results found or the API limit was reached.")
        else:
            # 2. Find the absolute lowest price
            best_item = None
            lowest_price = float('inf')
            
            # 3. Clean prices and filter
            valid_items = []
            for item in results:
                raw_price = item.get("price", "")
                num_price = clean_price_string(raw_price)
                
                # If the price is valid, add it to our list
                if num_price < float('inf'):
                    item['numeric_price'] = num_price
                    valid_items.append(item)
                    
                    # Update the winner if this is the lowest we've seen
                    if num_price < lowest_price:
                        lowest_price = num_price
                        best_item = item
            
            # 4. Display the Winner!
            if best_item:
                st.success("🎯 True Best Deal Found!")
                
                # We use columns to make it look like a dashboard
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label=f"Winner: {best_item.get('source')}", value=f"₹{best_item['numeric_price']:,.2f}")
                with col2:
                    st.write(f"**Product:** {best_item.get('title')}")
                    
                    # 1. Try to get the direct store link, fallback to Google's product link
                    store_link = best_item.get('link')
                    if not store_link:
                        store_link = best_item.get('product_link', 'https://google.com/shopping')
                    
                    # 2. Use Streamlit's native button instead of Markdown
                    st.link_button(f"🛒 Buy Now at {best_item.get('source')}", store_link)
                st.divider()
                
                # 5. Display the runner-ups
                st.write("### Compare Other Live Offers:")
                
                # Create a simple table for the rest of the items
                comparison_data = []
                for item in valid_items:
                    comparison_data.append({
                        "Store": item.get('source'),
                        "Price": f"₹{item['numeric_price']:,.2f}",
                        "Product Name": item.get('title')
                    })
                
                st.dataframe(comparison_data, use_container_width=True)