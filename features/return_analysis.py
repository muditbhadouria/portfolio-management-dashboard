import matplotlib.pyplot as plt
import pandas as pd
from features.data_retrieval import historical_returns, market_index_returns
from features.risk_analysis import portfolio_daily_returns


def calculate_cumulative_returns(daily_returns):
    """ Calculate cumulative returns from daily returns. """
    cumulative_returns = (1 + daily_returns).cumprod()
    return cumulative_returns


def compare_with_benchmark(portfolio_returns, benchmark_returns):
    """ Compare portfolio returns with benchmark index returns. """
    comparison = pd.DataFrame(
        {'Portfolio': portfolio_returns, 'Benchmark': benchmark_returns})
    return comparison


# def plot_returns_over_time(cumulative_returns, title='Cumulative Returns Over Time'):
#     """ Plot cumulative returns over time. """
#     cumulative_returns.plot()
#     plt.title(title)
#     plt.xlabel('Date')
#     plt.ylabel('Cumulative Returns')
#     plt.show()


# def plot_comparison_with_benchmark(comparison_df, title='Portfolio vs Benchmark'):
#     """ Plot a comparison of the portfolio with a benchmark. """
#     comparison_df.plot()
#     plt.title(title)
#     plt.xlabel('Date')


cumulative_returns = calculate_cumulative_returns(historical_returns)
comparison_df = compare_with_benchmark(
    portfolio_daily_returns, market_index_returns)
# plot_returns_over_time(cumulative_returns)
# plot_comparison_with_benchmark(comparison_df)
portfolio_cumulative_returns = calculate_cumulative_returns(
    portfolio_daily_returns)
benchmark_cumulative_returns = calculate_cumulative_returns(
    market_index_returns)
