from datetime import datetime
import pandas as pd
import yfinance as yf


def retrieve_historical_data(stock_list, start_date, end_date):
    """
    Retrieves historical data for a list of stocks from Yahoo Finance.

    :param stock_list: List of stock symbols.
    :param start_date: Start date for the historical data in 'YYYY-MM-DD' format.
    :param end_date: End date for the historical data in 'YYYY-MM-DD' format.
    :return: A dictionary with stock symbols as keys and their historical data as values.
    """
    data = {}
    for stock in stock_list:
        try:
            data[stock] = yf.download(stock, start=start_date, end=end_date)
        except Exception as e:
            print(f"Error retrieving data for {stock}: {e}")
    return data


def create_historical_returns_dataframe(banking_stocks_data):
    close_prices = pd.DataFrame()
    for stock, data in banking_stocks_data.items():
        close_prices[stock] = data['Close']
    historical_returns = close_prices.pct_change()
    historical_returns = historical_returns.dropna()
    return historical_returns


def retrieve_market_index_returns(index_symbol, start_date, end_date):
    """ Retrieve and calculate market index returns. """
    index_data = yf.download(index_symbol, start=start_date, end=end_date)
    index_returns = index_data['Close'].pct_change().dropna()
    return index_returns


stock_symbols = ['SBIN.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS',
                 'KOTAKBANK.NS', 'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS',
                 'FEDERALBNK.NS', 'YESBANK.NS']

start_date = '2020-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

banking_stocks_data = retrieve_historical_data(
    stock_symbols, start_date, end_date)

historical_returns = create_historical_returns_dataframe(banking_stocks_data)
market_index_returns = retrieve_market_index_returns(
    '^NSEI', start_date, end_date)
