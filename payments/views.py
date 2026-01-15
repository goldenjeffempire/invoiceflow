from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPaymentSettings
from .forms import PaymentSettingsForm

@login_required
def payment_settings_view(request):
    settings_obj, created = UserPaymentSettings.objects.get_or_create(user=request.user)
    form = PaymentSettingsForm(request.POST or None, instance=settings_obj)
    
    if form.is_valid():
        form.save()
        return redirect('payments:payment_settings')
    
    return render(request, 'settings/payment_settings.html', {'form': form})
