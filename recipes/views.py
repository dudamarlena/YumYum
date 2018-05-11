from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect

from .models import Recipe
from .forms import SearchRecipeForm


class RecipeView(ListView):
    model = Recipe
    template_name = 'recipes/recipes.html'


class RecommendedRecipeView(ListView):
    model = Recipe
    template_name = 'recipes/recommended_recipes.html'


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        return context


def search_recipe(request):
    if request.method == 'POST':
        print('post')
        form = SearchRecipeForm(request.POST)
        if form.is_valid():
            user_choices = {'diet_type': form.data['diet_type'], 'cuisine': form.data['cuisine'],
                            'difficulty_level': form.data['difficulty_level'],
                            'meal_type': form.data['meal_type'], 'allergens': form.data['allergens'],
                            'prepare_time': form.data['prepare_time'], 'calorie': form.data['calorie'],
                            'cost': form.data['cost']}
            return HttpResponseRedirect('/recommended/')
    else:
        print('get')
        form = SearchRecipeForm()
    return render(request, 'recipes/search_recipe.html', {'form': form})


