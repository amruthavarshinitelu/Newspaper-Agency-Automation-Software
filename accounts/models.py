import profile
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "logo.wepg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    Area= models.CharField(max_length=200)
    door_number= models.IntegerField(null=True)
    no_of_days=models.IntegerField(null=True)
    is_active=models.BooleanField(default=False,null=True)
    bill_option=models.BooleanField(default=False,null=True)
    Amount= models.IntegerField(default=0)
    previous_Amount= models.IntegerField(default=0,blank=True)
    previous2months_Amount= models.IntegerField(default=0,blank=True)
    def __str__(self):
      return self.name
     
class Deliveryagent(models.Model):
    user = models.OneToOneField(User,null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "logo.wepg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    salary_option=models.BooleanField(default=False,null=True)
    salary=models.IntegerField(default=0,blank=True)
    # city = models.CharField(max_length=200,null=True)
    # zipcode = models.FloatField()

    def __str__(self):
      return self.name

class Manager(models.Model):
    user = models.OneToOneField(User,null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "logo.wepg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # gender = models.CharField(max_length= 10, null= True)
    # dob = models.CharField(max_length=20, null= True)

    def __str__(self):
      return self.name	
      
class Publication(models.Model):
    paper_name=models.CharField(max_length=200)
    price=models.FloatField(null=True)
    
    def __str__(self):
    	return self.paper_name
    	

class Subscription(models.Model):
    
    Customer = models.ForeignKey(Customer, null= True, blank= True, on_delete= models.SET_NULL)
    publication =  models.ForeignKey(Publication, null= True, on_delete= models.SET_NULL)   
    date_created = models.DateTimeField(auto_now_add=True) 
    
    #complete = models.BooleanField(default=False, null= True)
    def __str__(self):
        return str(self.Customer)
    
    @property
    def get_subscription_items(self):
        subscribeitems=self.subscribeitem_set.all()
        total=sum([item.quantity for item in subscribeitems])
        return total;
       
    @property
    def get_subscription_total(self):
        subscribeitems=self.subscribeitem_set.all()
        total=sum([item.get_total for item in subscribeitems])*30
        return total;
    
        
class SubscribeItem(models.Model):
    Customer = models.ForeignKey(Customer, null= True, blank= True, on_delete= models.SET_NULL)
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    Area= models.CharField(max_length=200,null=True)
    door_number= models.IntegerField(null=True)
    
    @property
    def get_total(self):
        total=self.publication.price * self.quantity
        return total

class customer_bill(models.Model):
    
    Amount= models.IntegerField(default=0, null=True, blank=True)
    previous_Amount= models.IntegerField(default=0, null=True, blank=True)
    previous2months_Amount= models.IntegerField(default=0, null=True, blank=True)
    

