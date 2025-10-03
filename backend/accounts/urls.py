from django.urls import path
from .views import ExampleAccountView
urlpatterns = [
    path('', ExampleAccountView.as_view()),
]
