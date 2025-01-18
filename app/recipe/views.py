"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers

#there is many types of viewsets and we chose ModelViewSet beacause we'll use a lot of existing logic "read, create,..." provided by serializer
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] #to make sure that only auth users "logged in users" can use recipe

    def get_queryset(self):
        """Retrieve recipes for authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class
    
    def perform_create(self, serializer): #it only accept 1 paramete "serializer" which is the the validated new recipe we want to create
        """Create a new recipe."""
        serializer.save(user=self.request.user)
        

#refactored Base view class
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet): #the parameter here are inherited base classes
    """Base viewset for recipe attributes."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name') #each user can manage their own Ingredient


#refactored view class
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


#refactored view class 
class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all() #to tell djnago REST what models we want to be managable 