from django.urls import path
from .views import index, user_logout, user_register, user_login

urlpatterns = [
    path('', index, name="index"),
    path('login', user_login, name="login"),
    path('register', user_register, name="register"),
    path('logout', user_logout, name="logout")
]
