from django.shortcuts import render
from django.contrib import messages


def login(request):
    return render(request, 'contas/login.html')


def logout(request):
    return render(request, 'contas/logout.html')


def cadastro(request):
    return render(request, 'contas/cadastro.html')


def dashboard(request):
    return render(request, 'contas/dashboard.html')
