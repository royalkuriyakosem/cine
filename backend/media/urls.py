from django.urls import path
from .views import ExampleMediaView
urlpatterns = [
    path('', ExampleMediaView.as_view()),
]
