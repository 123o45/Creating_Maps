import json
import pandas as pd

# Open and read the JSON file
with open("world.json", "r") as file:
    content = file.read()  # Read the raw file content

# Print the raw content to verify if it's empty or malformed
#print(content)
world_data = json.loads(content) 
df = pd.read_json(world_data)
df.head()

# Now try loading the JSON content
try:
    world_data = json.loads(content)  # Load JSON from the string content
    df = pd.read_json(content)
    df.head()
    #print(world_data[0])  # Print the first object if it's an array
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")

