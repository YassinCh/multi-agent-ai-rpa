from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Person
import json

def form_view(request):
    if request.method == 'POST':
        try:
            Person.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                occupation=request.POST['occupation'],
                birth_date=request.POST['birth_date'],
                gender=request.POST['gender']
            )
            messages.success(request, 'Form submitted successfully!')
            return redirect('test_form:form')
        except Exception as e:
            messages.error(request, f'Error submitting form: {str(e)}')
    return render(request, 'test_form/form.html')

@csrf_exempt
def ai_fill_form(request):
    # This is a placeholder response - you'll integrate with your AI agent later
    dummy_data = {
        'full_name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'address': '123 Main St, City, Country',
        'occupation': 'Software Engineer',
        'birth_date': '1990-01-01'
    }
    return JsonResponse(dummy_data)
