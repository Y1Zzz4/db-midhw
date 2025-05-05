from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  
    # 用户登录页面

    path('logout/', views.logout_view, name='logout'),  
    # 用户注销操作

    path('', views.home, name='home'),  
    # 系统首页（默认路径）

    path('user-management/', views.user_management, name='user_management'),  
    # 用户管理界面（查看所有用户）

    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),  
    # 编辑用户信息，传入用户ID

    path('book-management/', views.book_management, name='book_management'),  
    # 图书管理页面（查看图书列表）

    path('book/edit/<int:book_id>/', views.edit_book, name='edit_book'),  
    # 编辑书籍信息，传入书籍ID

    path('purchase-management/', views.purchase_management, name='purchase_management'),  
    # 进货管理界面，显示所有进货记录

    path('add-purchase/', views.add_purchase, name='add_purchase'),  
    # 添加一条新的进货记录

    path('pay-purchase/<int:purchase_id>/', views.pay_purchase, name='pay_purchase'),  
    # 为指定ID的进货记录付款

    path('return-purchase/<int:purchase_id>/', views.return_purchase, name='return_purchase'),  
    # 退还指定ID的进货记录

    path('add-to-stock/<int:purchase_id>/', views.add_to_stock, name='add_to_stock'),  
    # 将某次进货入库（更新库存）

    path('sale/', views.sale, name='sale'),  
    # 销售页面（发起销售）

    path('buy-book/<int:book_id>/', views.buy_book, name='buy_book'),  
    # 购买指定ID的图书

    path('bill-view/', views.bill_view, name='bill_view'),  
    # 查看账单记录（收入和支出）
]