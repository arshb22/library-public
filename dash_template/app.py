import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from queries.sql_generator import natural_language_to_sql, SQLQuery
from queries.predefined_queries import get_predefined_query
from config import DATABASE_URI
from utils.data_loader import load_banking_data, load_mortgage_data, load_sbl_data
from utils.update_process import update_banking_table, update_mortgage_table, update_sbl_table

# Initialize database engine
engine = create_engine(DATABASE_URI)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Input(id='nl-query-input', type='text', placeholder='Enter your query here', style={'width': '100%'}),
    html.Button('Run Query', id='run-query-button', n_clicks=0),
    dcc.Graph(id='table-graph'),
    html.Div(id='summary-stats')
])

# Function to run a query and return a DataFrame
def run_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Callback to run the query and update the graph and summary statistics
@app.callback(
    [Output('table-graph', 'figure'), Output('summary-stats', 'children')],
    [Input('run-query-button', 'n_clicks')],
    [State('nl-query-input', 'value')]
)
def update_output(n_clicks, nl_query):
    if n_clicks > 0:
        if nl_query:
            # Generate the SQL query from the natural language query
            sql_query_str = natural_language_to_sql(nl_query)
            query = sql_query_str
        else:
            # Use a predefined query as the default
            query = get_predefined_query('banking')

        # Run the generated query
        df = run_query(query)

        # Determine the column to plot based on the table being queried
        column_to_plot = 'balance' if 'banking' in query else 'loan_amount'

        # Visualize the data and generate summary statistics
        fig = px.histogram(df, x=column_to_plot, title=f'{column_to_plot.capitalize()} Distribution')
        summary = df[column_to_plot].describe().to_dict()

        summary_stats = html.Div([
            html.H4('Summary Statistics'),
            html.P(f"Count: {summary['count']}"),
            html.P(f"Mean: {summary['mean']}"),
            html.P(f"Std: {summary['std']}"),
            html.P(f"Min: {summary['min']}"),
            html.P(f"25%: {summary['25%']}"),
            html.P(f"50%: {summary['50%']}"),
            html.P(f"75%: {summary['75%']}"),
            html.P(f"Max: {summary['max']}")
        ])

        return fig, summary_stats
    return {}, ''

if __name__ == '__main__':

    # Perform initial table updates if needed
    update_banking_table()
    update_mortgage_table()
    update_sbl_table()

    # Run the Dash app
    app.run_server(debug=True)
