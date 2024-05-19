from django.contrib import admin
from .models import Customer, Vehicle, ParkMovement, Contract, ContractRule

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(ParkMovement)
admin.site.register(Contract)
admin.site.register(ContractRule)
