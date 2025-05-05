from django.contrib import admin
from .models import User, Book, Purchase, Sale, Bill
from django.contrib.auth.admin import UserAdmin

#将模型注册到后台管理界面
admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Bill)
