from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('profile/', views.profile_settings, name='profile'),
]
