from fastapi import FastAPI
from src.nutrition_calculator import calculate_nutrition

app = FastAPI()

@app.get("/nutrition/{dish_name}")
def get_nutrition(dish_name: str):
    data, ingredients = calculate_nutrition(dish_name)
    return {
        "data": data,
        "ingredients": ingredients
    }

