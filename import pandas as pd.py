import pandas as pd
import matplotlib.pyplot as plt

# Load stock data
df = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1262304000&period2=1645824000&interval=1d&events=history')

# Convert date to datetime format and set it as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate 50-day and 200-day moving averages
df['50MA'] = df['Close'].rolling(window=50).mean()
df['200MA'] = df['Close'].rolling(window=200).mean()

# Plot candlestick chart
plt.figure(figsize=(10, 6))
plt.title('Microsoft Stock Prices with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.grid(True)

for i in range(len(df)):
    if df['Close'][i] > df['Open'][i]:
        plt.plot([df.index[i], df.index[i]], [df['Low'][i], df['High'][i]], color='green')
        plt.plot([df.index[i], df.index[i]], [df['Open'][i], df['Close'][i]], color='green', linewidth=2)
    elif df['Close'][i] < df['Open'][i]:
        plt.plot([df.index[i], df.index[i]], [df['Low'][i], df['High'][i]], color='red')
        plt.plot([df.index[i], df.index[i]], [df['Open'][i], df['Close'][i]], color='red', linewidth=2)
    else:
        plt.plot(df.index[i], df['Close'][i], 'k_')

plt.plot(df.index, df['50MA'], color='blue', label='50-day MA')
plt.plot(df.index, df['200MA'], color='red', label='200-day MA')

# Plot markers for crossover points
crossover_points = []
for i in range(1, len(df)):
    if (df['50MA'][i] > df['200MA'][i]) != (df['50MA'][i - 1] > df['200MA'][i - 1]):
        crossover_points.append(df.index[i])
        plt.scatter(df.index[i], df['Close'][i], marker='^', color='green', s=100)
    elif (df['50MA'][i] < df['200MA'][i]) != (df['50MA'][i - 1] < df['200MA'][i - 1]):
        crossover_points.append(df.index[i])
        plt.scatter(df.index[i], df['Close'][i], marker='v', color='red', s=100)

plt.legend()
plt.show()
