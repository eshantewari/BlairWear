from django import forms
from django.core.exceptions import ValidationError
from django.forms.extras.widgets import SelectDateWidget
from .models import Transaction, Accessory, Clothing


class DateForm(forms.Form):
    start_date = forms.DateField(required = True, label = 'View Statistics From ', widget = SelectDateWidget)
    end_date = forms.DateField(required = True, label = 'To ', widget = SelectDateWidget)

class ClothingForm(forms.Form):
    TYPES = (
        ('Hoodie', 'Hoodie'),
        ('Sweatpant', 'Sweatpant'),
        ('Tee', 'Tee'),
        ('Crewneck', 'Crewneck'),
    )
    SIZES = (
        ('s', 's'),
        ('m', 'm'),
        ('l', 'l'),
        ('xl', 'xl'),
    )
    clothing_type = forms.ChoiceField(choices=TYPES, required=True, label='Clothing Type')
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
    TYPES = (
        ('Beanie', 'Beanie'),
    )
    accessory_type = forms.ChoiceField(choices=TYPES, required=True, label='Accessory Types')
    
    def clean(self):        
        accessoryType  = Accessory.objects.get(name=self.cleaned_data['accessory_type'])
        error = "The inventory for the selected accessory type-size combination is at 0.  Update and come back. "
        if accessoryType.inventory == 0:
            raise ValidationError(error)
            return self.cleaned_data