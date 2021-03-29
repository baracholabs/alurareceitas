from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from receitas.models import Receita


def index(request):
    receitas = Receita.objects.order_by("-date_receita").filter(publicada=True)

    paginator = Paginator(receitas, 3)
    page = request.GET.get("page")
    receitas_por_pagina = paginator.get_page(page)

    dados = {"receitas": receitas_por_pagina}
    return render(request, "receitas/index.html", dados)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {"receita": receita}

    return render(request, "receitas/receita.html", receita_a_exibir)


def cria_receita(request):
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.user.id)
        nome_receita = request.POST.get("nome_receita")
        ingredientes = request.POST.get("ingredientes")
        modo_preparo = request.POST.get("modo_preparo")
        tempo_preparo = request.POST.get("tempo_preparo")
        rendimento = request.POST.get("rendimento")
        categoria = request.POST.get("categoria")
        foto_receita = request.FILES.get("foto_receita")
        receita = Receita.objects.create(
            pessoa=user,
            nome_receita=nome_receita,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo,
            rendimento=rendimento,
            categoria=categoria,
            foto_receita=foto_receita,
        )
        receita.save()
        redirect("dashboard")
    return redirect("receitas/cria_receita")


def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {"receita": receita}
    return render(request, "receitas/edita_receita.html", receita_a_editar)


def atualiza_receita(request):
    if request.method == "POST":
        receita_id = request.POST.get("receita_id")
        receita = Receita.objects.get(pk=receita_id)
        receita.nome_receita = request.POST.get("nome_receita")
        receita.ingredientes = request.POST.get("ingredientes")
        receita.modo_preparo = request.POST.get("modo_preparo")
        receita.tempo_preparo = request.POST.get("tempo_preparo")
        receita.rendimento = request.POST.get("rendimento")
        receita.categoria = request.POST.get("categoria")

        if "foto_receita" in request.FILES:
            receita.foto_receita = request.FILES.get("foto_receita")

        receita.save()
        messages.success(request, "Atualizada")

    return redirect("dashboard")


def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    messages.success(request, "Receita deletada")
    return redirect("dashboard")
