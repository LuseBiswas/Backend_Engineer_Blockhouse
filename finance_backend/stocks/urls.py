# stocks/urls.py

from django.urls import path
from .views import fetch_stock_data, backtest_strategy, predict_stock_prices, generate_report

urlpatterns = [
    path('fetch/<str:symbol>/', fetch_stock_data, name='fetch_stock_data'),
    path('backtest/', backtest_strategy, name='backtest_strategy'),
    path('predict/<str:symbol>/', predict_stock_prices, name='predict_stock_prices'),
     path('report/', generate_report, name='generate_report'),
]
