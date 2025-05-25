from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
df = pd.read_csv('processed_retail_data.csv')

grouped_df = df.groupby(['Age', 'Gender'], as_index=False)['Avg_Spend'].sum()
# Create initial figure
fig1 = px.bar(
    grouped_df,
    x='Age',
    y='Avg_Spend',
    color='Gender',
    color_discrete_sequence=px.colors.qualitative.Bold,
    barmode='group',
    title='Average Spending by Age'
)

# Set initial dark theme
fig1.update_layout(
    plot_bgcolor='rgba(10,10,10,0.1)',
    paper_bgcolor='black',
    font_color='white',
    hoverlabel=dict(bgcolor='black')
)

app.layout = html.Div([
    html.H3("Customer Spending Dashboard", style={'textAlign': 'center'}),
    dbc.Switch(
        id='theme-toggle',
        label="Dark Mode",
        value=True,  # Default to dark mode
        style={'margin': '10px auto', 'display': 'block', 'width': 'fit-content'}
    ),
    dcc.Graph(id='bar-plot', figure=fig1)
])

# Add callback to handle theme switching
@callback(
    Output('bar-plot', 'figure'),
    Output('theme-toggle', 'label'),
    Input('theme-toggle', 'value')
)
def update_theme(is_dark):
    if is_dark:
        # Dark theme settings
        fig1.update_layout(
            plot_bgcolor='rgba(10,10,10,0.1)',
            paper_bgcolor='black',
            font_color='white',
            hoverlabel=dict(bgcolor='black'),
            title='Average Spending by Age'
        )
        label = "Dark Mode"
    else:
        # Light theme settings
        fig1.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='aliceblue',
            font_color='black',
            hoverlabel=dict(bgcolor='white'),
            title='Average Spending by Age'
        )
        label = "Light Mode"
    return fig1, label

if __name__ == '__main__':
    app.run(debug=True)