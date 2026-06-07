from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    default_unit = models.CharField(max_length=20, default='g', help_text="e.g. g, ml, szt")

    def __str__(self):
        return self.name

class FridgeItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fridge_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity} {self.product.default_unit})"

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField()
    source_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    prep_time_minutes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unit or self.product.default_unit} {self.product.name} (for {self.recipe.title})"

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"
