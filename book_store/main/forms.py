from django import forms
from .models import User, Book, Purchase

# 用户表单
class UserForm(forms.ModelForm):
    # 密码输入框
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    # 确认密码输入框
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

    # 检查用户名唯一性
    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance and self.instance.username == username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名已存在")
        return username

    # 密码验证
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("两次输入的密码不一致")
            if len(password) < 6:
                raise forms.ValidationError("密码长度至少为6位")
        if not self.instance.pk and not password:
            raise forms.ValidationError("新用户必须设置密码")
        return cleaned_data

    # 保存用户，并处理密码加密
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        elif not self.instance.pk:
            raise ValueError("新用户必须设置密码")
        if commit:
            user.save()
            print(f"Saved user: {user.username}, password: {user.password}")  # 调试信息
        return user

# 图书表单
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

# 检查 ISBN 是否重复
def clean_isbn(self):
    isbn = self.cleaned_data['isbn']
    if self.instance and self.instance.isbn == isbn:
        return isbn
    if Book.objects.filter(isbn=isbn).exists():
        raise forms.ValidationError("该 ISBN 已存在")
    return isbn

# 进货表单
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['book', 'quantity', 'price']
        labels = {
            'book': '图书',
            'quantity': '数量',
            'price': '进货价格',
        }

# 验证进货总价有效性
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
