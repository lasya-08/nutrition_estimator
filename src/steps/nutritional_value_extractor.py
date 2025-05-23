import pandas as pd
import re
import logging
from rapidfuzz import process, fuzz
from typing import List, Dict, Union
class NutritionalValueExtractor:
    """
    A class to extract nutritional information from a CSV dataset based on approximate food name matching.
    """

    def __init__(self, csv_path, score_cutoff=70, top_n=5):
        """
        Initializes the extractor with a given CSV file containing nutritional values.
        
        Args:
            csv_path (str): Path to the CSV file containing food data.
            score_cutoff (int): Minimum fuzzy match score to consider as a match. Default is 70.
            top_n (int): Maximum number of top matches to return. Default is 5.
        """
        self.csv_path = csv_path
        self.score_cutoff = score_cutoff
        self.top_n = top_n

        # Setup logger
        self.logger = logging.getLogger("NutritionSearchEngine")
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(ch)

        self.df = None
        self.load_data()

    def load_data(self):
        """
        Loads and prepares the dataset by reading the CSV file, applying column names,
        and normalizing the food names for consistent searching.
        """
        self.logger.info(f"Loading data from {self.csv_path}")
        self.df = pd.read_csv(self.csv_path, header=None)
        self.df.columns = [
            "food_code", "food_name", "primarysource", "secondarysource",
            "Primary food group", "food_group_nin", "energy_kj", "energy_kcal",
            "carbohydrate_g", "protein_g", "fat_g", "freesugar_g", "fibre_g"
        ]
        self.df["normalized_name"] = self.df["food_name"].apply(self.normalize)
        self.logger.info("Data loaded and normalized successfully.")

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalizes a string by converting to lowercase, removing punctuation, and trimming whitespace.

        Args:
            text (str): The input text to normalize.

        Returns:
            str: A cleaned and normalized version of the input text.
        """
        text = str(text).lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def search_food(self, query: str) -> List[str]:
        """
        Searches for food items that match the given query using fuzzy string matching.

        Args:
            query (str): The name of the food item to search for.

        Returns:
            list[dict] | dict: A list of dictionaries containing matched food items and their
            nutritional values (protein, fat, carbohydrates, fibre), or a warning message
            if no matches are found.
        """
        self.logger.info(f"Searching for: '{query}'")
        query_norm = self.normalize(query)
        matches = process.extract(
            query_norm,
            self.df["normalized_name"],
            scorer=fuzz.token_sort_ratio,
            limit=self.top_n,
            score_cutoff=self.score_cutoff
        )

        if not matches:
            warning_msg = f"WARNING: No match found for '{query}'"
            self.logger.warning(warning_msg)
            return {"warning": warning_msg}

        results = []
        for match in matches:
            matched_name, score = match[0], match[1]
            row = self.df[self.df["normalized_name"] == matched_name].iloc[0]
            results.append({
                "Food Name": row["food_name"],
                "Protein (g)": row["protein_g"],
                "Fat (g)": row["fat_g"],
                "Carbohydrates (g)": row["carbohydrate_g"],
                "Fibre (g)": row["fibre_g"]
            })

        self.logger.info(f"Found {len(results)} matches for '{query}'")
        return results
