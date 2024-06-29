import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt


def fetch_stock_data(symbol, start_date, end_date):
    # Fetching stock data using yfinance
    data = yf.download(symbol, start=start_date, end=end_date)
    return data['Close']


def test_stationarity(series):
    # Perform Augmented Dickey-Fuller test
    # dropna is important as adfuller does not handle missing values
    result = adfuller(series.dropna())
    print(f'ADF Statistic for {series.name}: {result[0]}')
    print(f'p-value for {series.name}: {result[1]}')
    return result[1]


def find_optimal_d(series):
    d = 0
    p_value = test_stationarity(series)
    while p_value > 0.05:
        d += 1
        series = series.diff().dropna()
        p_value = test_stationarity(series)
    return d


def plot_acf_pacf(series, lags=20):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(series.dropna(), lags=lags, ax=ax1)
    plot_pacf(series.dropna(), lags=lags, ax=ax2)
    plt.show()


def fit_predict_arima(stock_symbols, start_date, end_date, forecast_date):
    forecasts = {}
    for symbol in stock_symbols:
        data = fetch_stock_data(symbol, start_date, end_date)
        d = find_optimal_d(data)
        print(f'Optimal d found for {symbol}: {d}')

        # Differencing the data according to the optimal d found
        data_diff = data.diff(d).dropna()

        # Display ACF and PACF to determine p and q
        plot_acf_pacf(data_diff)

        # Assume p=1, q=1 for initial model fitting (these should be adjusted based on ACF and PACF plots)
        model = ARIMA(data, order=(1, d, 1))
        model_fit = model.fit()

        # Forecasting
        forecast = model_fit.forecast(steps=(pd.to_datetime(
            forecast_date) - pd.to_datetime(end_date)).days)

        # Plotting results
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data, label='Historical Close Prices')
        forecast_index = pd.date_range(start=end_date, periods=len(
            forecast)+1, freq='D')[1:]  # Ensure continuity
        plt.plot(forecast_index, forecast.values,
                 label='Forecasted Close Prices', color='red')
        plt.title(f'Stock Price Forecast for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()

        forecasts[symbol] = forecast

    return forecasts


stock_symbols = ['SBIN.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS',
                 'KOTAKBANK.NS', 'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS',
                 'FEDERALBNK.NS', 'YESBANK.NS']
forecasts = fit_predict_arima(
    stock_symbols, '2023-04-15', '2024-04-15', '2024-04-30')
print(forecasts)
