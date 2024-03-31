import numpy as np
import pandas as pd
from scipy.optimize import minimize
from features.data_retrieval import historical_returns


def calculate_portfolio_metrics(returns, weights):
    """
    Calculate expected return, volatility, and Sharpe ratio for the portfolio.

    :param returns: DataFrame of historical returns.
    :param weights: Weights of each asset in the portfolio.
    :return: A tuple containing portfolio return, portfolio volatility, and Sharpe ratio.
    """
    portfolio_return = np.sum(returns.mean() * weights) * 252
    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    sharpe_ratio = portfolio_return / portfolio_volatility
    return portfolio_return, portfolio_volatility, sharpe_ratio


def mean_variance_optimization(returns):
    """
    Perform mean-variance optimization to find the optimal weights.

    :param returns: DataFrame of historical returns.
    :return: Optimal weights for the portfolio.
    """
    num_assets = len(returns.columns)
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    initial_guess = num_assets * [1. / num_assets,]

    def portfolio_volatility(weights, returns):
        return calculate_portfolio_metrics(returns, weights)[1]

    optimal_weights = minimize(portfolio_volatility, initial_guess, args=args,
                               method='SLSQP', bounds=bounds, constraints=constraints)
    return optimal_weights.x


def minimum_variance_portfolio(returns):
    num_assets = len(returns.columns)
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    initial_guess = num_assets * [1. / num_assets,]

    def portfolio_volatility(weights, returns):
        return calculate_portfolio_metrics(returns, weights)[1]

    optimal_weights = minimize(portfolio_volatility, initial_guess, args=args,
                               method='SLSQP', bounds=bounds, constraints=constraints)
    return optimal_weights.x


def maximum_diversification_portfolio(returns):
    num_assets = len(returns.columns)
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    initial_guess = num_assets * [1. / num_assets,]

    def diversification_ratio(weights, returns):
        weighted_volatilities = np.dot(weights, returns.std() * np.sqrt(252))
        portfolio_volatility = np.sqrt(
            np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        return -weighted_volatilities / portfolio_volatility  # Negative for maximization

    optimal_weights = minimize(diversification_ratio, initial_guess, args=args,
                               method='SLSQP', bounds=bounds, constraints=constraints)
    return optimal_weights.x


optimal_weights_mvo = mean_variance_optimization(historical_returns)
optimal_weights_mvp = minimum_variance_portfolio(historical_returns)
optimal_weights_max_div = maximum_diversification_portfolio(historical_returns)
