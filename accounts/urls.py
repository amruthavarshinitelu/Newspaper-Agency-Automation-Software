from django.urls import path

from . import views
from .views import redirect_to_admin
urlpatterns = [
    path('', views.home, name='home'),
    path('redirecr-to-admin/',redirect_to_admin,name='redirect_to_admin'),
    path('registerpage/',views.registerpage,name = 'register'),
    path('loginpage/',views.loginpage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('addpublication/', views.addpublication, name = 'addpublication'),
    path('manager_view/', views.manager_view, name = 'manager_view'),
    path('subscription/', views.subscription, name = 'subscription'),
    path('item/', views.item, name = 'item'),
    path('Address/', views.Address, name = 'Address'),
    path('updateitem/', views.updateitem, name = 'updateitem'),
    path('mregister/', views.register_manager, name = 'mregister'),
    path('deliveryagent/',views.register_deliveryagent, name = 'deliveryagent'),
    path('deliveryagenthome/',views.deliveryagent_home, name = 'deliveryagenthome'),
    path('buyer/', views.buyer, name= 'buyer'),
    path('managerdashboard/', views.managerdashboard, name = 'managerdashboard'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('generate_bill/', views.generate_bill, name = 'generate_bill'),
    path('customer_bill/', views.customer_bill, name = 'customer_bill'),
    path('buyer/apply_request/', views.apply_request, name='apply_request'),
    path('next_page/', views.next_page, name='next_page'),
    path('cancel/', views.cancel, name='cancel'),
    path('payment/', views.payment, name='payment'),
    path('salary/', views.salary, name='salary'),
    
    
    
]
