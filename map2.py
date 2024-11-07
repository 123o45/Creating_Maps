import folium
import pandas as pd
import json

# Read the CSV file, "r"
data = pd.read_csv("Volcanoes_USA.txt")

# Correct the variable names (lat for latitude, lon for longitude)
lat = list(data["LAT"])  # Latitude
lon = list(data["LON"])  # Longitude
location = list(data["LOCATION"])
elevation = list(data["ELEV"])  # Assuming the file has an elevation column

# Function to determine marker color based on elevation
def color_producer(elev):
    if elev < 1000:
        return "green"
    elif 1000 <= elev < 3000:
        return "orange"
    else:
        return "red"

# Load the GeoJSON file (ensure it's in the correct format with geometries)
with open("world.json", "r", encoding="utf-8-sig") as file:
    geojson_data = json.load(file)

# Create a map centered at a general location
m = folium.Map(location=[38.56, -99.1], zoom_start=6)

# Create a FeatureGroup to add CircleMarkers
fgv = folium.FeatureGroup(name="Volcanoes")

# Loop through the coordinates and add them as CircleMarkers on the map
for lt, ln, el, lo in zip(lat, lon, elevation, location):
    fgv.add_child(folium.CircleMarker(
        location=[lt, ln],
        radius=10,  # Set the size of the circle
        popup=str(lo) + " - " + str(el) + "m",
        color="grey",  # Border color of the circle
        fill=True,  # Enable filling the circle with color
        fill_color=color_producer(el),  # Use the color from the function
        fill_opacity=0.5  # Transparency of the fill color
    ))

fgp = folium.FeatureGroup(name="Population")

# Add GeoJson with conditional population-based coloring
fgp.add_child(folium.GeoJson(
    data=geojson_data,
    style_function=lambda x: {
        'fillColor': 'yellow' if x['properties'].get('pop2010', 0) < 10000000 
        else 'orange' if 10000000 <= x['properties'].get('pop2010', 0) < 50000000 
        else 'red'
    }
))

# Add the feature groups to the map
m.add_child(fgv)
m.add_child(fgp)

# Add LayerControl to toggle layers
m.add_child(folium.LayerControl())

# Save the map
m.save("map.html")
