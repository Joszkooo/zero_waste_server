from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from .models import Product, FridgeItem, Recipe, FavoriteRecipe
from .serializers import ProductSerializer, FridgeItemSerializer, RecipeSerializer, FavoriteRecipeSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class FridgeItemViewSet(viewsets.ModelViewSet):
    serializer_class = FridgeItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FridgeItem.objects.filter(user=self.request.user)

class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        user_fridge_products = FridgeItem.objects.filter(user=request.user).values_list('product_id', flat=True)
        
        if not user_fridge_products:
            return Response({"detail": "Twoja lodówka jest pusta."}, status=status.HTTP_200_OK)

        recipes = Recipe.objects.annotate(
            total_ingredients=Count('ingredients'),
            matching_ingredients=Count('ingredients', filter=Q(ingredients__product_id__in=user_fridge_products))
        ).filter(matching_ingredients__gt=0)

        # Oblicz procent dopasowania w Pythonie i posortuj
        recipe_list = list(recipes)
        for recipe in recipe_list:
            if recipe.total_ingredients > 0:
                recipe.match_percentage = round((recipe.matching_ingredients / recipe.total_ingredients) * 100)
            else:
                recipe.match_percentage = 0
                
        recipe_list.sort(key=lambda x: x.match_percentage, reverse=True)

        serializer = self.get_serializer(recipe_list, many=True)
        return Response(serializer.data)

class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(user=self.request.user)
