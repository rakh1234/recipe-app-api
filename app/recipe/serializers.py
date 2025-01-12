"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe

#Serializer for recipe obj, we use ModelSerializer to represent a specific model
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


#RecipeDetailSerializer is an extension of the RecipeSerializer
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']