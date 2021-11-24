from django.urls import path

from .endpoints import MetricAPIView

app_name = 'core'

urlpatterns = [
    path('metrics/', MetricAPIView.as_view(), name='metrics-api'),
]
