from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Transaction, Accessory, Clothing
from .forms import ClothingForm, AccessoryForm

@login_required
def index(request):
    return render(request, 'store/index.html')

@login_required
def clothing(request):
    if request.method == 'POST':
        form = ClothingForm(request.POST)
        if form.is_valid():
            clothingtype = Clothing.objects.get(name=form.cleaned_data['clothing_type'])
            clothing_size = form.cleaned_data['size']
            if clothing_size == 'Small':
                clothingtype.small -= 1
            elif clothing_size == 'Medium':
                clothingtype.medium -= 1
            elif clothing_size == 'Large':
                clothingtype.large -= 1
            elif clothing_size == 'XLarge':
                clothingtype.xlarge -= 1
            
            clothingtype.save()
            
            
            transaction = Transaction()
            transaction.pub_date=timezone.now()
            transaction.clothingType=clothingtype.name
            transaction.cash = clothingtype.price
            transaction.user = request.user.get_username()
            transaction.size=clothing_size
            transaction.save()            
            return HttpResponseRedirect(reverse('store:index')) #Go to the index
    else:
        form = ClothingForm()
    
    return render(request, 'store/clothingtransaction.html',{'form':form})

@login_required
def accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST)
        if form.is_valid():
            accessory_type = Accessory.objects.get(name=form.cleaned_data['accessory_type'])
            accessory_type.inventory -= 1            
            accessory_type.save()     
            
            transaction = Transaction()
            transaction.pub_date=timezone.now()
            transaction.clothingType=accessory_type.name
            transaction.cash = accessory_type.price
            transaction.user = request.user.get_username()
            transaction.save()            
            return HttpResponseRedirect(reverse('store:index')) #Go to the index
    else:
        form = AccessoryForm()
    
    return render(request, 'store/accessorytransaction.html',{'form':form})

@login_required 
def transactions(request):
    return render(request, 'store/index.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:index'))


