from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sales.models import Sale
from expenses.models import Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json

# type: ignore
@login_required
def report_summary(request):
    user = request.user
    total_sales = Sale.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    net_profit = total_sales - total_expenses

    # Monthly breakdown for charts
    sales_by_month = Sale.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    expenses_by_month = Expense.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')

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

    sorted_months = sorted(month_map.keys())
    months = [m for m in sorted_months]
    sales_data = [month_map[m]['sales'] for m in sorted_months]
    expenses_data = [month_map[m]['expenses'] for m in sorted_months]
    
    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'chart_labels': json.dumps(months),
        'chart_sales': json.dumps(sales_data),
        'chart_expenses': json.dumps(expenses_data),
    }
    return render(request, 'reports/summary.html', context)