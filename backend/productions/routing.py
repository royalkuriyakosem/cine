from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dashboard/(?P<production_id>\w+)/$', consumers.ProductionDashboardConsumer.as_asgi()),
]