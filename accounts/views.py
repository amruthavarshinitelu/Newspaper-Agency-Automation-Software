import re
from django.shortcuts import render,redirect
from django.http import HttpResponse
from matplotlib.style import context
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, logout,login
from .models import *
from .forms import CustomerForm

from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only


from django.core.mail import send_mail
from django.conf import settings

import json
from django.http import JsonResponse
from datetime import datetime,timedelta

stored_date = datetime.now()
ar=-1	

@unauthenticated_user
def registerpage(request):
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['mobile_number']
        Area = request.POST['Area']
        doornumber = request.POST['door_number']
        
        if len(password) <8:
            messages.error(request,'Password is too short')
            return redirect('register')
            
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:


                myuser = User.objects.create_user(username = username,email = email,password = password)
                myuser.number = number
               
                myuser.save()
                
                group = Group.objects.get(name = 'customer')
                myuser.groups.add(group)
                
                Customer.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    Area=Area,
                    door_number=doornumber,
                    
                    # phone = instance.mobile_number
                )
                
                
                subject = 'Thank you for using'
                message = 'Welcome to NAAS! we are very proud to have you'
                from_email = settings.EMAIL_HOST_USER
                print(myuser.email)
                to_list = [myuser.email, 'sivasaiyeswanth@gmail.com']
                # send_mail(subject, message, from_email, to_list, fail_silently= True)
                
                
                    
                messages.success(request, 'Customer Account created for '+username)
                return redirect('login')
            
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
            
            
        
            
        
            
    context = {}
    return render(request,'accounts/register.html', context)
    
 
   

def register_manager(request):
    
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['mobile_number']
        address = request.POST['address']
        gender = request.POST['gender']
        dob = request.POST['DOB']
        
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:
        
       
                myuser = User.objects.create_user(username = username,email = email,password = password)
                myuser.number = number
                myuser.address = address
                # myuser.gender = gender
                # myuser.dob = dob
                myuser.save()
                
                group = Group.objects.get(name = 'manager')
                myuser.groups.add(group)
                
                Manager.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    # phone = instance.mobile_number
                )
                
                messages.success(request, 'Manager Account created for '+username)
                
                return redirect('login')
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')

    
    context = {}
    return render(request,'accounts/mregister.html', context)



def register_deliveryagent(request):
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['mobile_number']
        address = request.POST['address']
        
        
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:
                myuser = User.objects.create_user(username = username,password = password)
                myuser.number = number
                myuser.email = email
                myuser.address = address
                
                myuser.save()
                
                group = Group.objects.get(name='deliveryagent')
                myuser.groups.add(group)
                
                Deliveryagent.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    
                    # phone = instance.mobile_number
                )
                
                
                    
                messages.success(request, 'Delivery Agent Account created for '+username)
                
                return redirect('login')
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
                
            
    context = {}
    return render(request,'accounts/deliveryagent.html', context)

