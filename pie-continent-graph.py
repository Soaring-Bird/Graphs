import pandas as pd
import json

# Load the data
file_name = "Comparison Query.txt"
columns = ["year", "area", "land cover", "agricultural emissions"]
data = pd.read_csv(file_name, names=columns, encoding='latin1')
data.fillna(0, inplace=True)

# Ensure the 'year' column is numeric for filtering
data['year'] = pd.to_numeric(data['year'], errors='coerce')

# Filter data for years from 1992 onwards
data = data[data['year'] >= 1992]

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

# Identify and print unknown countries
unknown_countries = data[data['continent'] == "Unknown"]['area'].unique()
if len(unknown_countries) > 0:
    print("Countries categorized as 'Unknown':")
    for country in unknown_countries:
        print(f"- {country}")
else:
    print("No unknown countries found.")

# HTML structure with dropdown and JavaScript to handle the interaction
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
        }}
        #year-dropdown {{
            margin: 20px;
            padding: 10px;
        }}
    </style>
</head>
<body>
    <h1>Average Agricultural Emissions by Continent (% of global)</h1>
    
    <!-- Dropdown for year selection -->
    <select id="year-dropdown" onchange="updateGraph()">
        {"".join([f'<option value="{int(year)}">{int(year)}</option>' for year in sorted(data['year'].unique())])}
    </select>

    <div id="plot"></div>

    <script>
        var data = {data.to_json(orient='records')};

        function updateGraph() {{
            var selectedYear = parseInt(document.getElementById("year-dropdown").value);
            var filteredData = data.filter(function(row) {{
                return row.year == selectedYear;
            }});

            var continentEmissions = aggregateEmissionsByContinent(filteredData);
            updatePieChart(continentEmissions, selectedYear);
        }}

        function aggregateEmissionsByContinent(data) {{
            var emissionsByContinent = {{}};
            data.forEach(function(row) {{
                var continent = row.continent;
                if (!emissionsByContinent[continent]) {{
                    emissionsByContinent[continent] = 0;
                }}
                emissionsByContinent[continent] += row['agricultural emissions'];
            }});
            return emissionsByContinent;
        }}

        function updatePieChart(emissionsByContinent, year) {{
            var labels = [];
            var values = [];
            for (var continent in emissionsByContinent) {{
                labels.push(continent);
                values.push(emissionsByContinent[continent]);
            }}
            
            var pieTrace = {{
                labels: labels,
                values: values,
                type: 'pie',
                textinfo: 'label+percent',
                hoverinfo: 'label+value',
                textposition: 'outside',
                insidetextorientation: 'horizontal',
                automargin: true
            }};

            var layout = {{
                margin: {{ l: 40, r: 40, t: 40, b: 40 }},
                showlegend: true
            }};

            Plotly.newPlot('plot', [pieTrace], layout);
        }}

        // Initialize the graph with the default year
        updateGraph();
    </script>
</body>
</html>
"""

# Save the HTML file
output_file = "interactive_pie_chart_with_adjusted_labels.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Interactive pie chart saved as {output_file}.")
