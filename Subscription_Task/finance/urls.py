from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path('', views.index, name="home"),
    path('register', views.theregister, name="register"),
    path('login', views.thelogin, name="login"),
    path('logout', views.thelogout, name="logout"),
    path('pricing', views.pricing, name="pricing"),
    path('profile/<user_id>', views.profile, name="profile"),
    path('subscribe/<plan>', views.subscribe, name="subscribe"),
    path('unsubscribe/<plan>', views.unsubscribe, name="unsubscribe"),
]
