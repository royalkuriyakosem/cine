from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/productions/', include('productions.urls')),
    path('api/scheduling/', include('scheduling.urls')),
    path('api/vfx/', include('vfx.urls')),
    path('api/media/', include('media.urls')),
    path('api/finance/', include('finance.urls')),
]
