from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_worker/", AddWorkerView.as_view(), name="add_worker"),
    path("add_work/", AddWorkView.as_view(), name="add_work"),
    path("status_work/", status_work, name="status_work"),
    path("send_sms/", sms_send, name="sms_send"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
