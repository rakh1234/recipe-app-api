"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet) #create new endpoint API "it means RecipeViewSet will auto generate URLs"
router.register('tags', views.TagViewSet)

app_name = 'recipe'

#auto create URLs by the router "beacause it is viewsets type" 
urlpatterns = [
    path('', include(router.urls)),
]