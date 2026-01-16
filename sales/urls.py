from django.urls import path
from .views import sales_dashboard, sale_add

app_name = 'sales'

urlpatterns = [
    path('', sales_dashboard, name='dashboard'),
    path('add/', sale_add, name='add')
]
