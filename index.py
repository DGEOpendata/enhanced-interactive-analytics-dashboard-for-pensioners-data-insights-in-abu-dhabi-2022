python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
data = pd.read_excel('Distribution_of_Pensioners_2022.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Enhanced Pensioners Data Dashboard for Abu Dhabi 2022'),
    html.Div([
        dcc.Dropdown(
            id='quarter-dropdown',
            options=[
                {'label': 'Q1', 'value': 'Q1'},
                {'label': 'Q2', 'value': 'Q2'},
                {'label': 'Q3', 'value': 'Q3'},
                {'label': 'Q4', 'value': 'Q4'}
            ],
            placeholder='Select a Quarter',
            multi=True
        ),
        dcc.Graph(id='gender-distribution')
    ]),
    html.Div([
        dcc.Graph(id='total-pensioners-trend')
    ])
])

# Callback for updating the gender distribution chart
@app.callback(
    Output('gender-distribution', 'figure'),
    [Input('quarter-dropdown', 'value')]
)
def update_gender_distribution(quarters):
    filtered_data = data if not quarters else data[data['Quarter'].isin(quarters)]
    fig = px.bar(
        filtered_data, 
        x='Quarter', 
        y='Count', 
        color='Type', 
        title='Gender Distribution per Quarter',
        labels={'Count': 'Number of Pensioners', 'Quarter': 'Quarter'},
    )
    return fig

# Callback for total pensioners trend
@app.callback(
    Output('total-pensioners-trend', 'figure'),
    [Input('quarter-dropdown', 'value')]
)
def update_total_pensioners_trend(quarters):
    filtered_data = data if not quarters else data[data['Quarter'].isin(quarters)]
    total_data = filtered_data.groupby('Quarter')['Count'].sum().reset_index()
    fig = px.line(
        total_data, 
        x='Quarter', 
        y='Count', 
        title='Total Number of Pensioners per Quarter',
        markers=True
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
