from datetime import datetime
from datetime import timedelta

from django.utils.dateparse import parse_date


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from .models import Transaction, Accessory, Clothing
from .forms import ClothingForm, AccessoryForm, DateForm, DeleteTransactionForm

@login_required
def index(request):
    #Display username on the top
    username = request.user.first_name.capitalize()
    #Hardcore Mr. Klein's username
    if(username == "Christopher"):
        username = "Mr. Klein"
    return render(request, 'store/index.html', {'username':username})

#Login Page
def login(request):
    message = ''
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('store:index'))
        else:
            message = "Incorrect Username-Password Combination"

    return render(request, 'store/login.html', {'message':message})

#View to purchase clothing item (any item with different sizes)
@login_required
def clothing(request):
    if request.method == 'POST':
        form = ClothingForm(request.POST)
        if form.is_valid():
            clothingtype = Clothing.objects.get(name=form.cleaned_data['clothing_type'])
            clothing_size = form.cleaned_data['size']

            #Preview before buying
            if 'preview' in request.POST:
                return render(request, 'store/clothingtransaction.html',{'form':form, 'clothingtype':clothingtype.name, 'clothingsize':clothing_size.upper()})

            #Clothing Type
            if 'submit' in request.POST:
                if clothing_size == 's':
                    clothingtype.s -= 1
                elif clothing_size == 'm':
                    clothingtype.m -= 1
                elif clothing_size == 'l':
                    clothingtype.l -= 1
                elif clothing_size == 'xl':
                    clothingtype.xl -= 1

                clothingtype.save()

                #Create New Transaction instance, for the records
                transaction = Transaction()
                transaction.pub_date=datetime.now()
                transaction.name=clothingtype.name
                transaction.cash = clothingtype.price
                transaction.user = request.user.first_name.capitalize()
                transaction.size=clothing_size
                transaction.save()
                request.session['confirmation'] = transaction.getConfirmation()
                return HttpResponseRedirect(reverse('store:confirmation')) #Go to the index
    else:
        form = ClothingForm()

    return render(request, 'store/clothingtransaction.html',{'form':form})

#View to purchase accessory (any item without size)
@login_required
def accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST)
        if form.is_valid():

            accessory_type = Accessory.objects.get(name=form.cleaned_data['accessory_type'])

            #Preview before purchase
            if 'preview' in request.POST:
                return render(request, 'store/accessorytransaction.html',{'form':form, 'accessorytype':accessory_type.name})

            #Execute the purchase
            if 'submit' in request.POST:
                accessory_type.inventory -= 1
                accessory_type.save()

                transaction = Transaction()
                transaction.pub_date=datetime.now()
                transaction.name=accessory_type.name
                transaction.cash = accessory_type.price
                transaction.user = request.user.first_name.capitalize()
                transaction.save()
                request.session['confirmation'] = transaction.getConfirmation()
                return HttpResponseRedirect(reverse('store:confirmation')) #Go to the confirmation page
    else:
        form = AccessoryForm()

    return render(request, 'store/accessorytransaction.html',{'form':form})

