from django.urls import path
from .views import *

urlpatterns = [
    path("today/", WorkListAPIView.as_view(), name="today"),
    path("history_days/", HistoryAPIView.as_view(), name="history"),
]
