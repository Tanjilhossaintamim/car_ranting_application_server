from django.contrib import admin
from .models import User, Owner, Client

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''Admin View for User'''

    list_display = ('id', 'email', 'is_owner')
    list_per_page = 10


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    '''Admin View for Owner'''

    list_display = ('id', 'user', 'first_name', 'last_name',
                    'phone', 'image', 'date_of_birth')
    list_per_page = 10


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    '''Admin View for Client'''

    list_display = ('id', 'user', 'first_name', 'last_name',
                    'phone', 'image', 'date_of_birth')
    list_per_page = 10
