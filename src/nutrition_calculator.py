import os
from dotenv import load_dotenv
from src.steps.ingredients_extractor import IngredientsExtractor 
from src.steps.nutritional_value_extractor import NutritionalValueExtractor
from src.steps.quantity_standardizer import QuantityStandardizer
from src.steps.quantity_calculator import QuantityCalculator
from src.steps.dish_categorizer import CategorizeDishes

load_dotenv()
nutrition_file_path = os.getenv('FILE_PATH')

def calculate_nutrition(dish_name: str):
    '''
    This function is used to calculate the nutrition of a recipe.
    It takes the recipe name as input and returns the nutrition information.
    '''
    # Extract the ingredients of the recipe
    results =IngredientsExtractor().extract_ingredients(dish_name)
    
    nutrition_extractor = NutritionalValueExtractor(nutrition_file_path)
    quantity_standardizer = QuantityStandardizer()
    quantity_calculator = QuantityCalculator()
    categorizer = CategorizeDishes()

    result = []
    res = []
    sum = 0
    total_protein_in_grams = 0
    total_carbohydrates_in_grams = 0
    total_fat_in_grams = 0
    total_fibre_in_grams = 0

    for i in results:
        extractor = nutrition_extractor.search_food(i['ingredient'])
        res = []
        s = 0
        if isinstance(extractor, list) and len(extractor) > 0:
            weight_in_grams = quantity_standardizer.estimate_grams(i['ingredient'], i['quantity'])
            res.append(extractor[0]['Protein (g)'])
            res.append(extractor[0]['Carbohydrates (g)'])
            res.append(extractor[0]['Fat (g)'])
            res.append(extractor[0]['Fibre (g)'])

            ans,nutritional_sum = quantity_calculator.calculate_total_nutrition(weight_in_grams,res)
            total_protein_in_grams = int(total_protein_in_grams + ans[0])
            total_carbohydrates_in_grams = int(total_carbohydrates_in_grams + ans[1])
            total_fat_in_grams = int(total_fat_in_grams + ans[2])
            total_fibre_in_grams = int(total_fibre_in_grams + ans[3])
            sum = sum + nutritional_sum

    result = {
        "estimated_nutrition": [{"protein":total_protein_in_grams,"carbs": total_carbohydrates_in_grams,"fat": total_fat_in_grams,"fibre":total_fibre_in_grams}],
        "dish_type": categorizer.categorize_dish(sum)
    }
    return result,results
    