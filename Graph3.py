import pandas as pd
import json
import plotly.graph_objects as go

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

# Define tick values and labels for the y-axis (log scale)
tickvals = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000, 20000000, 50000000, 100000000, 200000000, 500000000, 1000000000, 2000000000, 5000000000, 10000000000]
ticktext = ['1', '2', '5', '10', '20', '50', '100', '200', '500', '1000', '2000', '5000', '10⁴', '2×10⁴', '5×10⁴', '10⁵', '2×10⁵', '5×10⁵', '10⁶', '2×10⁶', '5×10⁶', '10⁷', '2×10⁷', '5×10⁷', '10⁸', '2×10⁸', '5×10⁸', '10⁹', '2×10⁹', '5×10⁹', '10¹⁰']

# Create the interactive plot
fig = go.Figure()

# Function to generate the plot for the selected year
def update_graph(year):
    filtered_data = data[data['year'] == year]
    continent_averages = filtered_data.groupby('continent')[['land cover', 'agricultural emissions']].mean().reset_index()
    
    # Add bar for land cover
    fig.add_trace(go.Bar(
        x=continent_averages['continent'],
        y=continent_averages['land cover'],
        name='Average Land Cover (1000 hectares)',
        text=continent_averages['land cover'],
        textposition='auto',
        marker_color='blue'
    ))

    # Add bar for agricultural emissions
    fig.add_trace(go.Bar(
        x=continent_averages['continent'],
        y=continent_averages['agricultural emissions'],
        name='Average Emissions (kilotons)',
        text=continent_averages['agricultural emissions'],
        textposition='auto',
        marker_color='orange'
    ))

    fig.update_layout(
        title=f'Average Land Cover and Emissions by Continent for {year}',
        xaxis_title='Continent',
        yaxis_title='Values (Logarithmic Scale)',
        yaxis=dict(
            type='log', 
            tickvals=tickvals,
            ticktext=ticktext
        ),
        barmode='group',
        hovermode='x unified'
    )

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
    <h1>Average Land Cover and Emissions by Continent</h1>
    
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

            var continentAverages = aggregateDataByContinent(filteredData);
            updatePlot(continentAverages);
        }}

        function aggregateDataByContinent(data) {{
            var continentAverages = {{}};
            data.forEach(function(row) {{
                var continent = row.continent;
                if (!continentAverages[continent]) {{
                    continentAverages[continent] = {{landCover: 0, emissions: 0, count: 0}};
                }}
                continentAverages[continent].landCover += row['land cover'];
                continentAverages[continent].emissions += row['agricultural emissions'];
                continentAverages[continent].count += 1;
            }});

            // Calculate averages
            for (var continent in continentAverages) {{
                continentAverages[continent].landCover /= continentAverages[continent].count;
                continentAverages[continent].emissions /= continentAverages[continent].count;
            }}
            return continentAverages;
        }}

        function updatePlot(continentAverages) {{
            var x = [];
            var landCover = [];
            var emissions = [];
            for (var continent in continentAverages) {{
                x.push(continent);
                landCover.push(continentAverages[continent].landCover);
                emissions.push(continentAverages[continent].emissions);
            }}
            
            var landCoverTrace = {{
                x: x,
                y: landCover,
                type: 'bar',
                name: 'Average Land Cover (1000 hectares)',
                marker: {{ color: 'blue' }}
            }};

            var emissionsTrace = {{
                x: x,
                y: emissions,
                type: 'bar',
                name: 'Average Emissions (kilotons)',
                marker: {{ color: 'orange' }}
            }};

            Plotly.newPlot('plot', [landCoverTrace, emissionsTrace]);
        }}

        // Initialize the graph with the default year
        updateGraph();
    </script>
</body>
</html>
"""

# Save the HTML file
output_file = "interactive_graph_with_dropdown_1992_onwards.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Interactive graph saved as {output_file}.")
