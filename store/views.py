from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template import RequestContext

from .models import Transaction, Accessory, Clothing
from .forms import ClothingForm, AccessoryForm, DateForm

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
            if clothing_size == 's':
                clothingtype.s -= 1
            elif clothing_size == 'm':
                clothingtype.m -= 1
            elif clothing_size == 'l':
                clothingtype.l -= 1
            elif clothing_size == 'xl':
                clothingtype.xl -= 1
            
            clothingtype.save()
            
            
            transaction = Transaction()
            transaction.pub_date=timezone.now()
            transaction.name=clothingtype.name
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
            transaction.name=accessory_type.name
            transaction.cash = accessory_type.price
            transaction.user = request.user.get_username()
            transaction.save()            
            return HttpResponseRedirect(reverse('store:index')) #Go to the index
    else:
        form = AccessoryForm()
    
    return render(request, 'store/accessorytransaction.html',{'form':form})

@login_required 
def transactions(request):
    clothing_table = []
    accessories_table = []
    transactions_table = []
    total_sales = 0
    total_bank = 0    
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            total_small = 0
            total_medium = 0
            total_large = 0
            total_xlarge = 0
            total_clothing = 0
            total_clothing_cash = 0
            total_accessories = 0
            total_accessory_cash = 0

            from_date = form.cleaned_data['start_date']
            to_date = form.cleaned_data['end_date']
            
            transactions = Transaction.objects.filter(pub_date__range=[from_date,datetime.today()])      
            for transaction in transactions:
                row = []
                row.append(transaction.name)
                row.append(transaction.size)
                row.append(transaction.pub_date)
                row.append(transaction.user)
                row.append('$'+format(transaction.cash,'.2f'))
                transactions_table.append(row)
            
            
            clothing_objects = Clothing.objects.all()
            for clothing in clothing_objects:
                row = []
                row.append(clothing.name)
                small = medium = large = xlarge = 0
                for transaction in transactions:
                    if transaction.name == clothing.name:
                        if transaction.size == 's':
                            small+=1
                        if transaction.size == 'm':
                            medium+=1
                        if transaction.size == 'l':
                            large+=1
                        if transaction.size == 'xl':
                            xlarge+=1
                row.append(small)
                row.append(medium)
                row.append(large)
                row.append(xlarge)
                sales = small+medium+large+xlarge
                row.append(sales)
                cash = sales*clothing.price
                row.append('$'+format(cash,'.2f'))                            
                clothing_table.append(row)
                total_small += small
                total_medium += medium
                total_large += large
                total_xlarge += xlarge
                total_clothing_cash += cash
        

            accessory_objects = Accessory.objects.all()
            for accessory in accessory_objects:
                row = []
                row.append(accessory.name)
                sales = 0
                for transaction in transactions:
                    if transaction.name == accessory.name:
                        sales += 1
   
                row.append(sales)
                cash = sales*accessory.price
                row.append('$'+format(cash,'.2f'))                            
                accessories_table.append(row)
                total_accessories += sales
                total_accessory_cash += cash
            
            total_clothing = total_small+total_medium+total_large+total_xlarge    
            clothing_table.append(['Totals',total_small,total_medium,total_large,total_xlarge,total_clothing,'$'+format(total_clothing_cash,'.2f')])
            accessories_table.append(['Totals',total_accessories,'$'+format(total_accessory_cash,'.2f')])
            
            total_sales = total_clothing+total_accessories
            total_bank = '$'+format(total_clothing_cash+total_accessory_cash,'.2f')       
            
                
    else:
        form = DateForm()
            
    return render_to_response('store/statistics.html',{'form':form,'transactions_table':transactions_table,'clothing_table':clothing_table,'accessories_table':accessories_table,'total_sales':total_sales,'total_bank':total_bank},context_instance=RequestContext(request))

    
    

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:index'))


