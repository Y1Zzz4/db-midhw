# 用户认证、跳转与消息模块导入
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# 引入模型与表单
from .models import User, Book, Purchase, Bill, Sale
from .forms import UserForm, BookForm, PurchaseForm 

# 登录视图
def login_view(request):
    if request.method == 'POST':
        # 提取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 认证用户
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)  # 登录成功
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'欢迎，{user.real_name}')
                return redirect(next_url)
            else:
                messages.error(request, '用户账户已禁用')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')

# 主页视图（需登录）
@login_required
def home(request):
    return render(request, 'home.html')

# 用户管理（仅超级管理员）
@login_required
def user_management(request):
    if not (request.user.is_superuser or request.user.user_type == 'superadmin'):
        messages.error(request, '无权限访问')
        return redirect('home')
    form = UserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'用户 {user.username} 创建成功')
                return redirect('user_management')
            except ValueError as e:
                messages.error(request, f'创建失败：{str(e)}')
        else:
            messages.error(request, f'创建失败，请检查输入：{form.errors}')
    users = User.objects.all()
    return render(request, 'user_management.html', {'form': form, 'users': users})

# 编辑用户信息
@login_required
def edit_user(request, user_id):
    if not (request.user.is_superuser or request.user.user_type == 'superadmin'):
        messages.error(request, '无权限访问')
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    form = UserForm(request.POST or None, instance=user)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'用户 {user.username} 更新成功')
                return redirect('user_management')
            except ValueError as e:
                messages.error(request, f'更新失败：{str(e)}')
        else:
            messages.error(request, f'更新失败，请检查输入：{form.errors}')
    return render(request, 'edit_user.html', {'form': form, 'user': user})

# 图书管理（仅管理员）
@login_required
def book_management(request):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_management')
    else:
        isbn = request.GET.get('isbn')
        if isbn:
            form = BookForm(instance=get_object_or_404(Book, isbn=isbn))
        else:
            form = BookForm()
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(isbn__icontains=query) |
        Q(author__icontains=query) | Q(publisher__icontains=query)
    )
    return render(request, 'book_management.html', {'form': form, 'books': books})

# 编辑图书信息
@login_required
def edit_book(request, book_id):
    if not (request.user.is_superuser or request.user.user_type in ['superadmin', 'admin']):
        return redirect('home')
    book = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('book_management')
    return render(request, 'edit_book.html', {'form': form, 'book': book})

# 进货单管理
@login_required
def purchase_management(request):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    purchases = Purchase.objects.all()
    purchase_form = PurchaseForm()
    return render(request, 'purchase_management.html', {'purchases': purchases, 'purchase_form': purchase_form})

# 添加进货单
@login_required
def add_purchase(request):
    if not (request.user.is_superuser or request.user.user_type in ['superadmin', 'admin']):
        return redirect('home')
    form = PurchaseForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, '进货单创建成功')
            return redirect('purchase_management')
        else:
            messages.error(request, '创建失败，请检查输入')
    return render(request, 'purchase_management.html', {'form': form, 'purchases': Purchase.objects.all()})

# 支付进货单
@login_required
def pay_purchase(request, purchase_id):
    if not (request.user.is_superuser or request.user.user_type in ['superadmin', 'admin']):
        messages.error(request, '无权限执行此操作')
        return redirect('purchase_management')
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.status != 'pending':
        messages.error(request, '只能对待付款的进货单进行付款')
        return redirect('purchase_management')
    purchase.status = 'paid'
    purchase.save()
    Bill.objects.create(
        bill_type='支出',
        amount=purchase.price * purchase.quantity,
        related_info=f'进货: {purchase.book.title} x {purchase.quantity}'
    )
    messages.success(request, '付款成功')
    return redirect('purchase_management')

# 退货处理
@login_required
def return_purchase(request, purchase_id):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.status == '未付款':
        purchase.status = '已退货'
        purchase.save()
    return redirect('purchase_management')

# 入库操作（新版）
@login_required
def add_to_stock(request, purchase_id):
    if not (request.user.is_superuser or request.user.user_type in ['superadmin', 'admin']):
        return redirect('home')
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.status != 'paid':
        messages.error(request, '只有已付款的进货可以入库')
        return redirect('purchase_management')
    if purchase.is_stocked:
        messages.error(request, '该进货已入库')
        return redirect('purchase_management')
    purchase.book.stock += purchase.quantity
    purchase.book.save()
    purchase.is_stocked = True
    purchase.save()
    messages.success(request, '成功入库')
    return redirect('purchase_management')

# 销售视图（用户与管理员不同界面）
@login_required
def sale(request):
    if request.user.user_type not in ['superadmin', 'admin', 'customer']:
        return redirect('home')
    if request.user.user_type == 'customer':
        books = Book.objects.filter(stock__gt=0)
        return render(request, 'sale.html', {'books': books})
    else:
        sales = Sale.objects.all()
        return render(request, 'sale.html', {'sales': sales})

# 购买图书
@login_required
def buy_book(request, book_id):
    if request.user.user_type != 'customer':
        return redirect('home')
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 0))
        if 0 < quantity <= book.stock:
            book.stock -= quantity
            book.save()
            # 创建销售记录与账单
            Sale.objects.create(book=book, quantity=quantity, sale_price=book.price, customer=request.user)
            Bill.objects.create(bill_type='收入', amount=book.price * quantity, related_info=f'销售: {book.title} x {quantity}')
        return redirect('sale')
    return redirect('sale')

# 账单查看（可按日期筛选）
@login_required
def bill_view(request):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    bills = Bill.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        bills = bills.filter(created_at__range=[start_date, end_date])
    return render(request, 'bill_view.html', {'bills': bills})

# 注销登录
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
