# stocks/models.py

from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)  # Stock symbol like AAPL
    date = models.DateField()  # Date of stock data
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.symbol} - {self.date}"


class BacktestResult(models.Model):
    symbol = models.CharField(max_length=10)
    total_return = models.FloatField()
    max_drawdown = models.FloatField()
    trades_executed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.total_return}%"
    


class StockPrediction(models.Model):
    symbol = models.CharField(max_length=10)  # E.g., 'AAPL'
    predicted_price = models.FloatField()      # Store the predicted price
    actual_price = models.FloatField(null=True, blank=True)
    day = models.IntegerField()                 # Day of the prediction (1 for the first predicted price, etc.)
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the prediction was made

    def __str__(self):
        return f"{self.symbol} - Day {self.day}: {self.predicted_price}"
