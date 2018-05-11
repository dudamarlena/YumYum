"""YumYum URL Configuration"""
from django.conf.urls import url
from django.contrib import admin
from recipes.views import RecipeView, RecommendedRecipeView, RecipeDetailView, search_recipe

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recipes/$', RecipeView.as_view(), name="recipes"),
    url(r'^search/$', search_recipe, name="search_recipes"),
    url(r'^recommended/$', RecommendedRecipeView.as_view(), name="recommended"),
    url(r'^recommended/(?P<pk>\w+)/$', RecipeDetailView.as_view(), name="detail"),
]
