from django.urls import path
from .views import ExampleSchedulingView
urlpatterns = [
    path('', ExampleSchedulingView.as_view()),
]
