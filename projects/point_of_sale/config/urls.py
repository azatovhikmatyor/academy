from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('', include('shop.urls', namespace='shop')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('admin/', admin.site.urls),
    
    # path('', include('shop.urls')),
]
