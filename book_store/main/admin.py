from django.contrib import admin
from .models import User, Book, Purchase, Sale, Bill
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Bill)
