from django.urls import path
from .views import (
    LoginView,
    UserPlantedTreesAPIView,
    UserTreesView,
    PlantTreeView,
    AccountTreesView,
    AddTreeView,
    TreeDetailView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user/trees/", UserTreesView.as_view(), name="user_trees"),
    path("tree/plant/", PlantTreeView.as_view(), name="plant_tree"),
    path("tree/<int:pk>/", TreeDetailView.as_view(), name="tree_detail"),
    path("account/trees/", AccountTreesView.as_view(), name="account_trees"),
    path("tree/add/", AddTreeView.as_view(), name="add_tree"),
    path(
        "api/user/trees/",
        UserPlantedTreesAPIView.as_view(),
        name="user_planted_trees_api",
    ),
]
