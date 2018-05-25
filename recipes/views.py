from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .electra import get_sorted_recipes, electre_I_method, electre_III_method
from .models import Recipe
from .forms import SearchRecipeForm


class RecipeView(ListView):
    model = Recipe
    template_name = 'recipes/recipes.html'


class RecommendedRecipeView(ListView):
    template_name = 'recipes/recommended_recipes.html'


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        return context


def search_recipe(request):
    if request.method == 'POST':
        form = SearchRecipeForm(request.POST)
        if form.is_valid():
            user_choices = {'diet type': form.data['diet_type'], 'cuisine': form.data['cuisine'],
                            'difficulty level': form.data['difficulty_level'],
                            'meal type': form.data['meal_type'], 'allergens': form.data['allergens'],
                            'prepare_time': form.data['prepare_time'], 'calorie': form.data['calorie'],
                            'cost': form.data['cost'], 'products': form.data['products'],
                            'cost_kcal': form.data['cost_kcal'], 'cost_time': form.data['cost_time'],
                            'kcal_time': form.data['kcal_time'], 'veto_time': form.data['veto_time'],
                            'veto_cost': form.data['veto_cost'], 'veto_kcal': form.data['veto_kcal']}
            recipes = get_sorted_recipes(user_choices, electre_III_method)
            template_name = 'recipes/recommended_recipes.html'
            return render(request, template_name, {'recipes': recipes})
    else:
        form = SearchRecipeForm()
    return render(request, 'recipes/search_recipe.html', {'form': form})
