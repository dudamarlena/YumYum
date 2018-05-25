from django import forms


class SearchRecipeForm(forms.Form):
    CUISINE = (('brak', 'brak'),
               ('angielska', 'angielska'),
               ('polska', 'polska'),
               ('francuska', 'francuska'),
               ('wloska', 'wloska'),
               ('azjatycka', 'azjatycka')
               )
    DIET_TYPE = (('brak', 'brak'),
                 ('weganska', 'weganska'),
                 ('wegetarianska', 'wegetarianska'),
                 ('bez glutenu', 'bez glutenu'),
                 ('bez laktozy', 'bez laktozy')
                 )
    DIFFICULTY_LEVEL = (('brak', 'brak'),
                        ('latwy', 'latwy'),
                        ('sredni', 'sredni'),
                        ('trudny', 'trudny')
                        )
    MEAL_TYPE = (('brak', 'brak'),
                 ('sniadanie', 'sniadanie'),
                 ('obiad', 'obiad'),
                 ('przekąska', 'przekąska'),
                 ('kolacja', 'kolacja'),
                 ('deser', 'deser')
                 )
    diet_type = forms.ChoiceField(choices=DIET_TYPE, required=False, label='Rodzaj diety')
    cuisine = forms.ChoiceField(choices=CUISINE, required=False, label='Rodzaj kuchni')
    difficulty_level = forms.ChoiceField(choices=DIFFICULTY_LEVEL, required=False, label='Poziom trudności')
    meal_type = forms.ChoiceField(choices=MEAL_TYPE, required=False, label='Rodzaj posiłku')
    allergens = forms.CharField(required=False, label='Alergeny', initial='brak')
    products = forms.CharField(required=False, label='Produkty, które mamy w kuchni', initial='brak')
    prepare_time = forms.IntegerField(required=False, label='Czas przygotowania [min]', initial=100)
    calorie = forms.IntegerField(required=False, label='Ilość kalorii', initial=1000)
    cost = forms.IntegerField(required=False, label='Koszt przygotowania posiłku [zł]', initial=100)
    cost_kcal = forms.IntegerField(required=False, label='Koszt czy ilość kalorii?', initial=1)
    cost_time = forms.IntegerField(required=False, label='Koszt czy czas przygotowania posiłku?', initial=1)
    kcal_time = forms.IntegerField(required=False, label='Ilość kalorii czy czas przygotowania posiłku?', initial=1)
    veto_time = forms.IntegerField(required=False, label='Czas przygotowania posiłku', initial=10)
    veto_cost = forms.IntegerField(required=False, label='Koszt', initial=10)
    veto_kcal = forms.IntegerField(required=False, label='Ilość kalorii', initial=200)
