import geopandas as gpd
import pandas as pd
import json
import os
import re

# Configuration
WHITELIST_ZONES = ['CM1', 'CM2', 'CM3']
NEIGHBORHOOD_ADDRESSES = 'Data/Humboldt Addresses, with Zoning.geojson'
BUSINESS_LICENSES = 'Data/portland_business_subset.json'
OUTPUT_CSV = 'Data/humboldt_commercial_matches.csv'

def ultra_clean(s):
    if not s or pd.isna(s): return ""
    s = str(s).upper().replace('NAN', '')
    s = re.sub(r'\b(STE|UNIT|APT|SUITE|BLDG|RM|#|PO BOX|BOX)\b.*', '', s)
    s = re.sub(r'\b(NORTH|SOUTH|EAST|WEST|N|S|E|W|NE|NW|SE|SW)\b', '', s)
    s = re.sub(r'\b(AVE|AVENUE|ST|STREET|RD|ROAD|BLVD|BOULEVARD|LN|LANE|PL|PLACE|CT|COURT|DR|DRIVE)\b', '', s)
    s = re.sub(r'(\d+)(ST|ND|RD|TH)', r'\1', s)
    s = re.sub(r'[^A-Z0-9\s]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def run_neighborhood_commercial_analysis():
    try:
        # --- Step 1: Load Local Data ---
        gdf = gpd.read_file(NEIGHBORHOOD_ADDRESSES)
        cm_gdf = gdf[gdf['ZONE'].isin(WHITELIST_ZONES)].copy()

        # --- Step 2: Load State Data & Filter for Principal Place ---
        with open(BUSINESS_LICENSES, 'r') as f:
            state_data_raw = pd.DataFrame(json.load(f))
        
        # Filter strictly for Principal Place of Business
        state_data = state_data_raw[state_data_raw['associated_name_type'] == 'PRINCIPAL PLACE OF BUSINESS'].copy()

        # --- Step 3: Clean & Match ---
        cm_gdf['match_key'] = cm_gdf['ADD_FULL'].apply(ultra_clean)
        
        state_data['address'] = state_data.get('address', '').fillna('')
        state_data['address_continued'] = state_data.get('address_continued', '').fillna('')
        state_data['match_key'] = (state_data['address'] + " " + state_data['address_continued']).apply(ultra_clean)

        # Merge
        merged = cm_gdf.merge(state_data, on='match_key', how='left', indicator=True)
        
        # --- Step 4: Save Matches to CSV ---
        successful_matches = merged[merged['_merge'] == 'both'].copy()
        if not successful_matches.empty:
            df_export = pd.DataFrame(successful_matches.drop(columns=['geometry', '_merge'], errors='ignore'))
            df_export.to_csv(OUTPUT_CSV, index=False)

        # --- Step 5: Updated Command Line Output ---
        total_in_subset = len(state_data_raw)
        local_addresses = len(cm_gdf)
        principal_count = len(successful_matches)

        print("\n" + "="*50)
        print("   HUMBOLDT BUSINESS MATCH REPORT")
        print("="*50)
        print(f"BUSINESSES IN SUBSET:            {total_in_subset}")
        print(f"LOCAL ADDRESSES IN WHITEZONES:   {local_addresses}")
        print(f"PRINCIPAL PLACE OF BUSINESSES:   {principal_count}")
        print("="*50)
        
        # Keeping original zone table for context
        zone_counts_total = cm_gdf['ZONE'].value_counts()
        zone_counts_matched = successful_matches.drop_duplicates('match_key')['ZONE'].value_counts()
        
        print(f"\n{'ZONE':<10} | {'TOTAL ADDR':<12} | {'PRINCIPAL MATCH':<10}")
        print("-" * 45)
        for zone in WHITELIST_ZONES:
            total = zone_counts_total.get(zone, 0)
            matched = zone_counts_matched.get(zone, 0)
            print(f"{zone:<10} | {total:<12} | {matched:<10}")
        
        if not successful_matches.empty:
            print(f"\n[FILE SAVED]: {OUTPUT_CSV}")
        print("="*50 + "\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_neighborhood_commercial_analysis()