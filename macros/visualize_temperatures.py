import os
import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PW = os.getenv('POSTGRES_PW')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
DB_CLIMATE = os.getenv('DB_CLIMATE')

# Create the database engine
engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_CLIMATE}')

# Query to import the table with average temperatures
query = """
SELECT location_id, region, country, week_start, avg_temperature, latitude, longitude
FROM mart_conditions_week
"""

# Load the data into a DataFrame
df = pd.read_sql_query(query, engine)

# Filter data for Berlin
df_berlin = df[df['region'] == 'Berlin']

# Create an interactive bar plot for Berlin
fig = px.bar(df_berlin, x='week_start', y='avg_temperature', title='Average Weekly Temperatures in Berlin', labels={'week_start': 'Week Start', 'avg_temperature': 'Average Temperature (°C)'})
fig.show()

# Create an interactive line chart for Berlin
fig_line = px.line(df_berlin, x='week_start', y='avg_temperature', title='Average Weekly Temperatures in Berlin', labels={'week_start': 'Week Start', 'avg_temperature': 'Average Temperature (°C)'})
fig_line.show()

# Create interactive plots for all locations
fig_all = px.line(df, x='week_start', y='avg_temperature', color='region', title='Average Weekly Temperatures by Location', labels={'week_start': 'Week Start', 'avg_temperature': 'Average Temperature (°C)', 'region': 'Location'})
fig_all.show()

# Experiment with other visualization types
fig_scatter = px.scatter(df, x='week_start', y='avg_temperature', color='region', title='Average Weekly Temperatures by Location (Scatter Plot)', labels={'week_start': 'Week Start', 'avg_temperature': 'Average Temperature (°C)', 'region': 'Location'})
fig_scatter.show()

# Optional: Save the plots as HTML files
fig.write_html("berlin_avg_temp_bar.html")
fig_line.write_html("berlin_avg_temp_line.html")
fig_all.write_html("all_locations_avg_temp_line.html")
fig_scatter.write_html("all_locations_avg_temp_scatter.html")

print("Plots created and saved as HTML files.")
