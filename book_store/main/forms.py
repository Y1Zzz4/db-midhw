from django import forms
from .models import User, Book, Purchase

class UserForm(forms.ModelForm):
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'real_name', 'user_type', 'employee_id', 'gender', 'age', 'password']
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

def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # 加密密码
        elif not self.instance.pk:  # 新用户未提供密码
            raise ValueError("新用户必须提供密码")
        if commit:
            user.save()
        return user

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

def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        quantity = cleaned_data.get('quantity')
        total_price = cleaned_data.get('total_price')
        if book and quantity and total_price:
            expected_price = book.price * quantity
            if total_price <= 0:
                raise forms.ValidationError("总价必须大于 0")
        return cleaned_data