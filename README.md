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

## Running the Web Application

To run the web application, follow these steps in your terminal:

1. **Create a Virtual Environment**:

   ```
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:

   - For Windows Terminal:
     ```
     .\venv\Scripts\Activate.ps1
     ```
   - For MacOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install Required Packages**:

   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```
   python app.py
   ```

Ensure to execute these commands in the root directory of your project where the `app.py` file is located. The `requirements.txt` file should list all the necessary Python packages needed for the web application.
