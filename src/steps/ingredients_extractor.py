import json
import logging
from typing import List, Dict
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class IngredientsExtractor:
    """
    Class for extracting ingredients from a recipe name using an LLM-based pipeline.
    """

    def __init__(self):
        """
        Initializes the LLM model, output schema, and prompt template.
        """
        # Define expected structured output schema
        self.logging =logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.response_schemas = [
            ResponseSchema(
                name="ingredients",
                description="List of ingredients with quantities",
                type="List[Dict[str, str]]"
            )
        ]

        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()

        # Define the prompt template
        self.prompt = PromptTemplate.from_template(
            """You are an expert multi-cuisine indian chef. Extract ingredients for {recipe_name} with these requirements. Do not add water into ingredients:
            1. Use ONLY standard Indian measurements (tsp, tbsp, cup, katori, pieces)
               150ml Cup or Katori
               250ml Glass
               5ml teaspoon
               15ml tablespoon
               100ml teacup
               pieces count (Give finite number like 5. Do not give approximations like 2-3)
            2. Format as list of dictionaries with 'quantity' and 'ingredient' keys. In the ingredient only mention ingredient, don't mention any quantity or pieces count. Mention it in quantity if needed. Do not add the words cubed, diced in ingredient names.
            3. For 3-4 servings
            4. Output MUST be valid JSON matching this schema:
            {format_instructions}

            Example Output:
            {{
                "ingredients": [
                    {{"quantity": "1 cup", "ingredient": "rice"}},
                    {{"quantity": "2 tbsp", "ingredient": "oil"}}
                ]
            }}"""
        )

        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,
            model_kwargs={
                "response_mime_type": "application/json"
            }
        )

        # Create the chain of operations: prompt -> model -> structured output
        self.chain = self.prompt | self.llm | self.output_parser

    def extract_ingredients(self, recipe_name: str) -> List[Dict[str, str]]:
        """
        Extracts a structured list of ingredients for the given recipe name.

        Args:
            recipe_name (str): The name of the recipe to extract ingredients for.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing 'quantity' and 'ingredient' keys.
        """
        self.logger.info(f"Extracting ingredients for recipe: {recipe_name}")

        try:
            result = self.chain.invoke({
                "recipe_name": recipe_name,
                "format_instructions": self.format_instructions
            })

            ingredients = result.get("ingredients", [])
            self.logger.info(f"Extracted {len(ingredients)} ingredients successfully.")
            return ingredients

        except Exception as e:
            self.logger.error(f"Error extracting ingredients: {e}")
            return []
