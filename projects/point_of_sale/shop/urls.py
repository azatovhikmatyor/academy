from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shop'

urlpatterns = [
    # path('load/', views.load),
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('login', auth_views.LoginView.as_view(template_name = 'pos/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    path('pos', views.pos, name="pos-page"),
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),
    path('save-pos', views.save_pos, name="save-pos"),
    path('sales', views.salesList, name="sales-page"),
    path('receipt', views.receipt, name="receipt-modal"),
    path('delete_sale', views.delete_sale, name="delete-sale"),
]