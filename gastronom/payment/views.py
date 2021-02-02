from django.shortcuts import render, redirect
from .models import Payment

def about(request):
    return render(request, 'gastronom/payment.html')