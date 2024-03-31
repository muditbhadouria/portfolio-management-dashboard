import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from features.data_retrieval import stock_symbols
from features.portfolio_construction import optimal_weights_mvo
from features.risk_analysis import standard_deviation, beta, sharpe_ratio, sortino_ratio, treynor_ratio, portfolio_daily_returns, market_index_returns
from features.return_analysis import benchmark_cumulative_returns, portfolio_cumulative_returns
from features.diversification_analysis import portfolio_variance, diversification_ratio, effective_number_of_assets, correlation_heatmap

# external JavaScript files
external_scripts = [
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH',
        'crossorigin': 'anonymous'
    }
]


def create_comparison_df(portfolio_df, benchmark_df):
    returns_df = pd.concat(
        [portfolio_df, benchmark_df], axis=1).dropna()
    returns_df_perc = returns_df * 100
    returns_df_perc = returns_df_perc.round(2)
    returns_df_perc.rename(columns={0: 'Portfolio Returns',
                                    'Close': 'Benchmark Returns'}, inplace=True)
    print(returns_df_perc)
    return returns_df_perc


# Create a Dash application
app = dash.Dash(__name__, external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

# Define the app layout
app.layout = html.Div([
    html.Div(id='trigger', style={'display': 'none'}),
    html.H1("Portfolio Management Dashboard", style={
            'textAlign': 'center'}, className='p-3 mb-2 bg-light text-dark'),
    html.Div(id='stocks', className='p-2 mb-2'),
    html.Div(children=[html.B('Choose optimization technique to construct portfolio: '), dcc.Dropdown(
        id='opt-dropdown',
        options=[
            {'label': 'Mean Variance', 'value': 'mean_var'},
            {'label': 'Minimum Variance', 'value': 'min_var'},
            {'label': 'Maximum Diversification', 'value': 'max_div'}
        ],
        value='mean_var'
    )], className='p-2 mb-2'),
    html.Div(children=[html.B('Optimal weights of the stocks calculated by Mean Variance Optimization'), html.Div(
        id='weights')], className='p-2 mb-2'),
    html.Div(children=[html.B('Risk Analysis'), html.Div(
        id='risk_metrics')], className='p-2 mb-2'),
    html.Div(children=[html.B('Portfolio Returns v/s Benchmark Returns'), html.Div(
        id='portfolio-returns-time-series')], className='p-2 mb-2'),
    html.Div(children=[html.B('Portfolio Cumulative Returns v/s Benchmark Cumulative Returns'), html.Div(
        id='cumulative-returns-time-series')], className='p-2 mb-2'),
    html.Div(children=[html.B('Diversification Analysis'), html.Div(
        id='diversification-metrics')], className='p-2 mb-2'),
    html.Div(children=[html.B('Diversification Heatmap'), dcc.Graph(
        figure=correlation_heatmap)], className='p-2 mb-2')
])


@app.callback(
    Output('stocks', 'children'),
    [Input('trigger', 'children')]
)
def update_stocks(trigger):
    return [html.B('Stocks in portfolio: '), html.Span(', '.join(stock_symbols))]


@app.callback(
    Output('weights', 'children'),
    [Input('trigger', 'children')]
)
def update_weights_table(trigger):
    weights_table_row = []
    for i in range(0, len(stock_symbols)):
        weights_table_row.append(
            html.Tr([html.Td(stock_symbols[i]), html.Td(round(optimal_weights_mvo[i] * 100, 2))]))

    weights_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Stock"), html.Th("Weight (%)")])
        ),
        html.Tbody(weights_table_row)
    ])
    return weights_table


@app.callback(
    Output('risk_metrics', 'children'),
    [Input('trigger', 'children')]
)
def update_risk_metrics_table(trigger):
    risk_metrics = [
        {'metric': 'Standard Deviation', 'value': standard_deviation},
        {'metric': 'Beta', 'value': beta},
        {'metric': 'Sharpe Ratio', 'value': sharpe_ratio},
        {'metric': 'Sortino Ratio', 'value': sortino_ratio},
        {'metric': 'Treynor Ratio', 'value': treynor_ratio},
    ]
    risk_metrics_row = []
    for i in range(0, len(risk_metrics)):
        risk_metrics_row.append(
            html.Tr([html.Td(risk_metrics[i]['metric']), html.Td(round(risk_metrics[i]['value'], 2))]))

    metrics_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Metric"), html.Th("Values")])
        ),
        html.Tbody(risk_metrics_row)
    ])
    return metrics_table


@app.callback(
    Output('portfolio-returns-time-series', 'children'),
    [Input('trigger', 'children')]
)
def update_pr_fig(trigger):
    df = create_comparison_df(
        portfolio_daily_returns, market_index_returns)
    return dcc.Graph(
        id='portfolio-returns-time-series-fig',
        figure=px.line(df, x=df.index, y=df.columns)
    ),


@app.callback(
    Output('cumulative-returns-time-series', 'children'),
    [Input('trigger', 'children')]
)
def update_cr_fig(trigger):
    return dcc.Graph(
        id='cumulative-returns-time-series-fig',
        figure=px.line(create_comparison_df(
            portfolio_cumulative_returns, benchmark_cumulative_returns))  # Create a line plot
    ),


@app.callback(
    Output('diversification-metrics', 'children'),
    [Input('trigger', 'children')]
)
def update_div_metrics_table(trigger):
    diversification_metrics = [
        {'metric': 'Portfolio variance', 'value': portfolio_variance},
        {'metric': 'Diversification Ratio', 'value': diversification_ratio},
        {'metric': 'Effective Number of Assets',
            'value': effective_number_of_assets}
    ]
    diversification_metrics_row = []
    for i in range(0, len(diversification_metrics)):
        diversification_metrics_row.append(
            html.Tr([html.Td(diversification_metrics[i]['metric']), html.Td(round(diversification_metrics[i]['value'], 2))]))

    metrics_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Metric"), html.Th("Values")])
        ),
        html.Tbody(diversification_metrics_row)
    ])
    return metrics_table


# Run the Dash app
if __name__ == '__main__':
    app.run_server()
