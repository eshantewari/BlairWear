from django import forms
from django.core.exceptions import ValidationError
from django.forms.extras.widgets import SelectDateWidget
from .models import Transaction, Accessory, Clothing
from datetime import datetime

class DateForm(forms.Form):
    start_date = forms.DateField(required = True, label = 'View Transactions From ', widget = SelectDateWidget)
    end_date = forms.DateField(initial = datetime.now, required = True, label = 'To ', widget = SelectDateWidget)

class ClothingForm(forms.Form):
    SIZES = (
        ('s', 's'),
        ('m', 'm'),
        ('l', 'l'),
        ('xl', 'xl'),
    )
    clothing_type = forms.ModelChoiceField(queryset=Clothing.objects.all(), required=True)
    size = forms.ChoiceField(choices=SIZES, required=True, label='Size')

    def clean(self):
        clothingtype  = Clothing.objects.get(name=self.cleaned_data['clothing_type'])
        clothing_size = self.cleaned_data['size']
        error = "The inventory for the selected clothing type-size combination is at 0.  Update and come back. "
        if clothing_size == 's':
            if clothingtype.s == 0:
                raise ValidationError(error)
                return self.cleaned_data
        elif clothing_size == 'm':
            if clothingtype.m == 0:
                raise ValidationError(error)
                return self.cleaned_data
        elif clothing_size == 'l':
            if clothingtype.l == 0:
                raise ValidationError(error)
                return self.cleaned_data
        elif clothing_size == 'xl':
            if clothingtype.xl == 0:
                raise ValidationError(error)
                return self.cleaned_data

class AccessoryForm(forms.Form):

    accessory_type = forms.ModelChoiceField(queryset=Accessory.objects.all(), required=True)

    def clean(self):
        accessoryType  = Accessory.objects.get(name=self.cleaned_data['accessory_type'])
        error = "The inventory for the selected accessory type is at 0.  If you are holding said accessory, that is a problem. "
        if accessoryType.inventory == 0:
            raise ValidationError(error)
            return self.cleaned_data

class DeleteTransactionForm(forms.Form):
    def __init__(self,*args,**kwargs):
        dates = kwargs.pop('data', None)
        from_date = dates[0]['from_date']    # from_date is the parameter passed from views.py
        to_date = dates[0]['to_date']
        super(DeleteTransactionForm, self).__init__(*args,**kwargs)
        self.fields['transaction'] = forms.ModelChoiceField(Transaction.objects.filter(pub_date__range=[from_date,to_date]))
