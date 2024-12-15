import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# Load the data
file_name = "Comparison Query.txt"
columns = ["year", "area", "land cover", "agricultural emissions"]
data = pd.read_csv(file_name, names=columns, encoding='latin1')

# Load population data from JSON
population_file = "country-by-population.json"
with open(population_file, 'r') as f:
    population_data = json.load(f)

# Convert JSON data to DataFrame
population_df = pd.DataFrame(population_data)  # Assumes keys: "country" and "population"
population_df.rename(columns={'country': 'area'}, inplace=True)

# Merge population data with emissions and land cover data
data = pd.merge(data, population_df, on='area', how='left')

# Filter data for the year 2021
data['year'] = pd.to_numeric(data['year'], errors='coerce')
data_2021 = data[data['year'] == 2021]

# Clean data by filling missing values
for col in ['land cover', 'agricultural emissions', 'population']:
    data_2021[col] = data_2021[col].fillna(0)

# Directory to save plots
output_dir = "Country_Horizontal_Bar_Graphs_2021"
os.makedirs(output_dir, exist_ok=True)

def save_country_horizontal_bar_plot(country):
    # Filter data for the specified country
    country_data = data_2021[data_2021['area'] == country]

    if country_data.empty:
        print(f"No data found for {country}")
        return

    # Extract values for the plot
    land_cover = country_data['land cover'].values[0]
    emissions = country_data['agricultural emissions'].values[0]
    population = country_data['population'].values[0]

    # Data and labels
    values = [land_cover, emissions, population]
    labels = ['Land Cover (1000 hectares)', 'Agricultural Emissions (kilotons)', 'Population']
    colors = ['blue', 'orange', 'green']

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(labels, values, color=colors)

    # Add value labels to bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:,.2f}', va='center', ha='left', fontsize=10)

    # Set axis labels and title
    ax.set_xlabel('Values', fontsize=12)
    ax.set_title(f'Comparison of Land Cover, Emissions, and Population in {country} (2021)', fontsize=14)
    plt.tight_layout()

    # Save plot to file
    output_path = os.path.join(output_dir, f"{country}_comparison_2021.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot for {country} at {output_path}")

# Batch processing for all unique countries
countries = data_2021['area'].unique()
for country in countries:
    save_country_horizontal_bar_plot(country)
