from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = [
        ('superadmin', '超级管理员'),
        ('admin', '普通管理员'),
        ('customer', '普通用户'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    real_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}（{self.isbn}）"
    
class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('未付款', '未付款'), ('已付款', '已付款'), ('已退货', '已退货')])
    created_at = models.DateTimeField(auto_now_add=True)

class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sale_time = models.DateTimeField(auto_now_add=True)

class Bill(models.Model):
    TYPE_CHOICES = [('收入', '收入'), ('支出', '支出')]
    bill_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    related_info = models.TextField()
