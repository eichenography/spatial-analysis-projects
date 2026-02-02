import geopandas as gpd
import folium
from folium.plugins import Search

# 1. Setup Data and Colors
ZONE_NAMES = {
    'CE': 'Commercial Employment', 'CI2': 'Campus Institutional 2',
    'CM1': 'Commercial Mixed Use 1', 'CM2': 'Commercial Mixed Use 2',
    'CM3': 'Commercial Mixed Use 3', 'IR': 'Institutional Residential',
    'OS': 'Open Space', 'R2.5': 'Single-Dwelling Residential 2.5',
    'R5': 'Single-Dwelling Residential 5', 'RM1': 'Residential Multi-Dwelling 1',
    'RM2': 'Residential Multi-Dwelling 2', 'RM4': 'Residential Multi-Dwelling 4'
}

zoning_colors = {
    'CE': '#fccde5', 'CI2': '#fb8072', 'CM1': '#8dd3c7', 'CM2': '#ffffb3',
    'CM3': '#bebada', 'IR': '#bc80bd', 'OS': '#33a02c', 'R2.5': '#ffed6f',
    'R5': '#fdb462', 'RM1': '#b3de69', 'RM2': '#ccebc5', 'RM4': '#6a3d9a'
}

# Load data
data = gpd.read_file('Humboldt, Taxlots+Zoning.geojson').to_crs(epsg=4326)
data['ZONE_FULL'] = data['ZONE'].map(ZONE_NAMES).fillna('Other')
data['OWNER1'] = data['OWNER1'].fillna('Unknown Owner')

# 2. Base Map
m = folium.Map(location=[45.560, -122.668], zoom_start=15, tiles='CartoDB positron')

# 3. Create Layers with Hover Tooltips
available_zones = sorted(data['ZONE'].unique())
for code in available_zones:
    full_name = ZONE_NAMES.get(code, code)
    feat_group = folium.FeatureGroup(name=full_name, overlay=True).add_to(m)
    
    folium.GeoJson(
        data[data['ZONE'] == code],
        style_function=lambda feature, color=zoning_colors.get(code): {
            'fillColor': color, 'color': 'black', 'weight': 0.5, 'fillOpacity': 0.7
        },
        # OWNER1 is now in the Tooltip (Hover) instead of Popup (Click)
        tooltip=folium.GeoJsonTooltip(
            fields=['SITEADDR', 'OWNER1', 'ZONE_FULL'], 
            aliases=['Address:', 'Owner:', 'Zoning:'],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """
        )
    ).add_to(feat_group)

# 4. Custom Legend HTML & JS
legend_items = "".join([
    f'''<div class="legend-item" onclick="toggleLayer('{ZONE_NAMES.get(code, code)}')" style="cursor: pointer; margin-bottom: 5px;">
        <span style="background-color: {zoning_colors.get(code, '#ccc')}; width: 15px; height: 15px; display: inline-block; border: 1px solid black; vertical-align: middle;"></span>
        <span style="vertical-align: middle; margin-left: 5px;">{ZONE_NAMES.get(code, code)}</span>
    </div>''' for code in available_zones
])

legend_html = f'''
<div id="clickable-legend" style="position: fixed; bottom: 30px; right: 30px; width: 260px; 
    background: white; padding: 10px; border: 2px solid grey; z-index: 9999; border-radius: 8px; font-family: sans-serif; font-size: 12px;">
    <h4 style="margin: 0 0 10px 0;">Humboldt Zoning (Toggle)</h4>
    {legend_items}
</div>
'''

js_code = """
<script>
function toggleLayer(layerName) {
    var layers = document.querySelectorAll('.leaflet-control-layers-overlays label');
    for (var i = 0; i < layers.length; i++) {
        if (layers[i].innerText.trim() === layerName) {
            layers[i].click();
            break;
        }
    }
}
</script>
"""

m.get_root().html.add_child(folium.Element(legend_html))
m.get_root().html.add_child(folium.Element(js_code))
folium.LayerControl(collapsed=True).add_to(m)

m.save('humboldt_hover_owners.html')
print("Map saved! You can now hover over properties to see Owner info.")