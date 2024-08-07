from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account, Profile, Tree, PlantedTree
from .forms import UserCreationFormWithAccount


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationFormWithAccount
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password",
                    "accounts",
                ),
            },
        ),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_editable = ("active",)


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name")


@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ("tree", "user", "latitude", "longitude", "planted_at")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "about", "joined")
