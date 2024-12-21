from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('category', views.category, name="category-page"),
    path('manage_category', views.manage_category, name="manage_category-page"),
    path('save_category', views.save_category, name="save-category-page"),
    path('delete_category', views.delete_category, name="delete-category"),
    path('products', views.products, name="product-page"),
    path('manage_products', views.manage_products, name="manage_products-page"),
    path('save_product', views.save_product, name="save-product-page"),
    path('delete_product', views.delete_product, name="delete-product"),    
]