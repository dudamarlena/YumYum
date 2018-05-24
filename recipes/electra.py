from itertools import product
import numpy as np
from .recipes_utils import recipes


def get_sorted_recipes(user_choices, electre_method):
    recipes = get_possible_recipes(user_choices)
    electre_values = electre_method(user_choices, recipes)
    sorted_names = sort_recipes(electre_values, recipes)
    electre_data = [recipe for name in sorted_names for recipe in recipes if name == recipe['name']]
    return electre_data


def electre_I_method(user_choices, recipes):
    time, cost, kcal = get_criteria(recipes)
    weights = get_weight()
    fi_array = get_fi_array(time, cost, kcal, weights)
    c_array = get_c_array(fi_array)
    return c_array


def electre_III_method(user_choices, recipes):
    time, cost, kcal = get_criteria(recipes)
    weights = get_weight()
    preference_thresholds = get_preference_thresholds()
    equivalence_thresholds = get_equivalence_thresholds()
    veto = get__veto()
    fi_array = get_fi3_array(time, cost, kcal, weights, preference_thresholds, equivalence_thresholds)
    c_array = get_c_array(fi_array)
    reliability_coefficient = get_reliability_coefficient([time, cost, kcal], c_array, preference_thresholds, veto)
    return reliability_coefficient


def get_reliability_coefficient(criteria, c_array, preference_thresholds, veto):
    return [value if get_d_list(criteria, preference_thresholds, veto) <= value else value * (
        (1 - get_d_list(criteria, preference_thresholds, veto)) / 1 - value) for value in c_array]


def get_c_array(fi_array, s=0.5):
    c_array = [sum(fi_array[:, index]) for index in range(fi_array.shape[1])]
    return [c if c >= s else 0 for c in c_array]


def get_d_list(criteria, preference_thresholds, veto):
    d = 1
    for criterium in criteria:
        for i in range(len(veto)):
            if int(criterium[i][0]) >= int(criterium[i][1]) + veto[i]:
                d *= 1
            elif int(criterium[i][1]) <= int(criterium[i][0]) + preference_thresholds[i]:
                d *= 0
            else:
                try:
                    d *= (int(criterium[i][1]) - int(criterium[i][0]) - preference_thresholds[i]) / (
                        veto[i] - preference_thresholds[i])
                except ZeroDivisionError:
                    d *= 0
    return d


def get_fi_array(time, cost, kcal, weights):
    fi1 = np.array([list(map(lambda x: x * weights[0], get_fi_list_I(time)))])
    fi2 = np.array([list(map(lambda x: x * weights[1], get_fi_list_I(cost)))])
    fi3 = np.array([list(map(lambda x: x * weights[2], get_fi_list_I(kcal)))])
    return np.concatenate((fi1, fi2, fi3), axis=0)


def get_fi3_array(time, cost, kcal, weights, preference_thresholds, equivalence_thresholds):
    fi1 = np.array([list(
        map(lambda x: x * weights[0], get_fi_list_III(time, preference_thresholds[0], equivalence_thresholds[0])))])
    fi2 = np.array([list(
        map(lambda x: x * weights[1], get_fi_list_III(cost, preference_thresholds[1], equivalence_thresholds[1])))])
    fi3 = np.array([list(
        map(lambda x: x * weights[2], get_fi_list_III(kcal, preference_thresholds[2], equivalence_thresholds[2])))])
    return np.concatenate((fi1, fi2, fi3), axis=0)


def get_fi_list_I(criterium):
    return [1 if int(criterium[i][0]) > int(criterium[i][1]) else 0 for i in range(len(criterium))]


def get_fi_list_III(criterium, preference_thresholds, equivalence_thresholds):
    fi_list = []
    for i in range(len(criterium)):
        if int(criterium[i][0]) + equivalence_thresholds > int(criterium[i][1]):
            fi_list.append(1)
        elif int(criterium[i][0]) + equivalence_thresholds < int(criterium[i][1]) and int(criterium[i][1]) <= int(
                criterium[i][0]) + preference_thresholds:
            try:
                fi_list.append((int(criterium[i][1]) + preference_thresholds - int(
                    criterium[i][0])) / preference_thresholds - equivalence_thresholds)
            except ZeroDivisionError:
                fi_list.append(0)
        else:
            fi_list.append(0)
    return fi_list


def get_criteria(recipes):
    time = [recipe['prepare_time'] for recipe in recipes]
    cost = [recipe['cost'] for recipe in recipes]
    kcal = [recipe['calorie'] for recipe in recipes]
    return list(product(time, time)), list(product(cost, cost)), list(product(kcal, kcal))


def get_weight():
    return [0.3, 0.1, 0.6]


def get_preference_thresholds():
    return [0, 0, 0]


def get_equivalence_thresholds():
    return [0, 0, 0]


def get__veto():
    return [0, 0, 0]


def get_possible_recipes(user_choices):
    possible_recipes_list = []
    all_recipes = get_all_recipes()
    for recipe in all_recipes:
        condition1 = recipe['diet type'] == user_choices['diet type'] or user_choices['diet type'] == 'brak'
        condition2 = recipe['cuisine'] == user_choices['cuisine'] or user_choices['cuisine'] == 'brak'
        condition3 = recipe['difficulty level'] == user_choices['difficulty level'] or user_choices[
                                                                                           'difficulty level'] == 'brak'
        condition4 = recipe['meal type'] == user_choices['meal type'] or user_choices['meal type'] == 'brak'
        condition5 = [ingredient for ingredient in split_strings(recipe['ingredients']) if
                      any(allergen in ingredient for allergen in split_strings(user_choices['allergens']))]
        ingredients = split_strings(recipe['ingredients'])
        ingredients.append('brak')
        condition6 = [ingredient for ingredient in ingredients if
                      any(products in ingredient for products in split_strings(user_choices['products'])) or recipe[
                          'ingredients'] == 'brak']
        condition7 = int(user_choices['prepare_time']) >= int(recipe['prepare_time'])
        condition8 = int(user_choices['calorie']) >= int(recipe['calorie'])
        condition9 = int(user_choices['cost']) >= int(recipe['cost'])
        if condition1 and condition2 and condition3 and condition4 and not condition5 and condition6 and condition7 and condition8 and condition9:
            possible_recipes_list.append(recipe)
    return possible_recipes_list


def split_strings(strings):
    return strings.split(',')


def get_all_recipes():
    return recipes


def get_dictionary(electre_values, recipes):
    name_list = []
    for recipe in recipes:
        name_list.append(recipe['name'])
    prod_list = zip(list(product(name_list, name_list)), electre_values)
    electre_data = []
    for pair in (prod_list):
        electre_data.append({'pair': pair[0], 'value': pair[1]})
    return electre_data


def sort_recipes(reliability_coefficient, recipes):
    reliability_coefficient = np.array(reliability_coefficient)
    recipes_names = [name['name'] for name in recipes]
    c_sqrt = int(np.sqrt(len(reliability_coefficient)))
    sum_values = [sum(row) for row in reliability_coefficient.reshape((c_sqrt, c_sqrt))]
    sorted_indexes = sorted(range(len(sum_values)), key=lambda x: sum_values[x])
    return [recipes_names[index] for index in sorted_indexes][::-1]
