from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
df = pd.read_csv('processed_retail_data.csv')

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


#---------------------app-section----------------------------------------
app.layout = html.Div([
    html.H3("Customer Spending Dashboard", style={'textAlign': 'center'}),
    dbc.Row([  # Wrap graphs in a Row
        dbc.Col(dcc.Graph(id='bar-plot', figure=fig1), width=6),
        dbc.Col(dcc.Graph(id='sunburst-plot', figure=fig2), width=6)
        ], justify="center"),
    dcc.Graph(id ='heatmap-plot', figure=fig3),

])

if __name__ == '__main__':
    app.run(debug=True)