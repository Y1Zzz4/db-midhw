from django import forms
from .models import User, Book, Purchase

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'real_name', 'user_type', 'employee_id', 'gender', 'age']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'real_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

def clean_username(self):
        username = self.cleaned_data['username']
        # 允许现有用户的用户名保持不变
        if self.instance and self.instance.username == username:
            return username
        # 检查新用户名是否重复
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名已存在")
        return username

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publisher', 'price', 'stock']
        widgets = {
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        # Allow existing book's ISBN to remain unchanged
        if self.instance and self.instance.isbn == isbn:
            return isbn
        # Check for duplicate ISBN
        if Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError("该 ISBN 已存在")
        return isbn

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['book', 'quantity', 'price']
        labels = {
            'book': '图书',
            'quantity': '数量',
            'price': '进货价格',
        }