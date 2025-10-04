from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/productions/', include('productions.urls')),
    path('api/scheduling/', include('scheduling.urls')),
    path('api/vfx/', include('vfx.urls')),
    path('api/media/', include('media.urls')),
    path('api/finance/', include('finance.urls')),
]

# Add this line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
