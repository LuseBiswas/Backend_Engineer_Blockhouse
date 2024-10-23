# stocks/views.py

import requests
from django.http import JsonResponse, HttpResponse
from .models import StockData, BacktestResult, StockPrediction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import joblib
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

ALPHA_VANTAGE_API_KEY = 'MVKYIAO0KG6YJUZP'  # Replace with your key

def fetch_stock_data(request, symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("Time Series (Daily)", {})
        for date, daily_data in data.items():
            StockData.objects.update_or_create(
                symbol=symbol,
                date=datetime.strptime(date, "%Y-%m-%d"),
                defaults={
                    'open_price': daily_data["1. open"],
                    'close_price': daily_data["4. close"],
                    'high_price': daily_data["2. high"],
                    'low_price': daily_data["3. low"],
                    'volume': daily_data["5. volume"],
                }
            )
        return JsonResponse({"status": "success", "message": f"Data for {symbol} fetched and saved."})
    else:
        return JsonResponse({"status": "error", "message": "Failed to fetch data."})


def backtest_strategy(request):
    symbol = request.GET.get('symbol', 'AAPL')
    initial_investment = float(request.GET.get('investment', 10000))

    # Fetch historical data from the database
    data = StockData.objects.filter(symbol=symbol).values()
    df = pd.DataFrame(data)

    # Calculate moving averages
    df['50_MA'] = df['close_price'].rolling(window=50).mean()
    df['200_MA'] = df['close_price'].rolling(window=200).mean()

    # Backtesting logic: Buy below 50_MA, Sell above 200_MA
    cash = initial_investment
    holdings = 0
    trades = 0

    for i in range(1, len(df)):
        if df['close_price'].iloc[i] < df['50_MA'].iloc[i] and holdings == 0:
            holdings = cash / df['close_price'].iloc[i]
            cash = 0
            trades += 1
        elif df['close_price'].iloc[i] > df['200_MA'].iloc[i] and holdings > 0:
            cash = holdings * df['close_price'].iloc[i]
            holdings = 0
            trades += 1

    # Final portfolio value
    portfolio_value = cash + (holdings * df['close_price'].iloc[-1])
    total_return = ((portfolio_value - initial_investment) / initial_investment) * 100
    max_drawdown = df['close_price'].min()  # Simplified for demo purposes

    # Save result (optional)
    result = BacktestResult.objects.create(
        symbol=symbol, total_return=total_return, 
        max_drawdown=max_drawdown, trades_executed=trades
    )

    return JsonResponse({
        'status': 'success',
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'trades_executed': trades
    })



# Load your pre-trained model
MODEL_PATH = 'stocks/models/model.pkl'  # Adjust the path if needed
model = joblib.load(MODEL_PATH)

def prepare_input_data(historical_data):
   
    # Ensure the date column is in datetime format
    historical_data['date'] = pd.to_datetime(historical_data['date'])

     # Extract relevant features from historical data
    # Using 'day' of the year for this example

    historical_data['day'] = historical_data['date'].dt.dayofyear
    X = historical_data[['day']]
    return X



def fetch_actual_prices(symbol):
    """
    Fetch actual stock prices for the given symbol from the StockData model.

    Args:
        symbol (str): The stock symbol for which to fetch actual prices.

    Returns:
        List[float]: A list of actual prices for the specified symbol, ordered by date.
    """
    # Fetch the actual stock prices from the StockData model, ordered by date
    actual_data = StockData.objects.filter(symbol=symbol).order_by('date')

    # Extract and return the close prices as a list
    # We're fetching the close prices for each date
    return StockData.objects.filter(symbol=symbol).values_list('close_price', flat=True)

def predict_stock_prices(request, symbol):
    # Fetch historical data for the given symbol
    historical_data = StockData.objects.filter(symbol=symbol).order_by('date')
    historical_df = pd.DataFrame(list(historical_data.values('date', 'close_price')))
    
    if historical_df.empty:
        return JsonResponse({"status": "error", "message": "No historical data found."})

    # Prepare the input data
    X = prepare_input_data(historical_df)

    # Predict future stock prices
    predicted_prices = model.predict(X)

    # Fetch actual prices (this part depends on your actual data source)
    # Example: You might fetch the latest prices from another API or your database
    actual_prices = fetch_actual_prices(symbol)  # Define this function as needed
    print(f"Actual Prices for {symbol}: {actual_prices}")  # Debug statement


    # Save predictions in the database
    for i, price in enumerate(predicted_prices):
        actual_price = actual_prices[i] if i < len(actual_prices) else None
        print(f"Predicted Price: {price}, Actual Price: {actual_price}")  # Debug statement
        prediction = StockPrediction(symbol=symbol, predicted_price=price, day=i+1)  # Assuming day starts from 1
        prediction.save()

    # Return the predictions as a JSON response
    return JsonResponse({
        "status": "success",
        "predicted_prices": predicted_prices.tolist()  # Convert to list for JSON serialization
    })







def generate_report(request):
  # Fetch the actual and predicted prices from the database
    symbol = 'AAPL'  # You can make this dynamic based on user input
    actual_prices = fetch_actual_prices(symbol)  
    predicted_prices = StockPrediction.objects.filter(symbol=symbol).values_list('predicted_price', flat=True)  

    # Convert to lists for processing
    actual_prices = list(actual_prices)
    predicted_prices = list(predicted_prices)

    # Debug output
    print(f"Actual Prices: {actual_prices}")
    print(f"Predicted Prices: {predicted_prices}")

    # Calculate metrics
    total_roi = calculate_total_roi(actual_prices, predicted_prices)
    max_drawdown = calculate_max_drawdown(actual_prices)
    num_trades = len(predicted_prices)

    # Create a plot
    plt.figure(figsize=(10, 5))
    plt.plot(actual_prices, label='Actual Prices', color='blue', marker='o')
    plt.plot(predicted_prices, label='Predicted Prices', color='orange', linestyle='dashed', marker='x')
    plt.title(f'Stock Prices for {symbol}')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    
    # Save the plot as an image
    plot_file = 'stock_prices_plot.png'
    plt.savefig(plot_file, format='png')
    plt.close()  # Close the plot to free memory

    # Generate PDF report
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    p.drawString(100, 750, "Stock Performance Report")
    p.drawString(100, 730, f"Total ROI: {total_roi:.2f}%")
    p.drawString(100, 710, f"Max Drawdown: {max_drawdown:.2f}%")
    p.drawString(100, 690, f"Number of Trades: {num_trades}")

    # Add the plot image to the PDF
    p.drawImage(plot_file, 50, 400, width=500, height=300)  # Adjust position and size as needed

    p.showPage()
    p.save()

    return response


def calculate_total_roi(actual_prices, predicted_prices):
    # Filter out None values
    actual_prices = [price for price in actual_prices if price is not None]

    if not actual_prices:
        return 0  # or some appropriate value if there are no valid actual prices

    total_value = sum(actual_prices)  # Example logic
    total_return = total_value - sum(predicted_prices)  # Example logic

    roi = (total_return / total_value) * 100 if total_value != 0 else 0
    return roi

def calculate_max_drawdown(prices):
    peak = float('-inf')
    max_drawdown = 0

    for price in prices:
        if price is None:
            continue  # Skip None values

        if price > peak:
            peak = price
        drawdown = peak - price
        max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown