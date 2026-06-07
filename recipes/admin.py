from django.contrib import admin
from .models import Product, FridgeItem, Recipe, RecipeIngredient, FavoriteRecipe

admin.site.register(Product)
admin.site.register(FridgeItem)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(FavoriteRecipe)
