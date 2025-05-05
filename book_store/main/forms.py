from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="密码")
    class Meta:
        model = User
        fields = ['username', 'password', 'real_name', 'user_type', 'employee_id', 'gender', 'age']
        labels = {
            'username': '用户名',
            'real_name': '真实姓名',
            'user_type': '用户类型',
            'employee_id': '工号',
            'gender': '性别',
            'age': '年龄',
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publisher', 'price', 'stock']
        labels = {
            'isbn': 'ISBN',
            'title': '书名',
            'author': '作者',
            'publisher': '出版社',
            'price': '价格',
            'stock': '库存',
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['book', 'quantity', 'purchase_price']
        labels = {
            'book': '图书',
            'quantity': '数量',
            'purchase_price': '进货价格',
        }