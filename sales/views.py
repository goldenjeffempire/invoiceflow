from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sale
from .forms import SaleForm
from django.db.models import Sum
from datetime import date, timedelta

@login_required
def sales_dashboard(request):
    sales = Sale.objects.filter(user=request.user).order_by('-date')
    # Aggregate for charts
    today = date.today()
    weekly = Sale.objects.filter(user=request.user, date__gte=today - timedelta(days=7)).aggregate(total=Sum('amount'))['total'] or 0
    monthly = Sale.objects.filter(user=request.user, date__month=today.month).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'dashboard/sales.html', {'sales': sales, 'weekly': weekly, 'monthly': monthly})

@login_required
def sale_add(request):
    form = SaleForm(request.POST or None)
    if form.is_valid():
        sale = form.save(commit=False)
        sale.user = request.user
        sale.save()
        return redirect('sales:dashboard')
    return render(request, 'dashboard/sale_form.html', {'form': form})
