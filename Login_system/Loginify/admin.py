from django.contrib import admin

from .models import UserDetails

# Register your models here.

# @admin.register(UserDetails)
# class UserDetailsAdmin(admin.ModelAdmin):
#     list_display = ['id','username','email','password']

admin.site.register(UserDetails)

