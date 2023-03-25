from database import db


class IdentifiableObject(object):
    def __init__(self, object_id):
        self.object_id = object_id
        self.object_type = self.__class__.__name__.lower()

    @classmethod
    def get_object_type(cls):
        return cls.__name__.lower()

class Ingredient(IdentifiableObject):

    def __init__(self, object_id, unsuitable_diets=[]):
        super(Ingredient, self).__init__(object_id=object_id)
        self.unsuitable_diets = unsuitable_diets

class Meal(IdentifiableObject):
    def __init__(self, object_id, ingredient_ids=[]):
        super(Meal, self).__init__(object_id=object_id)
        self.ingredient_ids = ingredient_ids

    def get_ingredients_string(self):
        ingredients = [db.get_object_by_id(object_id).object_id.upper() for object_id in self.ingredient_ids]
        ingredients.sort()
        return ','.join(ingredients) if ingredients else ''

class MealHistory(IdentifiableObject):
    def __init__(self, object_id, meal_ids=[], vegan_count=0, vegetarian_count=0, dairy_free_count=0, pescatarian_count=0):
        super(MealHistory, self).__init__(object_id=object_id)
        self.meal_ids = meal_ids
        self.vegan_count = vegan_count
        self.vegetarian_count = vegetarian_count
        self.dairy_free_count = dairy_free_count
        self.pescatarian_count = pescatarian_count

    def add_meal(self, meal_id):
        if meal_id in self.meal_ids:
            return
        meal = db.get_object_by_id(meal_id)
        if not meal:
            return

        self.meal_ids.append(meal_id)

        vegan = True
        vegetarian = True
        dairy_free = True
        pescatarian = True

        for ingredient_id in meal.ingredient_ids:
            ingredient = db.get_object_by_id(ingredient_id)
            if not ingredient:
                continue

            if 'vegan' in ingredient.unsuitable_diets:
                vegan = False
            if 'vegetarian' in ingredient.unsuitable_diets:
                vegetarian = False
            if 'dairy_free' in ingredient.unsuitable_diets:
                dairy_free = False
            if 'pescatarian' in ingredient.unsuitable_diets:
                pescatarian = False

        if vegan:
            self.vegan_count += 1
        if vegetarian:
            self.vegetarian_count += 1
        if dairy_free:
            self.dairy_free_count += 1
        if pescatarian:
            self.pescatarian_count += 1

