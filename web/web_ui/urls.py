# myapp/urls.py
from django.urls import path
from .views import flowchart_view

urlpatterns = [
    path("flowchart", flowchart_view, name="flowchart"),
]
