import geopandas as gpd
import pandas as pd

# Your provided mapping
ZONE_NAMES = {
    'CE': 'Commercial Employment', 'CI2': 'Campus Institutional 2',
    'CM1': 'Commercial Mixed Use 1', 'CM2': 'Commercial Mixed Use 2',
    'CM3': 'Commercial Mixed Use 3', 'IR': 'Institutional Residential',
    'OS': 'Open Space', 'R2.5': 'Single-Dwelling Residential 2.5',
    'R5': 'Single-Dwelling Residential 5', 'RM1': 'Residential Multi-Dwelling 1',
    'RM2': 'Residential Multi-Dwelling 2', 'RM4': 'Residential Multi-Dwelling 4'
}

def analyze_humboldt_zoning(file_path):
    try:
        # 1. Load the data
        gdf = gpd.read_file(file_path)
        
        # 2. Identify the zoning column (usually 'ZONING' or 'ZONE')
        # We'll check for 'ZONING' first as it's standard for Humboldt/Portland data
        zoning_col = 'ZONING' if 'ZONING' in gdf.columns else 'ZONE'
        
        if zoning_col not in gdf.columns:
            print(f"Error: Could not find zoning column. Available: {list(gdf.columns)}")
            return

        # 3. Map the shorthand codes to your full names
        # .map() will replace the code with the full name from your dictionary
        gdf['Full_Zone_Name'] = gdf[zoning_col].map(ZONE_NAMES).fillna("Unknown/Other")

        # 4. Filter for names containing "Commercial"
        commercial_df = gdf[gdf['Full_Zone_Name'].str.contains('Commercial', case=False)]

        # 5. Output Results
        total_commercial = len(commercial_df)
        
        print(f"--- Humboldt Commercial Property Analysis ---")
        print(f"Total Commercial Properties found: {total_commercial}")
        print("-" * 45)
        
        if total_commercial > 0:
            # Group by the full name and count
            summary = commercial_df['Full_Zone_Name'].value_counts()
            for name, count in summary.items():
                print(f"{name: <30} | Count: {count}")
        else:
            print("No commercial properties found with the specified mapping.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_humboldt_zoning('Humboldt, Taxlots+Zoning.geojson')