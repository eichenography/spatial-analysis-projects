import pandas as pd
from thefuzz import fuzz
import os
import re
import folium
import json
from pyproj import Transformer

def clean_name(text):
    text = str(text).upper()
    text = re.sub(r'\b(LLC|INC|CORP|HOLDCO|LTD|CO|CORPORATION|INCORPORATED)\b', '', text)
    return text.strip()

def generate_map(df, map_path, geojson_path=None):
    if 'y' not in df.columns or 'x' not in df.columns:
        print("Skipping Map: 'x' or 'y' columns not found.")
        return

    map_data = df.dropna(subset=['x', 'y'])
    if map_data.empty:
        print("Skipping Map: No valid coordinate data found.")
        return
    
    start_coords = [map_data['y'].mean(), map_data['x'].mean()]
    m = folium.Map(location=start_coords, zoom_start=14)

    if geojson_path and os.path.exists(geojson_path):
        with open(geojson_path, 'r') as f:
            boundary_data = json.load(f)
        
        folium.GeoJson(
            boundary_data,
            name="Humboldt Boundary",
            style_function=lambda x: {'fillColor': '#3186cc', 'color': 'black', 'weight': 2, 'fillOpacity': 0.1}
        ).add_to(m)

    for _, row in map_data.iterrows():
        name = str(row.get('business_name', 'Unknown')).replace("'", "\\'")
        address = str(row.get('address', 'N/A')).replace("'", "\\'")
        obj_id = str(row.get('OBJECTID', 'N/A'))
        
        popup_text = f"<b>{name}</b><br>{address}<br>ID: {obj_id}"
        folium.Marker(
            location=[row['y'], row['x']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=name
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(map_path)

def process_business_matches(input_path, output_path, map_path, geojson_path=None):
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return

    df = pd.read_csv(input_path)
    df.columns = [c.strip() for c in df.columns]

    transformer = Transformer.from_crs("EPSG:2913", "EPSG:4326", always_xy=True)

    def convert_coords(row):
        try:
            lon, lat = transformer.transform(row['X'], row['Y'])
            return pd.Series({'x': lon, 'y': lat})
        except:
            return pd.Series({'x': None, 'y': None})

    print("Converting coordinates...")
    coords = df.apply(convert_coords, axis=1)
    df['x'] = coords['x']
    df['y'] = coords['y']

    df['business_name'] = df['business_name'].fillna('').astype(str)
    df['entity_type'] = df['entity_type'].fillna('').astype(str)
    df['address'] = df['address'].fillna('').astype(str)
    
    final_results = []
    change_log = [] # Track modifications
    
    for obj_id, group in df.groupby('OBJECTID'):
        unique_for_this_id = []
        for _, row in group.iterrows():
            name = row['business_name'].strip()
            name_u = name.upper()
            name_clean = clean_name(name_u)
            e_type = row['entity_type'].strip().upper()
            addr = row['address']
            
            matched = False
            for entry in unique_for_this_id:
                entry_u = entry['business_name'].upper()
                entry_clean = clean_name(entry_u)
                
                prefix_match = name_clean[:8] == entry_clean[:8] and len(name_clean) >= 8
                fuzz_ratio = fuzz.token_set_ratio(name_u, entry_u)
                
                if prefix_match or fuzz_ratio > 85:
                    matched = True
                    print(f"\n[MATCH DETECTED] ID: {obj_id} | ADDRESS: {addr}")
                    print(f"  1) [DEFAULT] Keep Original: {entry['business_name']}")
                    print(f"  2) Accept Suggested:     {name}")
                    
                    choice = input("Select 1, 2, or type custom (Enter for 1): ").strip()
                    
                    original_val = entry['business_name']
                    if choice == "2":
                        entry['business_name'] = name
                        change_log.append({'id': obj_id, 'from': original_val, 'to': name, 'addr': addr})
                    elif choice != "" and choice != "1":
                        entry['business_name'] = choice
                        change_log.append({'id': obj_id, 'from': original_val, 'to': choice, 'addr': addr})
                    break
            
            if not matched:
                unique_for_this_id.append({
                    'business_name': name, 
                    'address': addr,
                    'OBJECTID': obj_id, 
                    'entity_type': e_type, 
                    'x': row['x'], 
                    'y': row['y']
                })
        final_results.extend(unique_for_this_id)

    # Export Logic
    output_df = pd.DataFrame(final_results)
    if 'entity_type' in output_df.columns:
        output_df = output_df.drop(columns=['entity_type'])

    output_df.to_csv(output_path, index=False)
    generate_map(output_df, map_path, geojson_path)
    
    # Final Reporting
    print("\n" + "="*60)
    print("   PROCESSING COMPLETE")
    print("="*60)
    
    if change_log:
        print(f"{'ID':<8} | {'ADDRESS':<25} | {'CHANGES MADE'}")
        print("-" * 60)
        for c in change_log:
            print(f"{c['id']:<8} | {c['addr'][:25]:<25} | {c['from']} -> {c['to']}")
    else:
        print("No name changes were made.")
        
    print("-" * 60)
    print(f"Reduced {len(df)} rows to {len(output_df)} entries.")
    print(f"Final CSV: {output_path}")
    print("="*60 + "\n")

if __name__ == "__main__":
    input_file = 'Data/humboldt_commercial_matches.csv'
    output_file = 'Data/humboldt_final_deduplicated.csv'
    map_file = 'humboldt_business_map.html'
    boundary_file = 'Data/HUMBOLDT Boundary.geojson'
    
    process_business_matches(input_file, output_file, map_file, boundary_file)