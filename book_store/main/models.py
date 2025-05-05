from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, real_name, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名不能为空')
        user = self.model(username=username, real_name=real_name, **extra_fields)
        user.set_password(password)  # 使用 Django 的密码加密
        user.save(using=self._db)
        return user
    
def create_superuser(self, username, real_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'superadmin')
        return self.create_user(username, real_name, password, **extra_fields)

class User(AbstractUser):
    USER_TYPES = [
        ('superadmin', '超级管理员'),
        ('admin', '普通管理员'),
        ('customer', '普通用户'),
    ]
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('none', '无'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES,default='customer')
    real_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='none', blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['real_name']

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
        return f"{self.title}({self.isbn})"
    
class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('returned', '已退货'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_stocked = models.BooleanField(default=False)  # 新增

    def __str__(self):
        return f"Purchase {self.id} - {self.book.title}"

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
