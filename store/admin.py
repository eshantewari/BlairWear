from django.contrib import admin

# Register your models here.

from .models import Transaction, Accessory, Clothing

class TransactionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['name', 'size' ,'user','cash']}),
		('Date information', {'fields': ['pub_date']}),
	]
	list_display = ('name', 'size' ,'user','cash','pub_date')
	list_filter = ['pub_date']
	search_fields = ['pub_date']

class ClothingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'price' ,'s','m','l','xl']}),
    ]
    list_display = ('name', 'price' ,'s','m','l','xl')
    list_filter = ['name']
    search_fields = ['name']
    
class AccesoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'price' , 'inventory']}),
    ]
    list_display = ('name', 'price' ,'inventory')
    list_filter = ['name']
    search_fields = ['name']
    
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Accessory, AccesoryAdmin)
admin.site.register(Clothing, ClothingAdmin)
    
