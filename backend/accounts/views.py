from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .permissions import role_required
from .serializers import UserProfileSerializer, UserCreateSerializer

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [role_required(['ADMIN'])]

class AdminOnlyView(APIView):
    permission_classes = [role_required(['ADMIN'])]
    def get(self, request):
        return Response({"message": "Hello, Admin!"})

class ProducerOrDirectorView(APIView):
    permission_classes = [role_required(['PRODUCER', 'DIRECTOR'])]
    def get(self, request):
        return Response({"message": "Hello, Producer or Director!"})
