from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('profile', views.profile),
    path('post_message', views.post_message),
    path('post_comment/<int:message_id>', views.post_comment),
    path('logout', views.logout),
]
