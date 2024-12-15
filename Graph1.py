import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
file_name = "Comparison Query.txt"
columns = ["year", "area", "land cover", "agricultural emissions"]
data = pd.read_csv(file_name, names=columns, encoding='latin1')

# Clean data by filling missing values if necessary
data.fillna(0, inplace=True)

# Debug: Print maximum values in the dataset for verification
print("Maximum Land Cover:", data['land cover'].max())
print("Maximum Agricultural Emissions:", data['agricultural emissions'].max())

# Find global maximum values for fixed scaling
max_land_cover = data['land cover'].max()  # Raw values for land cover
max_emissions = data['agricultural emissions'].max()  # Raw values for emissions

# Directory to save plots
output_dir = "Country_Graphs_Updated"
os.makedirs(output_dir, exist_ok=True)

def save_country_comparison_plot(country):
    # Filter data for the specified country
    country_data = data[data['area'] == country]
    
    if country_data.empty:
        print(f"No data found for {country}")
        return

    # Create the plot
    x_labels = country_data['year'].astype(int).astype(str)
    bar_width = 0.4
    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Primary axis for land cover with logarithmic scale
    ax1.bar(x_labels, country_data['land cover'], width=bar_width, label='Land Cover (1000 hectares)', color='blue', align='center')
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Land Cover (1000 hectares)', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_yscale('log')  # Apply logarithmic scale for land cover
    ax1.set_ylim(1, max_land_cover)  # Avoid 0 for logarithmic scale

    # Secondary axis for emissions with logarithmic scale
    ax2 = ax1.twinx()
    ax2.bar(x_labels, country_data['agricultural emissions'], width=bar_width, label='Emissions (kilotons)', color='orange', align='edge')
    ax2.set_ylabel('Emissions (kilotons)', fontsize=12, color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.set_yscale('log')  # Apply logarithmic scale for emissions
    ax2.set_ylim(1, max_emissions)  # Avoid 0 for logarithmic scale

    # Add title and adjust x-axis ticks
    plt.title(f'Comparison of Land Cover and Emissions in {country}', fontsize=14)
    ax1.set_xticks(range(len(x_labels)))
    ax1.set_xticklabels(x_labels, rotation=45, ha='right')
    fig.tight_layout()

    # Save plot to file
    output_path = os.path.join(output_dir, f"{country}_comparison.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot for {country} at {output_path}")

# Batch processing for all unique countries
countries = data['area'].unique()
for country in countries:
    save_country_comparison_plot(country)

