# About the Project

This project provides a FastAPI-based REST API that calculates the nutritional information of a dish using an LLM (Large Language Model) and fuzzy matching against a nutritional database.

# 🚀 Project Overview

This application allows users to get nutritional insights for a dish simply by passing its name through a REST API.

## 🔄 Flow of the Application

1. Ingredient Extraction

The name of the dish is passed to an LLM, which extracts the probable ingredients.

2. Fuzzy Matching

Extracted ingredients are matched against a nutrition database using rapidfuzz to handle:

Spelling mistakes
Synonyms (e.g., “curd” vs. “yogurt”)

3. Standardization

Ingredient quantities are standardized to grams for consistency using LLM.

4. Nutrient Calculation

Total nutritional values (per 100g) are calculated for:

Protein

Carbohydrates

Fat

Fibre

5. Dish Categorization

Based on the extracted nutrient weights, the dish is categorized into predefined types like:

Wet Rice Item

Veg Gravy

Non-Veg Gravy

## Tech Stack
1. Python 3.9
2. FastAPI - Web Framework
3. Uvicorn - ASGI Server
4. Pydantic - Data validation
5. rapidfuzz - Fuzzy string matching
6. LLM (Local or cloud-based) - For ingredient extraction


To start the project:

1. Create a virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  
    ```
2. Install dependencies

    ```bash
    pip install -r requirements.txt
    ``

3. Load the credentials from .env file

Create a .env file and add any required credentials, API keys, or model paths.

4. Run the following command to start the server:
```bash
 uvicorn main:app --reload
 ``

Examples:

1. Paneer butter masala:{
    "data": {
        "estimated_nutrition": [
            {
                "protein": 54,
                "carbs": 60,
                "fat": 77,
                "fibre": 8
            }
        ],
        "dish_type": "Wet Rice Item / Veg Gravy / Non-Veg Gravy / Dals / Raita / Plain Soup"
    },
    "ingredients": [
        {
            "quantity": "250ml",
            "ingredient": "paneer"
        },
        {
            "quantity": "1 tbsp",
            "ingredient": "ginger-garlic paste"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "turmeric powder"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "red chili powder"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "garam masala"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "cumin powder"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "coriander powder"
        },
        {
            "quantity": "150ml",
            "ingredient": "tomato puree"
        },
        {
            "quantity": "2 tbsp",
            "ingredient": "butter"
        },
        {
            "quantity": "1/2 cup",
            "ingredient": "heavy cream"
        },
        {
            "quantity": "1/4 cup",
            "ingredient": "cashew paste"
        },
        {
            "quantity": "2",
            "ingredient": "green chilies"
        },
        {
            "quantity": "1",
            "ingredient": "bay leaf"
        },
        {
            "quantity": "2",
            "ingredient": "cardamom"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "salt"
        },
        {
            "quantity": "2 tbsp",
            "ingredient": "oil"
        },
        {
            "quantity": "1/4 cup",
            "ingredient": "onion"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "sugar"
        }
    ]
}

2. Sandwich
{
    "data": {
        "estimated_nutrition": [
            {
                "protein": 7,
                "carbs": 25,
                "fat": 1,
                "fibre": 3
            }
        ],
        "dish_type": "Plain Flatbread"
    },
    "ingredients": [
        {
            "quantity": "2",
            "ingredient": "brown bread slices"
        },
        {
            "quantity": "1/2 cup",
            "ingredient": "mashed potatoes"
        },
        {
            "quantity": "2 tbsp",
            "ingredient": "coriander chutney"
        },
        {
            "quantity": "1 tbsp",
            "ingredient": "mint chutney"
        },
        {
            "quantity": "1/4 cup",
            "ingredient": "shredded paneer"
        },
        {
            "quantity": "1 tbsp",
            "ingredient": "chopped onions"
        },
        {
            "quantity": "1 tbsp",
            "ingredient": "chopped tomatoes"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "red chili powder"
        },
        {
            "quantity": "1/4 tsp",
            "ingredient": "garam masala"
        },
        {
            "quantity": "1/4 tsp",
            "ingredient": "chaat masala"
        },
        {
            "quantity": "2",
            "ingredient": "cucumber slices"
        },
        {
            "quantity": "2",
            "ingredient": "tomato slices"
        }
    ]
}

3. Chicken curry
{
    "data": {
        "estimated_nutrition": [
            {
                "protein": 38,
                "carbs": 41,
                "fat": 45,
                "fibre": 18
            }
        ],
        "dish_type": "Wet Rice Item / Veg Gravy / Non-Veg Gravy / Dals / Raita / Plain Soup"
    },
    "ingredients": [
        {
            "quantity": "500 gms",
            "ingredient": "chicken"
        },
        {
            "quantity": "2",
            "ingredient": "large onions"
        },
        {
            "quantity": "2 tbsp",
            "ingredient": "ginger-garlic paste"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "turmeric powder"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "red chili powder"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "coriander powder"
        },
        {
            "quantity": "1 tsp",
            "ingredient": "cumin powder"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "garam masala"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "salt"
        },
        {
            "quantity": "2",
            "ingredient": "tomatoes"
        },
        {
            "quantity": "1/2 cup",
            "ingredient": "yogurt"
        },
        {
            "quantity": "2 tbsp",
            "ingredient": "oil"
        },
        {
            "quantity": "1 cup",
            "ingredient": "chopped cilantro"
        },
        {
            "quantity": "2",
            "ingredient": "green chilies"
        },
        {
            "quantity": "1/2 tsp",
            "ingredient": "asafoetida"
        },
        {
            "quantity": "2",
            "ingredient": "bay leaves"
        },
        {
            "quantity": "4",
            "ingredient": "cardamom pods"
        },
        {
            "quantity": "2",
            "ingredient": "cloves"
        }
    ]
}

Here is the local api to access the server:
    http://127.0.0.1:8000/nutrition/{dish_name}