from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView
from .models import PlantedTree
from .forms import PlantedTreeForm, TreeForm
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import PlantedTreeSerializer


class UserIsAdminMixin(UserPassesTestMixin):
    # Mixin para verificar se o usuário é administrador
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class LoginView(View):
    # View para login de usuários
    form_class = AuthenticationForm
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        # Renderiza o formulário de login na requisição GET
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        # Processa o formulário de login na requisição POST
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(
                    "user_trees"
                )  # Redireciona para a lista de árvores do usuário # NOQA
        return render(request, self.template_name, {"form": form})


class UserPlantedTreesAPIView(generics.ListAPIView):
    # API View para listar árvores plantadas pelo usuário logado
    serializer_class = PlantedTreeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna as árvores plantadas pelo usuário logado
        return PlantedTree.objects.filter(user=self.request.user)


class UserTreesView(LoginRequiredMixin, ListView):
    # View para listar árvores plantadas pelo usuário logado
    model = PlantedTree
    template_name = "user_trees.html"
    context_object_name = "planted_trees"

    def get_queryset(self):
        # Filtra as árvores plantadas pelo usuário logado
        return PlantedTree.objects.filter(user=self.request.user)


class TreeDetailView(LoginRequiredMixin, DetailView):
    # View para exibir detalhes de uma árvore plantada
    model = PlantedTree
    template_name = "tree_detail.html"

    def get(self, request, *args, **kwargs):
        # Verifica a permissão do usuário e renderiza os detalhes da árvore
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return HttpResponseForbidden(
                "Você não tem permissão para visualizar esta árvore."
            )
        return super().get(request, *args, **kwargs)


class PlantTreeView(LoginRequiredMixin, CreateView):
    # View para plantar uma nova árvore
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "plant_tree.html"
    success_url = reverse_lazy("user_trees")

    def get_form_kwargs(self):
        # Passa o usuário logado para o formulário
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Define o usuário logado como o plantador da árvore
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountTreesView(LoginRequiredMixin, ListView):
    # View para listar árvores plantadas por usuários das contas do usuário logado  # NOQA
    model = PlantedTree
    template_name = "account_trees.html"
    context_object_name = "planted_trees"

    def get_queryset(self):
        # Filtra as árvores plantadas por usuários das contas do usuário logado
        user = self.request.user
        accounts = user.accounts.all()
        return PlantedTree.objects.filter(
            user__accounts__in=accounts
        ).distinct()


class AddTreeView(LoginRequiredMixin, CreateView):
    # View para adicionar uma nova árvore
    form_class = TreeForm
    template_name = "add_tree.html"
    success_url = reverse_lazy("user_trees")
