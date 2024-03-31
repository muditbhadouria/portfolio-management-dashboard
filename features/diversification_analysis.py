import numpy as np
from features.data_retrieval import historical_returns
from features.portfolio_construction import optimal_weights_mvo
import plotly.graph_objs as go


def calculate_portfolio_variance(returns, weights):
    """ Calculate the variance of the portfolio. """
    portfolio_variance = np.dot(
        weights.T, np.dot(returns.cov() * 252, weights))
    return portfolio_variance


def calculate_diversification_ratio(returns, weights):
    """ Calculate the diversification ratio of the portfolio. """
    portfolio_std = np.sqrt(calculate_portfolio_variance(returns, weights))
    weighted_std = np.sum(weights * returns.std() * np.sqrt(252))
    diversification_ratio = portfolio_std / weighted_std
    return diversification_ratio


def calculate_effective_number_of_assets(weights):
    """ Calculate the effective number of assets in the portfolio. """
    ena = (np.sum(weights)**2) / np.sum(weights**2)
    return ena


def plot_correlation_heatmap(returns, title='Asset Diversification Heatmap'):
    """ Plot a heatmap of asset correlations. """
    correlation_matrix = returns.corr()
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis'))
    fig.update_layout(title=title, xaxis_nticks=len(
        returns.columns), yaxis_nticks=len(returns.columns))
    return fig


correlation_heatmap = plot_correlation_heatmap(historical_returns)
