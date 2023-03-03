from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path('', views.index, name="home"),
    path('register', views.register, name="register"),
]
