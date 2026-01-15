from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/add/', views.client_create, name='client_create'),
    path('invoices/', views.invoices_list, name='invoices_list'),
    path('invoices/add/', views.invoice_create, name='invoice_create'),
]
