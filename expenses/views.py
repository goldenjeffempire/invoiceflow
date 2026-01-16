from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from datetime import date, timedelta

@login_required
def expenses_dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    today = date.today()
    weekly = Expense.objects.filter(user=request.user, date__gte=today - timedelta(days=7)).aggregate(total=Sum('amount'))['total'] or 0
    monthly = Expense.objects.filter(user=request.user, date__month=today.month).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'dashboard/expenses.html', {'expenses': expenses, 'weekly': weekly, 'monthly': monthly})

@login_required
def expense_add(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('expenses:dashboard')
    return render(request, 'dashboard/expense_form.html', {'form': form})
