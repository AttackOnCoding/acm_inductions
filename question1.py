import pandas as pd
import numpy as np
import yfinance as yf       
import matplotlib.pyplot as plt


# Fetch data
stock_data = yf.download("NVDA", start="2024-11-24", end="2025-05-24")
close_prices = np.array(stock_data["Close"])  # Convert to NumPy array


#rolling means   
stock_data["SMA5"] = stock_data["Close"].rolling(window=5).mean()
stock_data["SMA20"] = stock_data["Close"].rolling(window=20).mean()
print(stock_data[["Close", "SMA5", "SMA20"]].head(10))



# Create signals for crossovers
stock_data['Signal'] = 0
stock_data.loc[stock_data['SMA5'] > stock_data['SMA20'], 'Signal'] = 1
stock_data.loc[stock_data['SMA5'] < stock_data['SMA20'], 'Signal'] = -1
stock_data['Signal'] = stock_data['Signal'].fillna(0)
stock_data['Signal_Change'] = stock_data['Signal'].diff()

# Detect crosses (signal changes from previous day)
stock_data['Signal_Change'] = stock_data['Signal'].diff()

# Buy signals when crossing above (signal changes from -1 or 0 to 1)
buy_signals = stock_data[stock_data['Signal_Change'] > 0]

# Sell signals when crossing below (signal changes from 1 or 0 to -1)
sell_signals = stock_data[stock_data['Signal_Change'] < 0]

#get buy and sell signals's dates
print("Buy Signals:\n", buy_signals[['Close', 'SMA5', 'SMA20']])
print("Sell Signals:\n", sell_signals[['Close', 'SMA5', 'SMA20']])



# Plotting the closing prices and SMAs
plt.figure(figsize=(14, 7))         
plt.plot(stock_data.index, stock_data["Close"], label="Close Price", color='blue',linewidth=1)
plt.plot(stock_data.index, stock_data["SMA5"], label="5-Day SMA", color='orange',linewidth=2)      
plt.plot(stock_data.index, stock_data["SMA20"], label="20-Day SMA", color='green',linewidth=2)


# Plot the signals
plt.scatter(buy_signals.index, buy_signals['SMA5'], marker='^', color='green', label='Buy Signal', s=100)
plt.scatter(sell_signals.index, sell_signals['SMA5'], marker='v', color='red', label='Sell Signal', s=100)


plt.title("NVDA Closing Prices and SMAs",fontdict={"fontsize": 40, "fontname": "Comic Sans MS"})
plt.xlabel("Date",fontdict={"fontsize": 15, "fontname": "Comic Sans MS"})
plt.ylabel("Price (USD)",fontdict={"fontsize": 15, "fontname": "Comic Sans MS"})

plt.legend()
plt.grid()
plt.show()  # Display the plot

# Save the plot to a file instead of displaying it
plt.savefig("NVDA_Closing_Prices_and_SMAs.png", bbox_inches='tight')

# Close the plot to free up memory  
plt.close()
