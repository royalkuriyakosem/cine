from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserProfileView, 
    UserCreateView, 
    AdminOnlyView, 
    ProducerOrDirectorView,
    MyTokenObtainPairView
)

urlpatterns = [
    # JWT Auth endpoints
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('producer-director/', ProducerOrDirectorView.as_view(), name='producer_director'),
]
