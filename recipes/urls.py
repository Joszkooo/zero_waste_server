from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, FridgeItemViewSet, RecipeViewSet, FavoriteRecipeViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'fridge', FridgeItemViewSet, basename='fridgeitem')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'favorites', FavoriteRecipeViewSet, basename='favoriterecipe')

urlpatterns = [
    path('', include(router.urls)),
]
