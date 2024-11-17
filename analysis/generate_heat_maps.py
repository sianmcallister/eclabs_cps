import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the data
file_path = 'data/Project-Sites_AdHoc-2024-11-11-15-14-28_School_Locations.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path, encoding='latin1')

# Check if the required columns exist
if 'Latitude' not in data.columns or 'Longitude' not in data.columns:
    raise ValueError("The CSV file must contain 'Latitude' and 'Longitude' columns.")

# Create a base map centered around Chicago
chicago_coords = (41.8781, -87.6298)
base_map = folium.Map(location=chicago_coords, zoom_start=11)

# Extract latitude and longitude pairs
lat_lon_pairs = data[['Latitude', 'Longitude']].dropna().values.tolist()

# Add the HeatMap layer
HeatMap(lat_lon_pairs).add_to(base_map)

# Save the map to an HTML file
base_map.save("analysis/chicago_heatmap.html")

print("Heatmap created and saved as 'chicago_heatmap.html'.")