from django import forms
from .models import PlantedTree, Account, Tree, User


class PlantedTreeForm(forms.ModelForm):
    # Formulário para plantar uma nova árvore
    class Meta:
        model = PlantedTree
        fields = ["tree", "latitude", "longitude", "account"]

    def __init__(self, *args, **kwargs):
        # Filtra as contas disponíveis para o usuário logado
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = user.accounts.all()


class TreeForm(forms.ModelForm):
    # Formulário para adicionar uma nova árvore
    class Meta:
        model = Tree
        fields = ["name", "scientific_name"]


class UserCreationFormWithAccount(forms.ModelForm):
    # Formulário para criar um novo usuário com vinculação a uma conta
    password = forms.CharField(widget=forms.PasswordInput)
    accounts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(), required=True
    )

    class Meta:
        model = User
        fields = ["username", "password", "accounts"]

    def save(self, commit=True):
        # Define a senha do usuário e o vincula a uma conta
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user.accounts.add(self.cleaned_data["accounts"])
        return user