@unauthenticated_user
def loginpage(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password) 
        
        if user is not None:
            login(request,user)
            return redirect('managerdashboard')
        else:
            messages.info(request,'Username or password is incorrect')
        
    context = {}
    return render(request,'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@admin_only
def home(request):
    #orders = Order.objects.all()
    customers = Customer.objects.all()
    deliveryagent = Deliveryagent.objects.all()
    
    
    #total_orders = orders.count()
    total_customers = customers.count()
    
    #delivered = orders.filter(status = 'Delivered').count()
    #pending  = orders.filter(status = 'Pending').count()
    
    
    context = { 'customers' : customers, 'deliveryagents': deliveryagent, 'total_customers':total_customers,}
    return render(request, 'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['deliveryagent'])
def deliveryagent_home(request):
    context = {}
    return render(request, 'accounts/deliveryagenthome.html', context)

def cancel(request):
    customer=request.user.customer
    if request.user.is_authenticated:
        amount=None
       # print(1000)
       # amount = request.POST.get('Amount')
       # print(amount)
        #customer.Amount=amount
        if request.method == 'POST':
             amount = request.POST.get("Amount")
        if amount is not None:
        
             customer.Amount=amount
             print(amount)
             customer.save()
        subscription, created = Subscription.objects.get_or_create(Customer=customer)
        items=subscription.subscribeitem_set.all()
      
    else:
        items=[]
        
        subscriptions={'get_subscription_total':0,'get_subsription_items':0}
    context = {'items':items, 'subscription':subscription}
    
    return render(request, 'accounts/cancel.html', context)
   
def customer_bill(request):
    context = {}
    return render(request, 'accounts/customer_bill', context)
def payment(request):
    customer=request.user.customer
  
    subscription, created = Subscription.objects.get_or_create(Customer=customer)
    due=subscription.get_subscription_total-customer.Amount
    customer.previous_Amount=due
    customer.save()
    if customer.previous_Amount > 0:
         customer.is_active=True
    else:
         customer.is_active=False
    customer.save()
    context={'x':customer.Amount,'y':due}
    return render(request, 'accounts/payment.html', context)
def manager_view(request):
    context = {}
    return render(request, 'accounts/manager_view.html', context)
def item(request):
    context = {}
    return render(request, 'accounts/item.html', context)

@allowed_users(allowed_roles=['customer'])
def buyer(request):
    context={}
    return render(request, 'accounts/buyer.html',context)

@admin_only
def managerdashboard(request):
    
    customers = Customer.objects.all()
    deliveryagent = Deliveryagent.objects.all()
    #products = Product.objects.all()
    total_customers = customers.count()
    total_deliveryagents = deliveryagent.count()
    #orders = Order.objects.all()
    publications=Publication.objects.all()
    
    context = {'customers':customers, 'deliveryagent':deliveryagent, 'total_customers': total_customers, 'total_deliveryagents': total_deliveryagents,'publications':publications}
    
    
    return render(request, 'accounts/manager_view.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def addpublication(request):
    
    manager=request.user.manager
    
    if request.method == 'POST':
        
        itemname = request.POST['itemname']
        
        itemprice = request.POST['itemprice']
       
        
       
        Publication.objects.create(paper_name=itemname,price=itemprice)
        

        #publication.save()
        
        # print(product)
        
    
        
    context = {}
    return render(request, 'accounts/manager_Add_publication.html', context)
 

def buyer(request):
    context={}
    return render(request, 'accounts/buyer.html',context)

@login_required
def generate_bill(request):
    if request.method == 'POST':
        # perform bill generation logic here
        customers = Customer.objects.all()
        deliveryagent = Deliveryagent.objects.all()
        print("hello")
        for customer in customers:
            customer.bill_option = True
            customer.save()
        for agent in delivery_agents:
            agent.salary_option = True
            agent.save()

        # set a flag to indicate that a bill has been generated
        request.session['bill_generated'] = True

        # render a success message
        return render(request, 'accounts/manager_view.html')
       
    else:
        customers = Customer.objects.all()
        deliveryagent = Deliveryagent.objects.all()
        print("hello")
        for customer in customers:
            customer.bill_option = True
            customer.save()
        for agent in deliveryagent:
            agent.salary_option = True
            agent.save()

        # set a flag to indicate that a bill has been generated
        request.session['bill_generated'] = True
        return render(request, 'accounts/success.html')
        
def item(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        subscription, created = Subscription.objects.get_or_create(Customer=customer)
        items=subscription.subscribeitem_set.all()
    else:
        items=[]
        subscriptions={'get_subscription_items':0}
    publications=Publication.objects.all()
    context = {'publications':publications}
    return render(request, 'accounts/item.html',context)
def apply_request(request):

    request.session['request_time'] = datetime.now()
    print(request_time)
    print("Hello")
    response=JsonResponse({'status': 'success'})
    response.set_cookie('name',request.user.name)
    print(name)
   
    return response
def next_page(request):
    request_time = request.session.get('request_time')
    #print(request_time)
    name=request.COOKIES.get('name')
    #print(name)
    if not request_time:
        # If request_time is None, redirect the user back to the initial page
        return redirect('buyer')
    
    user=User.objects.get(username=name)
   
    # Check if at least 1 week has passed since the user made the request
    if datetime.now() >= request_time + timedelta(weeks=1):
        return render(request, 'accounts/next_page.html')
    else:
        # If less than 1 week has passed, redirect the user back to the initial page
        return redirect('buyer')
def Address(request):
    global ar
    ar=ar+1
    if(ar>4):
    	ar=0
    subscribeitem = SubscribeItem.objects.all()
    deliveryagent=request.user.deliveryagent
    subscribeitem = SubscribeItem.objects.order_by('Area','door_number')
    if(ar==0):
    	topass=[]
    	for item in subscribeitem:
    		if(item.Area=="Gandhi Nagar"):
    			topass.append(item)
    			deliveryagent.salary=deliveryagent.salary+item.publication.price/40
    			deliveryagent.save()
    if(ar==1):
    	topass=[]
    	for item in subscribeitem:
    		if(item.Area=="Sahithi Nagar"):
    			topass.append(item)
    			deliveryagent.salary=deliveryagent.salary+item.publication.price/40
    			deliveryagent.save()
    			
    if(ar==2):
    	topass=[]
    	for item in subscribeitem:
    		if(item.Area=="Sai Nagar"):
    			topass.append(item)
    			deliveryagent.salary=deliveryagent.salary+item.publication.price/40
    			deliveryagent.save()
    if(ar==3):
    	topass=[]
    	for item in subscribeitem:
    		if(item.Area=="Sarath Nagar"):
    			topass.append(item)
    			deliveryagent.salary=deliveryagent.salary+item.publication.price/40
    			deliveryagent.save()
    if(ar==4):
    	topass=[]
    	for item in subscribeitem:
    		if(item.Area=="Vidhya Nagar"):
    			topass.append(item)
    			deliveryagent.salary=deliveryagent.salary+item.publication.price/40
    			deliveryagent.save()
    print(ar)
    print(deliveryagent.salary)
    context = {'subscribeitem':topass}
    return render(request, 'accounts/addressal.html', context )
def subscription(request):
    if request.user.is_authenticated:
    
        customer=request.user.customer
        subscription, created = Subscription.objects.get_or_create(Customer=customer)
        items=subscription.subscribeitem_set.all()
        
    else:
        items=[]
        subscriptions={'get_subscription_items':0}

    context = {'items':items, 'subscription':subscription}
    return render(request, 'accounts/subscription.html',context)
   

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        subscription,created=Subscription.objects.get_or_create(Customer=customer)
        items=subscription.subscribeitem_set.all()
    else:
        items=[]
        subscriptions={'get_subscription_items':0}

    context = {'items':items, 'subscription':subscription}
    return render(request, 'accounts/checkout.html',context)

def myaccount(request):
    
    customer=request.user.customer
    subscriptions = customer.subscription_set.all()
    
    print(subscriptions)
    
    context = {'subscriptions':subscriptions}
    return render(request, 'accounts/myaccount.html', context)
    
'''def updateitem(request):
    
    data=json.loads(request.body)
    prodID=data['prodID']
    action=data['action']
    print('action:',action)
    print('prodID:',prodID)

    customer=request.user.customer
    publication=Publication.objects.get(id=prodID) 
    Area=request.user.customer.Area
    door_number=request.user.customer.door_number
    subscription,created=Subscription.objects.get_or_create(Customer=customer,complete=false)
    subscribeItem,created=SubscribeItem.objects.get_or_create(subscription=subscription,publication=publication,Area=Area,door_number=door_number)
    if action=='add':
        subscribeItem.quantity=(subscribeItem.quantity+1)
    elif action=='remove':
        subscribeItem.quantity=(subscribeItem.quantity-1)
    subscribeItem.save()
    if subscribeItem.quantity<=0:
        subscribeItem.delete()
    
    return JsonResponse('item added',safe=False)'''
def updateitem(request):
    
    data=json.loads(request.body)
    prodID=data['prodID']
    action=data['action']
    print('action:',action)
    print('prodID:',prodID)

    customer=request.user.customer
    publication=Publication.objects.get(id=prodID) 
    Area=request.user.customer.Area
    door_number=request.user.customer.door_number
    subscription,created=Subscription.objects.get_or_create(Customer=customer)
    subscribeItem,created=SubscribeItem.objects.get_or_create(subscription=subscription,publication=publication,Area=Area,door_number=door_number)
    
    if action=='add':
        subscribeItem.quantity=(subscribeItem.quantity+1)
    elif action=='remove':
        subscribeItem.quantity=(subscribeItem.quantity-1)
    subscribeItem.save()
    if subscribeItem.quantity<=0:
        subscribeItem.delete()
    
    return JsonResponse('item added',safe=False)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def updateSubscription(request,test_id):
    
    subscription = Subscription.objects.get(id = test_id)
    form = SubscriptionForm(instance=subscription)
    
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = SubscriptionForm(request.POST,instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    
    
    return render(request,'accounts/subscription_form.html',context)
    
def salary(request):
    deliveryagent=request.user.deliveryagent
    context={'deliveryagent':deliveryagent}
    return render(request,'accounts/salary.html',context)
    
def redirect_to_admin(request):
    return redirect('admin:index')
