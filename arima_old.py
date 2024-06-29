import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


# This function would fetch historical data for a stock symbol within specified dates
def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    data = data[['Close']]
    # Resample to daily frequency and forward fill missing values
    data = data.resample('D').last().ffill()
    return data

# This function prepares and predicts future stock prices using ARIMA


def predict_stock_prices(symbols, start_date, end_date, forecast_date):
    predictions = {}

    for symbol in symbols:
        # Fetching data
        data = fetch_stock_data(symbol, start_date, end_date)

        # Fit the ARIMA model
        model = ARIMA(data['Close'], order=(1, 1, 1))  # Example order
        model_fit = model.fit()

        # Forecasting the future price
        forecast = model_fit.forecast(steps=(pd.to_datetime(
            forecast_date) - pd.to_datetime(end_date)).days)

        # Plotting the results
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Historical Close Prices')
        forecast_index = pd.date_range(start=end_date, end=forecast_date, freq='D')[
            1:]  # excluding the first date to connect the lines
        plt.plot(forecast_index, forecast.values,
                 label='Forecasted Close Prices', color='red')
        plt.title(f'Stock Price Forecast for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()

        predictions[symbol] = forecast

    return predictions


stock_symbols = ['SBIN.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS',
                 'KOTAKBANK.NS', 'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS',
                 'FEDERALBNK.NS', 'YESBANK.NS']
predictions = predict_stock_prices(
    stock_symbols, '2023-04-15', '2024-04-15', '2024-04-30')
print(predictions)
