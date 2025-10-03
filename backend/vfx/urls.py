from django.urls import path
from .views import ExampleVFXView
urlpatterns = [
    path('', ExampleVFXView.as_view()),
]
