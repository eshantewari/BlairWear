from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction, Accessory, Clothing

class ClothingForm(forms.Form):
    TYPES = (
        ('Hoodie', 'Hoodie'),
        ('Sweatpant', 'Sweatpant'),
        ('Tee', 'Tee'),
        ('Crewneck', 'Crewneck'),
    )
    SIZES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('XLarge', 'XLarge'),
    )
    clothing_type = forms.ChoiceField(choices=TYPES, required=True, label='Clothing Type')
    size = forms.ChoiceField(choices=SIZES, required=True, label='Sizes')
    
    def clean(self):        
        clothingtype  = Clothing.objects.get(name=self.cleaned_data['clothing_type'])
        clothing_size = self.cleaned_data['size']
        error = "The inventory for the selected clothing type-size combination is at 0.  Update and come back. "
        if clothing_size == 'Small':
            if clothingtype.small == 0:
                raise ValidationError(error)
                return self.cleaned_data
        elif clothing_size == 'Medium':
            if clothingtype.medium == 0:
                raise ValidationError(error)
                return self.cleaned_data
        elif clothing_size == 'Large':
            if clothingtype.large == 0:
                raise ValidationError(error)
                return self.cleaned_data
        elif clothing_size == 'XLarge':
            if clothingtype.xlarge == 0:
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