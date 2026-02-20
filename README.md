# GIS & Spatial Analysis Portfolio

**Geographer | Python + GIS | Community-Focused Data Solutions**

## About Me

I'm a geographer with expertise in GIS, spatial analysis, and Python programming. My work focuses on translating complex spatial data into actionable insights for communities, organizations, and decision-makers.

With a PhD in Geography and experience teaching GIS, I combine technical skills with the ability to communicate spatial concepts to diverse audiences. I'm particularly interested in projects at the intersection of:

- Urban planning and community development
- Rural education and equity
- Evidence-based technical assistance
- Open data and civic technology

## Current Focus

Building a portfolio of Python-based GIS projects that demonstrate:

- Interactive web mapping (Folium, Leaflet)
- Spatial data analysis (GeoPandas, pandas)
- Data matching and deduplication workflows
- Workflow automation and reproducible research
- Data visualization for non-technical audiences

## Projects

### 1. Humboldt Neighborhood Business Map

An interactive web map of non-residential properties in Portland's Humboldt Neighborhood, built to support the neighborhood association's business outreach efforts.

**Phase 1: Interactive Map**
- Maps and classifies 396 non-residential properties by zoning type using Portland's open data
- Tools: Python, GeoPandas, Folium, QGIS
- Live Demo: [Interactive Map](https://eichenography.github.io/spatial-analysis-projects/humboldt_businesses_interactive.html)
- Blog Post: [From QGIS to Python: Recreating My Neighborhood Map](https://www.linkedin.com/posts/joshua-eichen_my-neighborhood-needed-to-identify-local-activity-7424470496722972672-nxsV)

**Phase 2: Business Matching & Deduplication**
- Connected 222 verified businesses from Oregon's business registry to neighborhood properties
- Built a modular 3-script pipeline: download → match → deduplicate
- Used fuzzy matching (TheFuzz library) to resolve business name variations and eliminate duplicates
- Live Demo: [Interactive Map](https://eichenography.github.io/spatial-analysis-projects/humboldt_business_map.html)
- Blog Post: [How I Connected 222 Businesses to Our Neighborhood Map](https://www.linkedin.com/pulse/how-i-connected-222-businesses-our-neighborhood-map-joshua-eichen-kdlwe/?trackingId=iHukPRRp7YzRASkWkMxNnA%3D%3D)

**How to Run the Analysis**

The business matching project uses a modular 3-script pipeline. Run in order:

```bash
# 1. Download Oregon business data via API, filtered to neighborhood zipcodes
python humboldt_downloader.py

# 2. Match addresses between tax lots and Oregon business registry
python humboldt_matcher.py

# 3. Deduplicate business names and generate interactive map
python humboldt_deduplicator.py
```

**Files:**
- `humboldt_downloader.py` - Fetch Oregon business registry data via API (zipcodes 97211, 97217)
- `humboldt_matcher.py` - Address-based join of tax lots with Oregon registry; filter to principal places of business
- `humboldt_deduplicator.py` - Fuzzy name matching to eliminate duplicates; outputs interactive Folium map
- `humboldt_business_map.html` - Final interactive map (deployed to GitHub Pages)

**Data Sources:**
- Portland tax lots: [Portland Maps Open Data Portal](https://gis-pdx.opendata.arcgis.com/)
- Oregon business registry: [Oregon Secretary of State Data API](https://data.oregon.gov/resource/tckn-sxa6.json)

---

## Skills

**GIS & Mapping:** QGIS, ArcGIS, Folium, spatial analysis, cartography  
**Programming:** Python (GeoPandas, Folium, pandas, matplotlib, TheFuzz)  
**Data:** Open data, ETL, data cleaning, spatial joins, fuzzy matching, deduplication  
**Communication:** Technical training, data visualization, stakeholder engagement

## Connect

- LinkedIn: [Joshua Eichen](https://www.linkedin.com/in/joshua-eichen/)
- Location: Portland, OR (open to remote work)

---

*This portfolio is actively being developed. New projects added regularly.*
