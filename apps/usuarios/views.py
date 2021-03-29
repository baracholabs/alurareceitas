from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """ Cadastra uma nova pessoa no sistema """
    if request.method == "POST":
        username = request.POST.get("nome")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if campo_vazio(username):
            messages.error(request, "O campo nome não pode ficar em branco")
            return redirect("cadastro")
        if campo_vazio(email):
            messages.error(request, "O campo email não pode ficar em branco")
            return redirect("cadastro")
        if senhas_nao_sao_iguais(password, password2):
            messages.error(request, "As senhas não são iguais")
            return redirect("cadastro")
        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "Usuário já cadastrado")
            return redirect("cadastro")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        messages.success(request, "Usuário cadastrado com sucesso")
        return redirect("login")
    else:
        return render(request, "usuarios/cadastro.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("senha")
        if campo_vazio(email) or campo_vazio(password):
            messages.error(request, "Os campos email e senha devem ser preenchidos")
            return redirect("login")
        if User.objects.filter(email=email).exists():
            username = (
                User.objects.filter(email=email)
                .values_list("username", flat=True)
                .get()
            )
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    return render(request, "usuarios/login.html")


def logout(request):
    auth.logout(request)
    return redirect("index")


def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by("-date_receita").filter(
            pessoa=request.user.id
        )
        dados = {"receitas": receitas}
        return render(request, "usuarios/dashboard.html", dados)
    return redirect("index")

def campo_vazio(campo):
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2