from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Account, Tree, PlantedTree

User = get_user_model()


class TreesEverywhereTests(TestCase):
    def setUp(self):
        # Configuração inicial de dados
        self.account1 = Account.objects.create(name="Account 1")
        self.account2 = Account.objects.create(name="Account 2")

        self.user1 = User.objects.create_user(
            username="user1", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password"
        )
        self.user3 = User.objects.create_user(
            username="user3", password="password"
        )

        self.user1.accounts.add(self.account1)
        self.user2.accounts.add(self.account1)
        self.user3.accounts.add(self.account2)

        self.tree1 = Tree.objects.create(name="Oak", scientific_name="Quercus")
        self.tree2 = Tree.objects.create(name="Pine", scientific_name="Pinus")
        self.tree3 = Tree.objects.create(
            name="Birch", scientific_name="Betula"
        )

        self.planted_tree1 = PlantedTree.objects.create(
            user=self.user1,
            tree=self.tree1,
            latitude=45.0,
            longitude=90.0,
            account=self.account1,
        )
        self.planted_tree2 = PlantedTree.objects.create(
            user=self.user2,
            tree=self.tree2,
            latitude=46.0,
            longitude=91.0,
            account=self.account1,
        )
        self.planted_tree3 = PlantedTree.objects.create(
            user=self.user3,
            tree=self.tree3,
            latitude=47.0,
            longitude=92.0,
            account=self.account2,
        )

        self.client = Client()

    def test_user_trees_template(self):
        # Testa se a lista de árvores plantadas por um usuário específico é renderizada corretamente # NOQA
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("user_trees"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tree1.name)
        self.assertNotContains(response, self.tree2.name)
        self.assertNotContains(response, self.tree3.name)

    def test_forbidden_access_to_other_user_trees(self):
        # Testa se o acesso às árvores plantadas por outro usuário retorna erro 403 # NOQA
        self.client.login(username="user1", password="password")
        response = self.client.get(
            reverse("tree_detail", args=[self.planted_tree3.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_account_trees_template(self):
        # Testa se a lista de árvores plantadas pelos usuários das contas do usuário logado é renderizada corretamente # NOQA
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("account_trees"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tree1.name)
        self.assertContains(response, self.tree2.name)
        self.assertNotContains(response, self.tree3.name)

    def test_plant_tree_method(self):
        # Testa se o método User.plant_tree() cria corretamente um objeto PlantedTree # NOQA
        self.user1.plant_tree(tree=self.tree3, latitude=48.0, longitude=93.0)
        self.assertTrue(
            PlantedTree.objects.filter(
                user=self.user1, tree=self.tree3
            ).exists()
        )

    def test_plant_trees_method(self):
        # Testa se o método User.plant_trees() cria corretamente múltiplos objetos PlantedTree # NOQA
        trees_to_plant = [
            (self.tree1, (49.0, 94.0)),
            (self.tree2, (50.0, 95.0)),
        ]
        self.user1.plant_trees(trees_to_plant)
        self.assertTrue(
            PlantedTree.objects.filter(
                user=self.user1, tree=self.tree1
            ).exists()
        )
        self.assertTrue(
            PlantedTree.objects.filter(
                user=self.user1, tree=self.tree2
            ).exists()
        )
