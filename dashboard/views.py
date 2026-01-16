from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice, Client
from sales.models import Sale
from expenses.models import Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json

@login_required
def home(request):
    user = request.user
    invoices = Invoice.objects.filter(user=user)
    clients_count = Client.objects.filter(user=user).count()
    
    total_sales = Sale.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    recent_invoices = invoices.order_by('-created_at')[:5]
    
    # Chart data: Sales vs Expenses by month
    sales_by_month = Sale.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    expenses_by_month = Expense.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    
    months = []
    sales_data = []
    expenses_data = []
    
    # Combine data for charts
    month_map = {}
    for entry in sales_by_month:
        m = entry['month'].strftime('%b %Y')
        month_map[m] = {'sales': float(entry['total']), 'expenses': 0}
        
    for entry in expenses_by_month:
        m = entry['month'].strftime('%b %Y')
        if m not in month_map:
            month_map[m] = {'sales': 0, 'expenses': float(entry['total'])}
        else:
            month_map[m]['expenses'] = float(entry['total'])
            
    sorted_months = sorted(month_map.keys()) # Simplified sorting
    for m in sorted_months:
        months.append(m)
        sales_data.append(month_map[m]['sales'])
        expenses_data.append(month_map[m]['expenses'])

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': total_sales - total_expenses,
        'clients_count': clients_count,
        'recent_invoices': recent_invoices,
        'chart_labels': json.dumps(months),
        'chart_sales': json.dumps(sales_data),
        'chart_expenses': json.dumps(expenses_data),
    }
    return render(request, 'dashboard/home.html', context)
