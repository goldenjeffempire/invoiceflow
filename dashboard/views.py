from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice, Client
from sales.models import Sale
from expenses.models import Expense
from django.db.models import Sum

@login_required
def home(request):
    user = request.user
    invoices = Invoice.objects.filter(user=user)
    clients_count = Client.objects.filter(user=user).count()
    
    total_sales = Sale.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    recent_invoices = invoices.order_by('-created_at')[:5]
    
    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': total_sales - total_expenses,
        'clients_count': clients_count,
        'recent_invoices': recent_invoices,
    }
    return render(request, 'dashboard/home.html', context)