#Create tables visualizing tracsaction history
@login_required
def transactions(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            clothing_table = [] #Table for clotihng
            accessories_table = [] #Table for accessories
            transactions_table = [] #Table for transactions
            total_sales = 0 #Track the number of sales
            total_bank = 0 #Track the total revenue generated (Will be computed at the end from the sum of total_clothing_cash and total_accessory_cash)

            #Track the total number of each size sold and the clothing revenue
            total_small = 0
            total_medium = 0
            total_large = 0
            total_xlarge = 0
            total_clothing = 0
            total_clothing_cash = 0

            #Track the total number of accessories sold and the accessory revenue
            total_accessories = 0
            total_accessory_cash = 0

            #Start and end dates for the search
            from_date = form.cleaned_data['start_date']
            to_date = form.cleaned_data['end_date'] + timedelta(days = 1)

            #Pull transactions between the start and end dates
            transactions = Transaction.objects.filter(pub_date__range=[from_date,to_date]).order_by('-pub_date')
            for transaction in transactions:
                row = []
                row.append(transaction.name)
                row.append(transaction.size)
                row.append(transaction.pub_date)
                row.append(transaction.user)
                row.append('$'+format(transaction.cash,'.2f'))
                transactions_table.append(row)

            #From the transactions, populate the clothing table
            clothing_objects = Clothing.objects.all()
            for clothing in clothing_objects:
                #Initialize the row corresponding to the clothing item
                row = []
                row.append(clothing.name)
                small = medium = large = xlarge = 0

                #Tally the sizes of the items sold
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

                #The first four columns represent size
                row.append(small)
                row.append(medium)
                row.append(large)
                row.append(xlarge)
                sales = small+medium+large+xlarge

                #The next column represents the number of units sold
                row.append(sales)

                #The next column represents the total revenue generated from the clothing article
                cash = sales*clothing.price
                row.append('$'+format(cash,'.2f'))
                clothing_table.append(row)

                #Update overall counts
                total_small += small
                total_medium += medium
                total_large += large
                total_xlarge += xlarge
                total_clothing_cash += cash

            #From the transactions, populate the accessory table
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

            #Calcaulte total values
            total_clothing = total_small+total_medium+total_large+total_xlarge
            clothing_table.append(['Totals',total_small,total_medium,total_large,total_xlarge,total_clothing,'$'+format(total_clothing_cash,'.2f')])
            accessories_table.append(['Totals',total_accessories,'$'+format(total_accessory_cash,'.2f')])

            total_sales = total_clothing+total_accessories
            total_bank = '$'+format(total_clothing_cash+total_accessory_cash,'.2f')


    else:
        form = DateForm()

    return render(request, 'store/statistics.html',{'form':form,'transactions_table':transactions_table,'clothing_table':clothing_table,'accessories_table':accessories_table,'total_sales':total_sales,'total_bank':total_bank})

#View to choose start and end dates for the delete transaction View
#I had to separate the delete transaction view into two because I couldn't figure out/didn't invest enough time to do it in one
#Note: ONLY KLEIN CAN ACCESS THIS PAGE
@login_required
def choose_dates(request):
    if request.user.groups.filter(name="Mere Peasants").exists():
        return HttpResponseRedirect(reverse('store:not_authorized'))
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            request.session['from_date'] = str(form.cleaned_data['start_date'])
            request.session['to_date'] = str(form.cleaned_data['end_date'])
            #Redirect to the page for deleting transactions
            return HttpResponseRedirect(reverse('store:delete_transaction'))
    else:
        form = DateForm()

    return render(request,'store/choose_dates.html', {'form':form})

#View to delete transactions
#Note: ONLY KLEIN CAN ACCESS THIS PAGE
@login_required
def delete_transaction(request):

    #Redirect to choose dates page if no dates are in the session
    if not ("from_date" in request.session and "to_date" in request.session):
        return HttpResponseRedirect(reverse('store:choose_dates'))

    #Redirect if not Klein
    if request.user.groups.filter(name="Mere Peasants").exists():
        return HttpResponseRedirect(reverse('store:not_authorized'))


    parameters = [{'from_date':parse_date(request.session.get('from_date')), 'to_date':parse_date(request.session.get('to_date'))}]
    message = ""
    if request.method == 'POST':
        #Collect the from and to-date
        form = DeleteTransactionForm(request.POST,data = parameters)
        if form.is_valid():
            transaction = form.cleaned_data['transaction']

            if 'preview' in request.POST:
                return render(request,'store/delete_transaction.html', {'form':form, 'transaction':transaction})

            if 'submit' in request.POST:
                if transaction.size:
                    clothingtype = Clothing.objects.get(name=transaction.name)
                    size = transaction.size
                    if size == 's':
                        clothingtype.s+=1
                    if size == 'm':
                        clothingtype.m+=1
                    if size == 'l':
                        clothingtype.l+=1
                    if size == 'xl':
                        clothingtype.xl+=1
                    clothingtype.save()
                else:
                    accessorytype = Accessory.objects.get(name=transaction.name)
                    accessorytype.inventory += 1
                    accessorytype.save()

                message = "Successfully deleted transaction "+str(transaction)
                transaction.delete()
                form = DeleteTransactionForm(data = parameters)
    else:
        form = DeleteTransactionForm(data = parameters)

    return render(request,'store/delete_transaction.html', {'form':form, 'message':message})

#Logout
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:index'))

#Confirm purchase of an item
@login_required
def confirmation(request):
    text = request.session['confirmation']
    del request.session['confirmation']
    return render(request, "store/confirmation.html", {'text':text})

#Create tables of inventory
@login_required
def inventory(request):
    clothing_table = []
    accessory_table = []

    clothing = Clothing.objects.all()
    accessories = Accessory.objects.all()

    #Clothing inventory
    for item in clothing:
        row = []
        #Name
        row.append(item.name.upper())

        #Inventory for each size
        row.append(item.s)
        row.append(item.m)
        row.append(item.l)
        row.append(item.xl)

        #Total number of items
        row.append(item.s+item.m+item.l+item.xl)
        clothing_table.append(row)

    #Accessory inventory
    for item in accessories:
        row = []
        row.append(item.name.upper())
        row.append(item.inventory)
        accessory_table.append(row)

    return render(request, "store/inventory.html", {'clothing_table':clothing_table,'accessory_table':accessory_table})

#The not authorized view
def not_authorized(request):
    return render(request, "store/not_authorized.html")
