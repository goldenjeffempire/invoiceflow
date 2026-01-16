from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sales.models import Sale
from expenses.models import Expense
from django.db.models import Sum

@login_required
def report_summary(request):
    total_sales = Sale.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    net_profit = total_sales - total_expenses
    
    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }
    return render(request, 'reports/summary.html', context)