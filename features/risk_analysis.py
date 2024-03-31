import pandas as pd
import numpy as np
from features.data_retrieval import historical_returns, market_index_returns
from features.portfolio_construction import optimal_weights_mvo


def calculate_portfolio_returns(daily_returns, weights):
    """ Calculate the daily portfolio returns. """
    weighted_returns = daily_returns.multiply(weights, axis=1)
    portfolio_returns = weighted_returns.sum(axis=1)
    return portfolio_returns


def calculate_standard_deviation(portfolio_returns):
    """ Calculate the standard deviation (total risk) of a portfolio. """
    return portfolio_returns.std()


def calculate_beta(stock_returns, market_returns):
    """ Calculate the beta of a portfolio. """
    covariance = np.cov(stock_returns, market_returns)[0][1]
    market_variance = np.var(market_returns)
    beta = covariance / market_variance
    return beta


def calculate_sharpe_ratio(portfolio_returns, risk_free_rate):
    """ Calculate the Sharpe Ratio of a portfolio. """
    excess_returns = portfolio_returns - risk_free_rate
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    return sharpe_ratio * np.sqrt(252)


def calculate_sortino_ratio(portfolio_returns, risk_free_rate):
    """ Calculate the Sortino Ratio of a portfolio. """
    negative_returns = portfolio_returns[portfolio_returns < risk_free_rate]
    downside_std = np.std(negative_returns)
    excess_returns = portfolio_returns - risk_free_rate
    sortino_ratio = excess_returns.mean() / downside_std
    return sortino_ratio * np.sqrt(252)


def calculate_treynor_ratio(portfolio_returns, portfolio_beta, risk_free_rate):
    """ Calculate the Treynor Ratio of a portfolio. """
    excess_returns = portfolio_returns - risk_free_rate
    treynor_ratio = excess_returns.mean() / portfolio_beta
    return treynor_ratio


# Step 2: Calculate portfolio returns
portfolio_daily_returns = calculate_portfolio_returns(
    historical_returns, optimal_weights_mvo)
standard_deviation = calculate_standard_deviation(portfolio_daily_returns)

# Step 2: Perform Risk Analysis
# You'll need the risk-free rate for some of these calculations.
# For example, use a typical value like 0.02 (or 2%) for the risk-free rate, or fetch the current rate.
risk_free_rate = 0.02

sharpe_ratio = calculate_sharpe_ratio(portfolio_daily_returns, risk_free_rate)
sortino_ratio = calculate_sortino_ratio(
    portfolio_daily_returns, risk_free_rate)


def align_data(stock_returns, market_returns):
    """ Align the stock and market returns data for analysis. """
    aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    return aligned_data.iloc[:, 0], aligned_data.iloc[:, 1]


portfolio_daily_returns, market_index_returns = align_data(
    portfolio_daily_returns, market_index_returns)
# If calculating beta, you'll need the market index returns as well.
beta = calculate_beta(portfolio_daily_returns, market_index_returns)
treynor_ratio = calculate_treynor_ratio(
    portfolio_daily_returns, beta, risk_free_rate)
