from django.db import models
from enum import Enum
from django.contrib.postgres.fields import ArrayField

class user(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class ftype(models.Model):
    title = models.CharField(max_length=150)
    abbreviation = models.CharField(max_length=150)	
    ctype = models.CharField(max_length=150)	
    alias_name = ArrayField(models.CharField(max_length=100, blank=True),size=50,null=True,blank=True)  
    createdate = models.DateTimeField()
    bActive = models.BooleanField(default=True)

class ctype_data(models.Model):
    title = models.CharField(max_length=150)
    fcategoryid= models.ForeignKey(ftype,on_delete=models.CASCADE,null=True,blank=True)
    abbreviation = models.CharField(max_length=150,null=True,blank=True)
    h_abbreviation = models.CharField(max_length=150,null=True,blank=True)
    tm_abbreviation = models.CharField(max_length=150,null=True,blank=True)
    tel_abbreviation = models.CharField(max_length=150,null=True,blank=True)
    guj_abbreviation = models.CharField(max_length=150,null=True,blank=True)
    ben_abbreviation = models.CharField(max_length=150,null=True,blank=True)
    ctype = models.CharField(max_length=150)
    alias_name = ArrayField(models.CharField(max_length=100, blank=True),size=50,null=True,blank=True)
    createdate = models.DateTimeField(auto_now=True)
    bActive = models.BooleanField(default=True)
    showOnList  = models.BooleanField(default=True)
   

class broiler_type(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)	
    abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    h_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    tm_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    tel_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    guj_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    ben_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    alias_name = ArrayField(models.CharField(max_length=100, blank=True),size=50,null=True,blank=True)  
    priority = models.IntegerField()	
    createdate = models.DateTimeField(auto_now=True)
    bActive = models.BooleanField(default=True)   

class Status(Enum):
    N = 'N'
    C = 'C'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values(cls):
        return [key.value for key in cls]

    def __str__(self):
        return self.value    

class broiler_region(models.Model):
    regionid = models.IntegerField() 
    ctype = models.ForeignKey(ctype_data,on_delete=models.CASCADE,null=True,blank=True)
    bfluctulate = models.IntegerField() 
    bnecc = models.IntegerField() 
    rateview = models.CharField(max_length=1, choices=Status.choices(),null=True,blank=True)
    region = models.CharField(max_length=100,null=True,blank=True)		
    abbreviation = models.CharField(max_length=50,null=True,blank=True)		
    zone = models.CharField(max_length=50,null=True,blank=True)			
    broilertype_c = models.CharField(max_length=200,null=True,blank=True)	
    broilertype = models.ForeignKey(broiler_type, on_delete=models.CASCADE,null=True,blank=True)
    timeslot = models.CharField(max_length=50,null=True,blank=True)			
    alias_name = ArrayField(models.CharField(max_length=100, blank=True),size=50,null=True,blank=True) 
    bActive = models.BooleanField(default=True)
        
class state_data(models.Model):
    state = models.CharField(max_length=100,null=True,blank=True)	
    abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    h_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    tm_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    tel_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    guj_abbreviation = models.CharField(max_length=100,null=True,blank=True)	
    ben_abbreviation = models.CharField(max_length=100,null=True,blank=True)
    alias_name = ArrayField(models.CharField(max_length=100, blank=True),size=50,null=True,blank=True)  
    bActive = models.BooleanField(default=True)	        
        
    

