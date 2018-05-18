from django.db import models


class Recipe(models.Model):
    CUISINE = (
        ('brak', 'brak'),
        ('angielska', 'angielska'),
        ('polska', 'polska'),
        ('francuska', 'francuska'),
        ('wloska', 'wloska'),
        ('azjatycka', 'azjatycka')
    )
    DIET_TYPE = (
        ('weganska', 'weganska'),
        ('wegetarianska', 'wegetarianska'),
        ('bez glutenu', 'bez glutenu'),
        ('bez laktozy', 'bez laktozy'),
        ('brak', 'brak')
    )
    DIFFICULTY_LEVEL = (
        ('latwy', 'latwy'),
        ('sredni', 'sredni'),
        ('trudny', 'trudny')
    )
    MEAL_TYPE = (
        ('sniadanie', 'sniadanie'),
        ('obiad', 'obiad'),
        ('przekąska', 'przekąska'),
        ('kolacja', 'kolacja'),
        ('deser', 'deser')
    )

    name = models.CharField(max_length=1000, null=False, primary_key=True)
    diet_type = models.CharField(max_length=20, choices=DIET_TYPE, default='brak')
    cuisine = models.CharField(max_length=20, choices=CUISINE, default='brak')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL, default='sredni')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE)
    ingredients = models.CharField(max_length=1000, null=False)
    prepare_time = models.IntegerField(default=0)
    calorie = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    description = models.CharField(max_length=100000, null=False, default=None)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']
