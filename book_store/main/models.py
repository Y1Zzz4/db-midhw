from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 自定义用户管理器，用于创建普通用户和超级用户
class UserManager(BaseUserManager):
    def create_user(self, username, real_name, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名不能为空')
        # 创建用户对象
        user = self.model(username=username, real_name=real_name, **extra_fields)
        if password:
            user.set_password(password)  # 使用 Django 内置方法加密密码
        else:
            user.password = ''  # 防止空密码报错
        user.save(using=self._db)
        return user

    def create_superuser(self, username, real_name, password=None, **extra_fields):
        # 设置超级用户标志字段
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'superadmin')
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, real_name, password, **extra_fields)

# 自定义用户模型，继承自 AbstractUser
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
    # 用户类型字段（决定权限等级）
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    # 用户真实姓名
    real_name = models.CharField(max_length=100)
    # 员工编号（可选）
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    # 性别
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='none', blank=True)
    # 年龄
    age = models.PositiveIntegerField(null=True, blank=True)
    # 是否激活
    is_active = models.BooleanField(default=True)
    # 是否为管理员（admin后台访问权限）
    is_staff = models.BooleanField(default=False)

    # 关联自定义管理器
    objects = UserManager()

    # 使用用户名作为登录字段
    USERNAME_FIELD = 'username'
    # 创建用户时必须填写的字段（除了用户名和密码）
    REQUIRED_FIELDS = ['real_name']

    def __str__(self):
        return self.username

# 书籍信息模型
class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)  # 唯一书号
    title = models.CharField(max_length=200)             # 书名
    author = models.CharField(max_length=100)            # 作者
    publisher = models.CharField(max_length=100)         # 出版社
    price = models.DecimalField(max_digits=8, decimal_places=2)  # 价格
    stock = models.PositiveIntegerField(default=0)        # 库存数量

    def __str__(self):
        return f"{self.title}({self.isbn})"

# 进货记录模型
class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 对应的书籍
    quantity = models.PositiveIntegerField()                  # 数量
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 总价
    status = models.CharField(max_length=20, choices=[
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('returned', '已退货'),
    ], default='pending')                                     # 状态
    created_at = models.DateTimeField(auto_now_add=True)      # 创建时间
    is_stocked = models.BooleanField(default=False)           # 是否已入库

    def __str__(self):
        return f"Purchase {self.id} - {self.book.title}"

# 售出记录模型
class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 出售的书籍
    quantity = models.PositiveIntegerField()                  # 销售数量
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)  # 售价
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 客户信息
    sale_time = models.DateTimeField(auto_now_add=True)       # 销售时间

# 财务流水账单模型
class Bill(models.Model):
    TYPE_CHOICES = [('收入', '收入'), ('支出', '支出')]
    bill_type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # 类型：收入/支出
    amount = models.DecimalField(max_digits=8, decimal_places=2)       # 金额
    created_at = models.DateTimeField(auto_now_add=True)               # 创建时间
    related_info = models.TextField()                                  # 备注信息或关联说明
