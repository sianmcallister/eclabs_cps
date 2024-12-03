import pandas as pd
import folium
from folium.plugins import HeatMap

# File paths
schools_file = 'data/Project-Sites_AdHoc-2024-11-11-15-14-28(Geolocations).csv'  # Initial file with School Name, Latitude, and Longitude
counts_file = 'data/Project-Sites_AdHoc-2024-11-11-15-14-28_School_Frequency.csv'    # File with School and Count (frequency)

# Load the data
schools_data = pd.read_csv(schools_file, encoding='latin1')
counts_data = pd.read_csv(counts_file, encoding='latin1')

# Check for required columns in each file
if not {'School', 'Latitude', 'Longitude'}.issubset(schools_data.columns):
    raise ValueError("schools.csv must contain 'School', 'Latitude', and 'Longitude' columns.")
if not {'School', 'Count'}.issubset(counts_data.columns):
    raise ValueError("counts.csv must contain 'School' and 'Count' columns.")

# Merge data on school name
merged_data = pd.merge(
    schools_data,
    counts_data,
    left_on='School',
    right_on='School',
    how='inner'
)

# Prepare data for HeatMap
# Extract latitude, longitude, and count
heat_data = merged_data[['Latitude', 'Longitude', 'Count']].dropna().values.tolist()

# Create a base map centered around Chicago
chicago_coords = (41.8781, -87.6298)
base_map = folium.Map(location=chicago_coords, zoom_start=11)

# Add the HeatMap layer with weights
HeatMap(heat_data).add_to(base_map)

# Save the map to an HTML file
base_map.save("analysis/chicago_heatmap.html")

print("Heatmap with school frequency created and saved as 'chicago_heatmap_with_school_frequency.html'.")