from django.urls import path
from .views import ExampleProductionView
urlpatterns = [
    path('', ExampleProductionView.as_view()),
]
