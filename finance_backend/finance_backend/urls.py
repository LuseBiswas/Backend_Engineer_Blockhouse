# finance_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stocks.urls')),  # Include stocks app URLs
    path('stocks/', include('stocks.urls')),
]
