from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('user-management/', views.user_management, name='user_management'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('user-management/', views.user_management, name='user_management'),
    path('book-management/', views.book_management, name='book_management'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('user-management/', views.user_management, name='user_management'),
    path('book-management/', views.book_management, name='book_management'),
    path('purchase-management/', views.purchase_management, name='purchase_management'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('pay-purchase/<int:purchase_id>/', views.pay_purchase, name='pay_purchase'),
    path('return-purchase/<int:purchase_id>/', views.return_purchase, name='return_purchase'),
    path('add-to-stock/<int:purchase_id>/', views.add_to_stock, name='add_to_stock'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('user-management/', views.user_management, name='user_management'),
    path('book-management/', views.book_management, name='book_management'),
    path('purchase-management/', views.purchase_management, name='purchase_management'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('pay-purchase/<int:purchase_id>/', views.pay_purchase, name='pay_purchase'),
    path('return-purchase/<int:purchase_id>/', views.return_purchase, name='return_purchase'),
    path('add-to-stock/<int:purchase_id>/', views.add_to_stock, name='add_to_stock'),
    path('sale/', views.sale, name='sale'),
    path('buy-book/<int:book_id>/', views.buy_book, name='buy_book'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('user-management/', views.user_management, name='user_management'),
    path('book-management/', views.book_management, name='book_management'),
    path('purchase-management/', views.purchase_management, name='purchase_management'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('pay-purchase/<int:purchase_id>/', views.pay_purchase, name='pay_purchase'),
    path('return-purchase/<int:purchase_id>/', views.return_purchase, name='return_purchase'),
    path('add-to-stock/<int:purchase_id>/', views.add_to_stock, name='add_to_stock'),
    path('sale/', views.sale, name='sale'),
    path('buy-book/<int:book_id>/', views.buy_book, name='buy_book'),
    path('bill-view/', views.bill_view, name='bill_view'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('user-management/', views.user_management, name='user_management'),
    path('book-management/', views.book_management, name='book_management'),
    path('purchase-management/', views.purchase_management, name='purchase_management'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('pay-purchase/<int:purchase_id>/', views.pay_purchase, name='pay_purchase'),
    path('return-purchase/<int:purchase_id>/', views.return_purchase, name='return_purchase'),
    path('add-to-stock/<int:purchase_id>/', views.add_to_stock, name='add_to_stock'),
    path('sale/', views.sale, name='sale'),
    path('buy-book/<int:book_id>/', views.buy_book, name='buy_book'),
    path('bill-view/', views.bill_view, name='bill_view'),
]