from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("predict_with_text", views.predict_with_text, name="predict_with_text"),
    path("predict_with_twitter_handle", views.predict_with_twitter_handle, name="predict_with_twitter_handle"),
    path("use_app", views.use_app, name="use_app"),  
]