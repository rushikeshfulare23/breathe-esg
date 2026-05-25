from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', upload_data),
    path('records/', list_records),
    path('records/<int:pk>/', approve_record),
    path('audit-logs/', audit_logs),
]