import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch data
stock_data = yf.download('BYDDY', start="2024-11-24", end="2025-05-24")
close_prices = stock_data["Close"].to_numpy().ravel()  # Ensure 1D array

# Daily Returns Calculation
daily_returns = ((close_prices[1:] - close_prices[:-1]) / close_prices[:-1]) * 100  # Percentage returns
window = 7  # Rolling window
print("Daily Returns shape:", daily_returns.shape)
print("Daily Returns:\n", daily_returns)

# Calculate rolling statistics using pandas
returns_series = pd.Series(daily_returns)  # 1D Series
rolling_mean_returns = returns_series.rolling(window=window).mean()
rolling_std_returns = returns_series.rolling(window=window).std()

# Print statistics
print(f"\n{window}-day Rolling Mean of Daily Returns:\n", rolling_mean_returns)
print(f"\n{window}-day Rolling Std Dev of Daily Returns:\n", rolling_std_returns)

# Plotting
plt.figure(figsize=(50, 7))
plt.plot(stock_data.index[1:], daily_returns, label="Daily Returns", color='blue', marker='o', markersize=3)
plt.plot(stock_data.index[window:], rolling_mean_returns[window-1:], label=f"{window}-Day Rolling Mean", color='orange', linewidth=2)
plt.plot(stock_data.index[window:], rolling_std_returns[window-1:], label=f"{window}-Day Rolling Std Dev", color='green', linewidth=2)

plt.title("BYDDY Daily Returns and Rolling Statistics", fontdict={"fontsize": 30, "fontname": "Comic Sans MS"})
plt.xlabel("Date", fontdict={"fontsize": 15, "fontname": "Comic Sans MS"})
plt.ylabel("Returns (%)", fontdict={"fontsize": 15, "fontname": "Comic Sans MS"})
plt.legend()
plt.grid()
plt.show()

# Save the plot to a file instead of displaying it
plt.savefig("BYDDY_Daily_Returns_and_Rolling_Statistics.png", bbox_inches='tight')
