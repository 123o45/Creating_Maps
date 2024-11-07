import folium
import pandas as pd
import json

data = pd.read_csv("Volcanoes_USA.txt")

lat = list(data["LAT"])  # Latitude
lon = list(data["LON"])  # Longitude
location = list(data["LOCATION"])
elevation = list(data["ELEV"])

def color_producer(elev):
    if elev < 1000:
        return "green"
    elif 1000 <= elev < 3000:
        return "orange"
    else:
        return "red"
    
with open("world.json", "r", encoding="utf-8-sig") as file:
    geojson_data = json.load(file)

m = folium.Map(location=[38.56, -99.1], zoom_start=6)

fgv = folium.FeatureGroup(name="volcanouse")

for lt, ln, el, lo in zip(lat, lon, elevation, location):
    fgv.add_child(folium.CircleMarker(
        location=[lt, ln],
        radius=10,  # Set the size of the circle
        popup=str(lo) + " - " + str(el) + "m",
        color="grey",  # Border color of the circle
        fill=True,  # Enable filling the circle with color
        fill_color=color_producer(el),  # Use the color from the function
        fill_opacity= 0.5))
    
fgp = folium.FeatureGroup(name="population")


fgp.add_child(folium.GeoJson(data=geojson_data, 
                            style_function=lambda x: {
                                "fillColor": "yellow" if x["properties"].get("POP2005", 0) < 10000000 
                                else "orange" if 10000000 <= x["properties"].get("POP2005", 0) < 50000000 
                                else "red"
                            },
                            # Add a tooltip to display the country name and population
                            tooltip=folium.GeoJsonTooltip(fields=["NAME", "POP2005"], aliases=["Country", "Population 2005"])
                            ))

m.add_child(fgv)
m.add_child(fgp)

m.add_child(folium.LayerControl())
# Save the map
m.save("map.html")
