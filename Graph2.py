import pandas as pd
import matplotlib.pyplot as plt
import json

# Load the data
file_name = "Comparison Query.txt"
columns = ["year", "area", "land cover", "agricultural emissions"]
data = pd.read_csv(file_name, names=columns, encoding='latin1')
data.fillna(0, inplace=True)

# Ensure the 'year' column is numeric for filtering
data['year'] = pd.to_numeric(data['year'], errors='coerce')

# Filter data for the specified year (2021)
year_to_compare = 2021
data = data[data['year'] == year_to_compare]

# Load continent data
with open('country-by-continent.json', 'r') as f:
    continent_data = json.load(f)

# Create a dictionary for continent mapping
continent_map = {entry['country']: entry['continent'] for entry in continent_data}

# Map countries to continents based on substring matching
def get_continent(area):
    for country, continent in continent_map.items():
        if country in area:
            return continent
    return "Unknown"

data['continent'] = data['area'].apply(get_continent)

# Print considered countries for each continent
considered_countries = {continent: [] for continent in set(continent_map.values())}
for area in data['area'].unique():
    continent = get_continent(area)
    if continent != "Unknown":
        considered_countries[continent].append(area)
    else:
        print(area)

for continent, countries in considered_countries.items():
    print(f"{continent}: {', '.join(countries)}")

# Calculate averages by continent
continent_averages = data.groupby('continent')[['land cover', 'agricultural emissions']].mean().reset_index()

# Print maximum values for verification
max_land_cover = data['land cover'].max()
max_emissions = data['agricultural emissions'].max()
print(f"Maximum Land Cover: {max_land_cover}")
print(f"Maximum Agricultural Emissions: {max_emissions}")

# Create the bar chart with logarithmic scale
fig, ax1 = plt.subplots(figsize=(10, 6))

x_labels = continent_averages['continent']
bar_width = 0.4

ax1.bar(x_labels, continent_averages['land cover'], width=bar_width, label='Average Land Cover (1000 hectares)', color='blue', align='center')
ax1.set_xlabel('Continent', fontsize=12)
ax1.set_ylabel('Average Land Cover (1000 hectares, Log Scale)', fontsize=12, color='blue')
ax1.set_yscale('log')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.bar(x_labels, continent_averages['agricultural emissions'], width=bar_width, label='Average Emissions (kilotons)', color='orange', align='edge')
ax2.set_ylabel('Average Emissions (kilotons, Log Scale)', fontsize=12, color='orange')
ax2.set_yscale('log')
ax2.tick_params(axis='y', labelcolor='orange')

plt.title(f'Average Land Cover and Emissions by Continent for {year_to_compare} (Logarithmic Scale)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
