from django.shortcuts import render
from django.views.generic import ListView, DetailView

from recipes import recipes_utils
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

    def public_post_view(self,recipe_id):
        print(recipe_id)


def search_recipe(request):
    if request.method == 'POST':
        form = SearchRecipeForm(request.POST)
        if form.is_valid():
            user_choices = {'diet_type': form.data['diet_type'], 'cuisine': form.data['cuisine'],
                            'difficulty_level': form.data['difficulty_level'],
                            'meal_type': form.data['meal_type'], 'allergens': form.data['allergens'],
                            'prepare_time': form.data['prepare_time'], 'calorie': form.data['calorie'],
                            'cost': form.data['cost']}
            recipes = Recipe.objects.filter(diet_type= 'wegetarianska') # for example
            template_name = 'recipes/recommended_recipes.html'
            return render(request, template_name, {'recipes': recipes})
    else:
        form = SearchRecipeForm()
    return render(request, 'recipes/search_recipe.html', {'form': form})


