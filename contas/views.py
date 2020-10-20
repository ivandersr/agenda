from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ContatoForm


def login(request):
    if request.method != 'POST':
        return render(request, 'contas/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'contas/login.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Bem vindo, {usuario}')
    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'contas/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome \
            or not sobrenome \
            or not email \
            or not usuario \
            or not senha \
            or not senha2:
        messages.error(request,
                       'Nenhum campo pode estar vazio.')
        return render(request, 'contas/cadastro.html')

    try:
        validate_email(email)
    except ValidationError as err:
        messages.error(request,
                       'Digite um email válido.')
        return render(request, 'contas/cadastro.html')

    if len(senha) < 6:
        messages.error(request,
                       'Senha deve conter ao menos 6 caracteres.')
        return render(request, 'contas/cadastro.html')

    if len(usuario) < 6:
        messages.error(request,
                       'Usuário deve conter ao menos 6 caracteres.')
        return render(request, 'contas/cadastro.html')

    if senha != senha2:
        messages.error(request,
                       'Erro na confirmação de senhas. Senhas não conferem.')

    if User.objects.filter(username=usuario).exists():
        messages.error(request,
                       'Usuário já existe.')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request,
                       'Email já existe.')
        return render(request, 'contas/cadastro.html')

    messages.success(request,
                     'Usuário cadastrado com sucesso. Faça seu login.')

    user = User.objects.create_user(
        username=usuario,
        email=email,
        password=senha,
        first_name=nome,
        last_name=sobrenome
    )

    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = ContatoForm()
        return render(request, 'contas/dashboard.html', {'form': form})

    form = ContatoForm(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao validar o formulário.')
        form = ContatoForm(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(
        request, f'Contato {request.POST.get("nome")} salvo com sucesso.')
    return redirect('dashboard')
