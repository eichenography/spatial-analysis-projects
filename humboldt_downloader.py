import requests
import json
import os
import urllib.parse

def save_portland_subset(output_path='Data/portland_business_subset.json'):
    base_url = "https://data.oregon.gov/resource/tckn-sxa6.json"
    
    # Using your specific parameters
    params = {
        "$where": "city='PORTLAND' AND zip IN('97211', '97217')", 
        "$limit": 50000 # Set slightly higher than your limit to ensure we catch everything
    }
    
    encoded_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    print(f"--- Downloading Portland Subset (97211, 97217) ---")
    
    try:
        response = requests.get(encoded_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f)
            
        print(f"SUCCESS: Saved {len(data)} records to {output_path}")
        
    except Exception as e:
        print(f"Failed to download: {e}")

if __name__ == "__main__":
    save_portland_subset()