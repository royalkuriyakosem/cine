from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CallSheetViewSet,
    DailyProductionReportViewSet,
    MyCallSheetView,
    generate_call_sheet_pdf
)

router = DefaultRouter()
router.register(r'call-sheets', CallSheetViewSet)
router.register(r'dprs', DailyProductionReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-call-sheets/', MyCallSheetView.as_view(), name='my-call-sheets'),
    path('call-sheets/<int:pk>/pdf/', generate_call_sheet_pdf, name='call-sheet-pdf'),
]
