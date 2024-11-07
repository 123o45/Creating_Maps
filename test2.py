import json

# Load both JSON files
with open("world.json", "r") as world_file:
    world_data = json.load(world_file)

with open("Downloading-Data/population_data.json", "r") as population_file:
    population_data = json.load(population_file)

# Create a dictionary to store population data (assuming country name as the key)
population_dict = {entry['country']: entry['population'] for entry in population_data}

# Compare population values
for country in world_data:
    world_country_name = country.get('name')
    world_population = country.get('population')
    
    # Check if the country exists in population_data.json
    if world_country_name in population_dict:
        pop_data_population = population_dict[world_country_name]
        
        if world_population != pop_data_population:
            print(f"Population mismatch for {world_country_name}:")
            print(f"world.json population: {world_population}")
            print(f"population_data.json population: {pop_data_population}")
    else:
        print(f"{world_country_name} not found in population_data.json.")

