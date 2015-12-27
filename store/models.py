from __future__ import unicode_literals

import datetime 
from django.db import models

# Create your models here.
class Transaction(models.Model):
    name = models.CharField(max_length = 50)
    size = models.CharField(max_length=10,null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    user = models.CharField(max_length=100)
    cash = models.FloatField()    

#Clothing With Sizes
class Clothing(models.Model):
    name = models.CharField(max_length=50);
       
    #Inventory Variables
    s = models.IntegerField(default = 0)
    m = models.IntegerField(default = 0)
    l = models.IntegerField(default = 0)
    xl = models.IntegerField(default = 0)
    
    price = models.FloatField()
    class Meta:
        verbose_name_plural = "Clothing"
    
class Accessory(models.Model):
    name = models.CharField(max_length=50);
       
    inventory = models.IntegerField(default = 0)
    
    price = models.FloatField()
    class Meta:
        verbose_name_plural = "Accessories"
    
    
        
        

    
            
            
    
    
