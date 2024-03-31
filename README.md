# Portfolio Management Dashboard

## Overview

This project includes a comprehensive set of tools for managing and analyzing investment portfolios. It features data retrieval, portfolio construction and optimization, risk and return analysis, diversification assessment, and an interactive web dashboard using Plotly Dash.

## Features

1. **Data Retrieval**: Fetch historical financial data for stocks.
2. **Portfolio Construction**: Implement portfolio optimization techniques like Mean-Variance Optimization, Minimum Variance, and Maximum Diversification.
3. **Risk Analysis**: Calculate risk metrics such as standard deviation, beta, Sharpe ratio, Sortino ratio, and Treynor ratio.
4. **Return Analysis**: Compute portfolio returns, cumulative returns, and compare against benchmark indices.
5. **Diversification Analysis**: Assess the level of diversification using metrics like portfolio variance, diversification ratio, and effective number of assets. Visualization of diversification benefits through heatmaps.

## Visualization

Interactive visualizations using Plotly to analyze the performance and diversification of the portfolio.

## Web Dashboard

An interactive web dashboard using Plotly Dash for a user-friendly analysis experience.

## Usage

The system requires Python with libraries such as Pandas, NumPy, SciPy, Plotly, and Dash. To run the web application, execute the following commands in your terminal -
python -m venv venv
.\myenv\Scripts\Activate.ps1 (for windows terminal)
source venv/bin/activate (for MacOS / linux)
pip install -R requirements.txt
python app.py
