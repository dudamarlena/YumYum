from itertools import product
import numpy as np

from .recipes_utils import recipes


def electre_method(user_choices):
    recipes = get_possible_recipes(user_choices)
    time, cost, kcal = get_criteria(recipes)
    weights = get_weight()
    fi_array = get_fi_array(time, cost, kcal, weights)
    c_array = get_c_array(fi_array)
    print(c_array)


def get_c_array(fi_array, s=0.5):
    c_array = [sum(fi_array[:, index]) for index in range(fi_array.shape[1])]
    return [c if c >= s else 0 for c in c_array]


def get_fi_array(time, cost, kcal, weights):
    fi1 = np.array([list(map(lambda x: x * weights[0], get_fi_list(time)))])
    fi2 = np.array([list(map(lambda x: x * weights[1], get_fi_list(cost)))])
    fi3 = np.array([list(map(lambda x: x * weights[2], get_fi_list(kcal)))])
    return np.concatenate((fi1, fi2, fi3), axis=0)


def get_fi_list(criterium):
    return [1 if criterium[i][0] > criterium[i][1] else 0 for i in range(len(criterium))]


def get_criteria(recipes):
    time = [t for t in recipes['prepare_time']]
    cost = [c for c in recipes['cost']]
    kcal = [k for k in recipes['calorie']]
    return list(product(time, time)), list(product(cost, cost)), list(product(kcal, kcal))


def get_weight():
    return [0.3, 0.1, 0.6]


def get_possible_recipes(user_choices):
    possible_recipes_list = []
    all_recipes = get_all_recipes()
    for recipe in all_recipes:
        condition1 = recipe['diet_type'] == user_choices['diet_type'] or user_choices['diet_type'] == 'brak'
        condition2 = recipe['cuisine'] == user_choices['cuisine'] or user_choices['cuisine'] == 'brak'
        condition3 = recipe['difficulty_level'] == user_choices['difficulty_level'] or user_choices[
                                                                                           'difficulty_level'] == 'brak'
        condition4 = recipe['meal_type'] == user_choices['meal_type'] or user_choices['meal_type'] == 'brak'
        condition5 = [ingredient for ingredient in recipe['ingredients'] if
                      any(allergen in ingredient for allergen in user_choices['allergens'])]
        condition6 = int(user_choices['prepare_time']) >= int(recipe['prepare_time'])
        condition7 = int(user_choices['calorie']) >= int(recipe['calorie'])
        condition8 = int(user_choices['cost']) >= int(recipe['cost'])
        if condition1 and condition2 and condition3 and condition4 and not condition5 and condition6 and condition7 and condition8:
            possible_recipes_list.append(recipe)
    return possible_recipes_list


def get_all_recipes():
    return recipes
