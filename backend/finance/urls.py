from django.urls import path
from .views import ExampleFinanceView
urlpatterns = [
    path('', ExampleFinanceView.as_view()),
]
