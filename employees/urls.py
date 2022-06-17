from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('checkin', views.CheckInView.as_view()),
    path('checkout', views.CheckoutView.as_view()),
    path('history', views.AttendenceHistoryView.as_view()),
]
