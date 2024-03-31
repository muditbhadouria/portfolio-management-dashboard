import pandas as pd


def calculate_cumulative_returns(daily_returns):
    """ Calculate cumulative returns from daily returns. """
    cumulative_returns = (1 + daily_returns).cumprod()
    return cumulative_returns


def compare_with_benchmark(portfolio_returns, benchmark_returns):
    """ Compare portfolio returns with benchmark index returns. """
    comparison = pd.DataFrame(
        {'Portfolio': portfolio_returns, 'Benchmark': benchmark_returns})
    return comparison


# cumulative_returns = calculate_cumulative_returns(historical_returns)
# plot_returns_over_time(cumulative_returns)
# plot_comparison_with_benchmark(comparison_df)
# portfolio_cumulative_returns = calculate_cumulative_returns(
#     portfolio_daily_returns)
# benchmark_cumulative_returns = calculate_cumulative_returns(
#     market_index_returns)
