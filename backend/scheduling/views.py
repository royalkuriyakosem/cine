from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import CallSheet, DailyProductionReport, CrewCheckIn
from .serializers import CallSheetSerializer, DailyProductionReportSerializer, CrewCheckInSerializer
from accounts.permissions import role_required
from .pdf_templates import generate_simple_call_sheet

class CallSheetViewSet(viewsets.ModelViewSet):
    queryset = CallSheet.objects.all()
    serializer_class = CallSheetSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish']:
            permission_classes = [role_required(['ADMIN', 'UPM_AD', 'LINE_PRODUCER'])]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        call_sheet = self.get_object()
        call_sheet.published = True
        call_sheet.save()

        # Send update to the production dashboard channel
        channel_layer = get_channel_layer()
        group_name = f'production_{call_sheet.production.id}'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_update',
                'message': {
                    'event': 'CALL_SHEET_PUBLISHED',
                    'call_sheet_id': call_sheet.id,
                    'date': str(call_sheet.date),
                }
            }
        )

        return Response({'status': 'Call sheet published'})

    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, pk=None):
        call_sheet = self.get_object()
        user = request.user
        if str(user.id) not in call_sheet.crew_assignments:
             return Response({'error': 'You are not assigned to this call sheet.'}, status=status.HTTP_403_FORBIDDEN)
        check_in, created = CrewCheckIn.objects.get_or_create(call_sheet=call_sheet, crew_member=user)
        if not created:
            return Response({'status': 'Already checked in'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CrewCheckInSerializer(check_in)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DailyProductionReportViewSet(viewsets.ModelViewSet):
    queryset = DailyProductionReport.objects.all()
    serializer_class = DailyProductionReportSerializer
    permission_classes = [role_required(['ADMIN', 'UPM_AD', 'LINE_PRODUCER', 'PRODUCER'])]

class MyCallSheetView(generics.ListAPIView):
    serializer_class = CallSheetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CallSheet.objects.filter(published=True, crew_assignments__has_key=str(user.id))

def generate_call_sheet_pdf(request, pk):
    user = request.user
    try:
        call_sheet = CallSheet.objects.get(pk=pk, published=True)
    except CallSheet.DoesNotExist:
        if user.is_authenticated and (user.is_staff or user.role in ['ADMIN', 'UPM_AD', 'LINE_PRODUCER']):
            try:
                call_sheet = CallSheet.objects.get(pk=pk)
            except CallSheet.DoesNotExist:
                 return HttpResponse("Call Sheet not found.", status=404)
        else:
            return HttpResponse("Call Sheet not found or is not published.", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="call_sheet_{call_sheet.date}.pdf"'
    pdf = generate_simple_call_sheet(call_sheet)
    response.write(pdf)
    return response

from rest_framework.views import APIView
from rest_framework.response import Response
class ExampleSchedulingView(APIView):
    def get(self, request):
        return Response({"message": "Scheduling endpoint"})
