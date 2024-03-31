import pandas as pd
import numpy as np


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


def align_data(stock_returns, market_returns):
    """ Align the stock and market returns data for analysis. """
    aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    return aligned_data.iloc[:, 0], aligned_data.iloc[:, 1]
