from django.urls import path
from .views import expenses_dashboard, expense_add

app_name = 'expenses'

urlpatterns = [
    path('', expenses_dashboard, name='dashboard'),
    path('add/', expense_add, name='add')
]
