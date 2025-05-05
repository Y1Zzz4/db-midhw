from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import User, Book, Purchase, Bill, Sale
from .forms import UserForm, BookForm, PurchaseForm 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Login attempt: username={username}, password={password}")  # 调试
        user = authenticate(request, username=username, password=password)
        print(f"Authenticate result: {user}")  # 调试
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'欢迎，{user.real_name}')
                return redirect(next_url)
            else:
                messages.error(request, '用户账户已禁用')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

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

@login_required
def purchase_management(request):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    purchases = Purchase.objects.all()
    purchase_form = PurchaseForm()
    return render(request, 'purchase_management.html', {'purchases': purchases, 'purchase_form': purchase_form})

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
    messages.success(request, '付款成功')
    return redirect('purchase_management')

@login_required
def return_purchase(request, purchase_id):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.status == '未付款':
        purchase.status = '已退货'
        purchase.save()
    return redirect('purchase_management')

@login_required
def add_to_stock(request, purchase_id):
    if request.user.user_type not in ['superadmin', 'admin']:
        return redirect('home')
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.status == '已付款':
        book = purchase.book
        book.stock += purchase.quantity
        book.save()
    return redirect('purchase_management')

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

@login_required
def buy_book(request, book_id):
    if request.user.user_type != 'customer':
        return redirect('home')
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 0))
        if quantity > 0 and quantity <= book.stock:
            book.stock -= quantity
            book.save()
            sale = Sale.objects.create(
                book=book,
                quantity=quantity,
                sale_price=book.price,
                customer=request.user
            )
            Bill.objects.create(
                bill_type='收入',
                amount=book.price * quantity,
                related_info=f'销售: {book.title} x {quantity}'
            )
        return redirect('sale')
    return redirect('sale')

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

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