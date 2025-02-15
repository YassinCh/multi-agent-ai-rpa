from django.urls import path
from . import views

app_name = 'test_form'

urlpatterns = [
    path('', views.form_view, name='form'),
    path('api/fill-form/', views.ai_fill_form, name='ai_fill_form'),
]
