from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.
class Transaction(models.Model):
    name = models.CharField(max_length = 50)
    size = models.CharField(max_length=10,null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    user = models.CharField(max_length=100)
    cash = models.FloatField()

    def __unicode__(self):
        date_string = str((self.pub_date).strftime('%m/%d/%y'))
        time_string = str((self.pub_date).strftime('%H:%M'))
        size_string = ""
        if self.size:
            size_string = "Size "+self.size.upper()+", "
        return self.name+", "+size_string+date_string+", "+time_string+", "+self.user

    def getConfirmation(self):
        date_string = str((self.pub_date).strftime('%m/%d/%y'))
        time_string = str((self.pub_date).strftime('%H:%M'))
        time_date = ".  The time is "+time_string+" on "+date_string
        output = "You have just completed a purchase of a "+self.name.lower()
        if(self.size):
            return output+" of size "+self.size.upper()+time_date
        else:
            return output+time_date

#Clothing With Sizes
class Clothing(models.Model):
    name = models.CharField(max_length=50);

    #Inventory Variables
    s = models.IntegerField(default = 0)
    m = models.IntegerField(default = 0)
    l = models.IntegerField(default = 0)
    xl = models.IntegerField(default = 0)

    price = models.FloatField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Clothing"

class Accessory(models.Model):
    name = models.CharField(max_length=50);

    inventory = models.IntegerField(default = 0)

    price = models.FloatField()

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Accessories"
