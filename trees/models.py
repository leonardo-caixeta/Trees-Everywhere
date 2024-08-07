from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    accounts = models.ManyToManyField(Account)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def plant_trees(self, trees):
        for tree, coords in trees:
            self.plant_tree(tree, coords[0], coords[1])

    def plant_tree(self, tree, latitude, longitude, account):
        planted_tree = PlantedTree(
            user=self,
            tree=tree,
            latitude=Decimal(latitude),
            longitude=Decimal(longitude),
            account=account,  # Atribui a primeira conta do usuário # NOQA
        )

        planted_tree.save()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    about = models.TextField(blank=True)
    joined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    tree = models.ForeignKey(
        Tree,
        on_delete=models.SET_NULL,
        related_name="planted_tree",
        null=True,
        blank=True,
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    planted_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.tree.name} planted by {self.user.username}"
