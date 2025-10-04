from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import RolePermission
from .serializers import UserProfileSerializer, UserCreateSerializer, MyTokenObtainPairSerializer
from .models import CustomUser

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [RolePermission]
    required_roles = ['ADMIN']

class AdminOnlyView(APIView):
    permission_classes = [RolePermission]
    required_roles = ['ADMIN']
    def get(self, request):
        return Response({"message": "Hello, Admin!"})

class ProducerOrDirectorView(APIView):
    permission_classes = [RolePermission]
    required_roles = ['PRODUCER', 'DIRECTOR']
    def get(self, request):
        return Response({"message": "Hello, Producer or Director!"})

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [RolePermission]
    required_roles = ['ADMIN']
