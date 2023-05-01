from django.contrib import admin
from .models import *
# Register your models here.
from atexit import register

admin.site.register(Customer)
admin.site.register(Deliveryagent)
admin.site.register(Manager)
admin.site.register(Publication)
admin.site.register(Subscription)
admin.site.register(SubscribeItem)
