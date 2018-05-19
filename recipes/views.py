from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .electra import electre_III_method, get_possible_recipes
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
                            'cost': form.data['cost'],'products': form.data['products']}
            # electre_list = electre_III_method(user_choices)
            recipes = get_possible_recipes(user_choices) # for now until electre method work
            template_name = 'recipes/recommended_recipes.html'
            return render(request, template_name, {'recipes': recipes})
    else:
        form = SearchRecipeForm()
    return render(request, 'recipes/search_recipe.html', {'form': form})
