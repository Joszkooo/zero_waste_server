from rest_framework import serializers
from .models import Product, FridgeItem, Recipe, RecipeIngredient, FavoriteRecipe

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FridgeItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_unit = serializers.ReadOnlyField(source='product.default_unit')

    class Meta:
        model = FridgeItem
        fields = ['id', 'product', 'product_name', 'product_unit', 'quantity']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class RecipeIngredientSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = RecipeIngredient
        fields = ['product', 'product_name', 'quantity', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    match_percentage = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'source_url', 'image_url', 'prep_time_minutes', 'ingredients', 'match_percentage']

    def get_match_percentage(self, obj):
        return getattr(obj, 'match_percentage', None)

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe_details = RecipeSerializer(source='recipe', read_only=True)

    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'recipe', 'recipe_details', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
