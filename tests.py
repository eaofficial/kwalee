import unittest

from database import db
from models import Ingredient, MealHistory, Meal


class TestModels(unittest.TestCase):
    def setUp(self):
        # Ingredients
        db.add_object(
            Ingredient(
                object_id='onion'
            )
        )
        db.add_object(
            Ingredient(
                object_id='potato'
            )
        )
        db.add_object(
            Ingredient(
                object_id='eggs',
                unsuitable_diets=['vegan']
            )
        )
        db.add_object(
            Ingredient(
                object_id='cheese',
                unsuitable_diets=['vegan', 'dairy_free']
            )
        )
        db.add_object(
            Ingredient(
                object_id='bread',
                unsuitable_diets=['vegan', 'dairy_free']
            )
        )
        db.add_object(
            Ingredient(
                object_id='tuna',
                unsuitable_diets=['vegan', 'vegetarian']
            )
        )
        db.add_object(
            Ingredient(
                object_id='sausage',
                unsuitable_diets=['vegan', 'vegetarian', 'pescatarian']
            )
        )

        # Meals
        db.add_object(
            Meal(
                object_id='vegetable_soup',
                ingredient_ids=['onion', 'potato']
            )
        )
        db.add_object(
            Meal(
                object_id='chips_n_cheese',
                ingredient_ids=['cheese', 'potato']
            )
        )
        db.add_object(
            Meal(
                object_id='sausage_roll',
                ingredient_ids=['bread', 'sausage']
            )
        )
        db.add_object(
            Meal(
                object_id='tuna_salad',
                ingredient_ids=['eggs', 'tuna', 'onion', 'potato']
            )
        )
        db.add_object(
            Meal(
                object_id='hot_dog',
                ingredient_ids=['onion', 'sausage', 'cheese', 'bread']
            )
        )

    def test_adding_meal(self):
        meal_history = MealHistory(object_id="i_like_cake")
        meal_history.add_meal(meal_id='chips_n_cheese')
        meal_history.add_meal(meal_id='vegetable_soup')
        meal_history.add_meal(meal_id='tuna_salad')
        meal_history.add_meal(meal_id='chips_n_cheese')
        meal_history.add_meal(meal_id='hot_dog')
        meal_history.add_meal(meal_id='vegetable_soup')

        # Part2
        self.assertEqual(4, len(meal_history.meal_ids))
        self.assertEqual(1, meal_history.vegan_count)
        self.assertEqual(2, meal_history.vegetarian_count)
        self.assertEqual(2, meal_history.dairy_free_count)
        self.assertEqual(3, meal_history.pescatarian_count)

        # Part3
        db.add_object(meal_history)
        self.assertEqual(1, db.get_object_by_id('i_like_cake').vegan_count)

        # Part4
        self.assertEqual('meal', Meal.get_object_type())
        self.assertEqual('mealhistory', MealHistory.get_object_type())

        # Part5
        ingredients = db.get_objects_by_object_type(object_type=Ingredient.get_object_type())
        self.assertEqual(7, len(ingredients))

        # Part6
        sausage_roll = db.get_object_by_id(object_id='sausage_roll')
        hot_dog = db.get_object_by_id(object_id='hot_dog')
        self.assertEqual('BREAD,SAUSAGE', sausage_roll.get_ingredients_string())
        self.assertEqual('BREAD,CHEESE,ONION,SAUSAGE', hot_dog.get_ingredients_string())
