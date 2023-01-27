from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("history/", views.HistoryView.as_view(), name="history"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # for ajax
    path("ajax_work_counter/<int:id>", views.list_work_counter, name="ajax_work_count"),
]
