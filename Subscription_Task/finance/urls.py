from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path('', views.index, name="home"),
    path('register', views.Theregister, name="register"),
    path('login', views.Thelogin, name="login"),
    path('logout', views.Thelogout, name="logout"),
]
