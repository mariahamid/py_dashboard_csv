import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

# Read data from CSV file
df = pd.read_csv('supermarkt_sales.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Dash app setup
app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Charts', children=[
            html.Div([
                html.Div([
                    dcc.Graph(id='pie-chart'),
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Graph(id='line-chart'),
                ], style={'width': '48%', 'display': 'inline-block'}),
            ]),
        ]),
        dcc.Tab(label='Data Table', children=[
            html.H2('Data Table'),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
            )
        ])
    ])
])


# Callback to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    Input('pie-chart', 'id')
)
def update_pie_chart(_):
    product_line_column = 'Product_line'

    if product_line_column in df.columns:
        product_line_counts = df[product_line_column].value_counts()
        fig = px.pie(
            names=product_line_counts.index,
            values=product_line_counts.values,
            title='Distribution of Product Lines',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        return fig
    return {}


# Callback to update the line chart
@app.callback(
    Output('line-chart', 'figure'),
    Input('line-chart', 'id')
)
def update_line_chart(_):
    date_column = 'Date'  # Replace with your actual date column
    sales_column = 'Total'  # Replace with your actual sales/amount column

    if date_column in df.columns and sales_column in df.columns:
        # Convert date column to datetime if it's not already
        df[date_column] = pd.to_datetime(df[date_column])

        # Group by date and sum the sales
        df_grouped = df.groupby(date_column)[sales_column].sum().reset_index()

        fig = px.line(
            df_grouped,
            x=date_column,
            y=sales_column,
            title='Total Sales Over Time',
            labels={sales_column: 'Total Sales', date_column: 'Date'}
        )
        return fig
    return {}


if __name__ == '__main__':
    app.run_server(debug=True, port=4444)
