from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sale
from .forms import SaleForm

# type: ignore
@login_required
def sale_list(request):
    sales = Sale.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sales/sale_list.html', {'sales': sales})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            return redirect('sales:sale_list')
    else:
        form = SaleForm()
    return render(request, 'sales/sale_form.html', {'form': form})
