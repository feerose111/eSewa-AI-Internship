from dash import Dash, html,dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Spending pattern dashboard.')

])

#run app
if __name__ == '__main__':
    app.run(debug= True)