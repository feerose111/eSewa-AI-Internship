from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
df = pd.read_csv('processed_retail_data.csv')
gdf = gpd.read_file('city_spend.geojson')

#-------------------figure-section-----------------------------------------------
grouped_df = df.groupby(['Age', 'Gender'], as_index=False)['Avg_Spend'].sum()
# Create initial figure
fig1 = px.bar(grouped_df, x='Age', y='Avg_Spend', color='Gender', color_discrete_sequence=px.colors.qualitative.Bold,
       barmode='group',
       title='Sum Of Spending By Age'
)

fig2 = px.sunburst(df, path=['Product_Category', 'Product_Brand'], values='Total_Amount', title='Spending On Brands')

df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Hour'] = df['DateTime'].dt.hour
df['Weekday'] = df['DateTime'].dt.day_name()
heatmap_data = df.pivot_table(index='Weekday', columns='Hour', values='Purchase_Count', aggfunc='sum')

fig3 = px.imshow(heatmap_data, title='Hourly Heatmap Of Purchase Count Each Weekday',labels=dict(x="Hour", y="Weekday", color="Purchase Count"),
                 color_continuous_scale='Viridis')

gdf['lon'] = gdf.geometry.x
gdf['lat'] = gdf.geometry.y
df['Total_Spend'] = df['Avg_Spend'] * df['Purchase_Count']

fig4 = px.scatter_geo(gdf, lat='lat', lon='lon', hover_name='City',
    hover_data={'Country': True, 'Total_Spend': ':.2f'},
    size='Total_Spend',
    color='Total_Spend',
    color_continuous_scale='Viridis',
    projection='natural earth',
    title='Total Spend per City'
)

fig4.update_layout(
    geo=dict(showland=True, landcolor="lightgray", showcountries=True, countrycolor="black", showocean=True, oceancolor="lightblue",
             projection_type="equirectangular"),
    margin={"r":0, "t":25, "l":0, "b":0}
)


#---------------------app-section----------------------------------------
app.layout = html.Div([
    html.H3("Customer Spending Dashboard", style={'textAlign': 'center'}),
    dbc.Row([  # Wrap graphs in a Row
        dbc.Col(dcc.Graph(id='bar-plot', figure=fig1), width=6),
        dbc.Col(dcc.Graph(id='sunburst-plot', figure=fig2), width=6)
        ], justify="center"),
    dcc.Graph(id ='heatmap-plot', figure=fig3),
    dcc.Graph(id='geo-plot', figure=fig4)

])

if __name__ == '__main__':
    app.run(debug=True)