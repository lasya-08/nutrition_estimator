import pandas as pd
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class QuantityCalculator:
    def __init__(self):
        """
        Initializes the QuantityCalculator class.

        - Sets up a logger.
        - Loads the nutrition data from a CSV file path specified in the environment variable 'FILE_PATH'.
        - Reads the CSV into a DataFrame and sets 'food_code' as the index.
        """
        self.logger = logging.getLogger("NutritionCalculator")
        self.logger.setLevel(logging.INFO)
        self.nutrition_csv_path = os.getenv('FILE_PATH')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        if not self.logger.handlers:
            self.logger.addHandler(handler)

        try:
            self.df = pd.read_csv(self.nutrition_csv_path)
            self.df.set_index("food_code", inplace=True)
            self.logger.info(f"Loaded nutrition data from '{self.nutrition_csv_path}' with {len(self.df)} items.")
        except Exception as e:
            self.logger.error(f"Failed to load nutrition data: {e}")
            raise

    def calculate_total_nutrition(self, quantity_in_grams: float, results: list) -> tuple[list[float], float]:
        """
        Calculates the total nutritional values based on the quantity provided.

        Args:
            quantity_in_grams (float): The quantity of food in grams.
            results (list): A list of nutritional values per 100 grams.

        Returns:
            tuple[list[float], float]: A tuple where the first item is a list of scaled nutritional values
                                       and the second item is their total sum.
        """
        result = []
        total = 0.0
        for i in results:
            try:
                val = float(i)
            except (ValueError, TypeError):
                val = 0.0
            partial = (quantity_in_grams / 100) * val
            result.append(partial)
            total += partial
        return result, total

