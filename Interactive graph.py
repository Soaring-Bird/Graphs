import pandas as pd

# Load and preprocess the data
file_name = "Comparison Query.txt"
columns = ["year", "area", "land cover", "agricultural emissions"]
data = pd.read_csv(file_name, names=columns, encoding='latin1')
data.fillna(0, inplace=True)

# Generate HTML content
dropdown_options = [{"label": country, "value": country} for country in data['area'].unique()]

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
        #dropdown {{
            width: 50%;
            margin: 20px auto;
            padding: 10px;
        }}
    </style>
</head>
<body>
    <h1>Country Statistics: Land Cover and Agricultural Emissions</h1>
    <select id="dropdown" onchange="updateGraph()">
        <option value="">Select a country</option>
        {''.join([f'<option value="{option["value"]}">{option["label"]}</option>' for option in dropdown_options])}
    </select>
    <div id="plot"></div>
    <script>
        const data = {data.to_json(orient='records')};

        function updateGraph() {{
            const selectedCountry = document.getElementById("dropdown").value;
            const countryData = data.filter(row => row.area === selectedCountry);

            if (countryData.length === 0) {{
                document.getElementById("plot").innerHTML = "<p>Please select a valid country.</p>";
                return;
            }}

            // Extract data
            const years = countryData.map(row => row.year);
            const landCover = countryData.map(row => row['land cover']);
            const emissions = countryData.map(row => row['agricultural emissions']);

            // Format values in "k" or "M" notation for hover labels
            const formatValues = values => values.map(v => {{
                if (v >= 1e6) {{
                    return (v / 1e6).toFixed(2) + 'M'; // Millions
                }} else if (v >= 1e3) {{
                    return (v / 1e3).toFixed(2) + 'k'; // Thousands
                }} else {{
                    return v.toFixed(2); // Plain value
                }}
            }});

            // Format data for display
            const formattedLandCover = formatValues(landCover);
            const formattedEmissions = formatValues(emissions);

            // Define traces
            const landCoverTrace = {{
                x: years,
                y: landCover,
                text: formattedLandCover,
                type: 'bar',
                name: 'Land Cover (1000 hectares)',
                marker: {{ color: 'blue' }},
                hovertemplate: 'Land Cover: %{{text}}<br>Year: %{{x}}<extra></extra>'
            }};

            const emissionsTrace = {{
                x: years,
                y: emissions,
                text: formattedEmissions,
                type: 'bar',
                name: 'Agricultural Emissions (kilotons)',
                marker: {{ color: 'orange' }},
                hovertemplate: 'Emissions: %{{text}}<br>Year: %{{x}}<extra></extra>'
            }};

            // Define layout with logarithmic y-axis
            const layout = {{
                title: `Statistics for ${{selectedCountry}}`,
                xaxis: {{
                    title: 'Year',
                    tickangle: 45,
                    dtick: 1
                }},
                yaxis: {{
                    title: 'Values (Logarithmic Scale)',
                    type: 'log',
                    tickvals: [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000],
                    ticktext: ['1', '10', '100', '1k', '10k', '100k', '1M', '10M']
                }},
                barmode: 'group',
                margin: {{
                    b: 100
                }}
            }};

            // Render the plot
            Plotly.newPlot('plot', [landCoverTrace, emissionsTrace], layout);
        }}
    </script>
</body>
</html>
"""

# Save the HTML file
output_file = "final_v2_logarithmic.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"HTML file saved as {output_file}.")
