import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from features.data_retrieval import stock_symbols, historical_returns, market_index_returns
from features.portfolio_construction import optimal_weights_mvo, optimal_weights_mvp, optimal_weights_max_div
from features.risk_analysis import calculate_portfolio_returns, align_data, calculate_standard_deviation, calculate_sharpe_ratio, calculate_sortino_ratio, calculate_beta, calculate_treynor_ratio
from features.return_analysis import calculate_cumulative_returns
from features.diversification_analysis import calculate_portfolio_variance, calculate_diversification_ratio, calculate_effective_number_of_assets, correlation_heatmap

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
    return returns_df_perc


# Create a Dash application
app = dash.Dash(__name__, external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

# Define the app layout
app.layout = html.Div([
    html.Div(id='trigger', style={'display': 'none'}),
    html.H1("Portfolio Management Dashboard", style={
            'textAlign': 'center'}, className='p-3 mb-2 bg-light text-dark'),
    html.Div(children=[html.B('Stocks in portfolio: '), html.Span(
        ', '.join(stock_symbols))], className='p-2 mb-2'),
    html.Div(children=[html.B('Choose optimization technique to construct portfolio: '), dcc.Dropdown(
        id='opt-dropdown',
        options=[
            {'label': 'Mean Variance', 'value': 'mev'},
            {'label': 'Minimum Variance', 'value': 'miv'},
            {'label': 'Maximum Diversification', 'value': 'mad'}
        ],
        value='mev'
    )], className='p-2 mb-2'),
    html.Div(children=[html.B('Optimal weights of the stocks calculated by Mean Variance Optimization'), html.Div(
        id='weights')], className='p-2 mb-2'),
    html.Div(children=[html.B('Risk Analysis'), html.Div(
        id='risk-metrics')], className='p-2 mb-2'),
    html.Div(children=[html.Div(
        id='portfolio-returns-time-series')], className='p-2 mb-2'),
    html.Div(children=[html.Div(
        id='cumulative-returns-time-series')], className='p-2 mb-2'),
    html.Div(children=[html.B('Diversification Analysis'), html.Div(
        id='diversification-metrics')], className='p-2 mb-2'),
    html.Div(children=[dcc.Graph(
        figure=correlation_heatmap)], className='p-2 mb-2')
])


@app.callback(
    [
        Output('weights', 'children'),
        Output('risk-metrics', 'children'),
        Output('portfolio-returns-time-series', 'children'),
        Output('cumulative-returns-time-series', 'children'),
        Output('diversification-metrics', 'children'),
    ],
    [Input('opt-dropdown', 'value')]
)
def update_weights_table(value):
    if value == 'mev':
        optimal_weights = optimal_weights_mvo
    elif value == 'miv':
        optimal_weights = optimal_weights_mvp
    elif value == 'mad':
        optimal_weights = optimal_weights_max_div

    ########################### Get weight of different stocks in portfolio ###########################
    weights_table_row = []
    for i in range(0, len(stock_symbols)):
        weights_table_row.append(
            html.Tr([html.Td(stock_symbols[i]), html.Td(round(optimal_weights[i] * 100, 2))]))

    weights_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Stock"), html.Th("Weight (%)")])
        ),
        html.Tbody(weights_table_row)
    ])

    ########################### Get risk metrics from risk analysis ###########################
    portfolio_daily_returns = calculate_portfolio_returns(
        historical_returns, optimal_weights)
    portfolio_daily_returns, index_daily_returns = align_data(
        portfolio_daily_returns, market_index_returns)
    standard_deviation = calculate_standard_deviation(portfolio_daily_returns)

    # You'll need the risk-free rate for some of these calculations.
    # For example, use a typical value like 0.02 (or 2%) for the risk-free rate, or fetch the current rate.
    risk_free_rate = 0.02

    sharpe_ratio = calculate_sharpe_ratio(
        portfolio_daily_returns, risk_free_rate)
    sortino_ratio = calculate_sortino_ratio(
        portfolio_daily_returns, risk_free_rate)

    # If calculating beta, you'll need the market index returns as well.
    beta = calculate_beta(portfolio_daily_returns, index_daily_returns)
    treynor_ratio = calculate_treynor_ratio(
        portfolio_daily_returns, beta, risk_free_rate)

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

    risk_metrics_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Metric"), html.Th("Values")])
        ),
        html.Tbody(risk_metrics_row)
    ])

    ########################### Create graphs for return analysis ###########################
    daily_comparison_fig = px.line(create_comparison_df(
        portfolio_daily_returns, index_daily_returns))
    daily_comparison_fig.update_layout(
        title='Portfolio Returns v/s Benchmark Returns')

    daily_comparison_graph = dcc.Graph(
        id='portfolio-returns-time-series-fig',
        figure=daily_comparison_fig
    )

    portfolio_cumulative_returns = calculate_cumulative_returns(
        portfolio_daily_returns)
    benchmark_cumulative_returns = calculate_cumulative_returns(
        index_daily_returns)

    cumulative_comparison_fig = px.line(create_comparison_df(
        portfolio_cumulative_returns, benchmark_cumulative_returns))
    cumulative_comparison_fig.update_layout(
        title='Portfolio Cumulative Returns v/s Benchmark Cumulative Returns')

    cumulative_comparison_graph = dcc.Graph(
        id='cumulative-returns-time-series-fig',
        figure=cumulative_comparison_fig
    )

    ########################### Get metrics and graphs for Diversification Analysis ###########################
    portfolio_variance = calculate_portfolio_variance(
        historical_returns, optimal_weights)
    diversification_ratio = calculate_diversification_ratio(
        historical_returns, optimal_weights)
    effective_number_of_assets = calculate_effective_number_of_assets(
        optimal_weights)
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
    diversification_metrics_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Metric"), html.Th("Values")])
        ),
        html.Tbody(diversification_metrics_row)
    ])

    return weights_table, risk_metrics_table, daily_comparison_graph, cumulative_comparison_graph, diversification_metrics_table


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
