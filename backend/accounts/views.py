from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import role_required

class ExampleAccountView(APIView):
    def get(self, request):
        return Response({"message": "Accounts endpoint"})

class AdminOnlyView(APIView):
    permission_classes = [role_required(['ADMIN'])]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})

class ProducerOrDirectorView(APIView):
    permission_classes = [role_required(['PRODUCER', 'DIRECTOR'])]

    def get(self, request):
        return Response({"message": "Hello, Producer or Director!"})
