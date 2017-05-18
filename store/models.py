from __future__ import unicode_literals

from datetime import datetime
from django.db import models

#Chief Flaw: Adding a new clothing size requires rewriting a fair portion of the source code
#However, it is very easy to add new clothing items in the Django Admin page

#The clothing model keeps inventory of all items that have sizes
class Clothing(models.Model):
    name = models.CharField(max_length=50) #The name of the clothing item

    #Inventory Variables
    s = models.IntegerField(default = 0) #The number of small items in inventory
    m = models.IntegerField(default = 0) #The number of medium items in inventory
    l = models.IntegerField(default = 0) #The number of large items in inventory
    xl = models.IntegerField(default = 0) #The number of xl items in inventory

    price = models.FloatField() #Price of the item

    def __unicode__(self):
        return self.name

    #For the Django Admin Page
    class Meta:
        verbose_name_plural = "Clothing"

#The clothing model keeps inventory of all items that do not have sizes
class Accessory(models.Model):
    name = models.CharField(max_length=50) #The name of the item

    inventory = models.IntegerField(default = 0) #The number of unites remaining

    price = models.FloatField() #The price of the item

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Accessories"


#The trasaction model maintains a log of all transactions that have occured
class Transaction(models.Model):
    name = models.CharField(max_length = 50) #The name of the item sold
    size = models.CharField(max_length=10,null=True, blank=True) #Clothing size (can be null because accessories don't have associated sizes)
    pub_date = models.DateTimeField('date published') #The date of the transaction
    user = models.CharField(max_length=100) #The vendor
    cash = models.FloatField() #The money exchanged

    #The to-sring method (might be depracated)
    def __unicode__(self):
        date_string = str((self.pub_date).strftime('%m/%d/%y'))
        time_string = str((self.pub_date).strftime('%H:%M'))
        size_string = ""
        if self.size:
            size_string = "Size "+self.size.upper()+", "
        return self.name+", "+size_string+date_string+", "+time_string+", "+self.user

    #For the confirmation aspect of the transaction
    def getConfirmation(self):
        date_string = str((self.pub_date).strftime('%m/%d/%y'))
        time_string = str((self.pub_date).strftime('%H:%M'))
        time_date = ".  The time is "+time_string+" on "+date_string
        output = "You have just completed a purchase of a "+self.name.lower()
        if(self.size):
            return output+" of size "+self.size.upper()+time_date
        else:
            return output+time_date
