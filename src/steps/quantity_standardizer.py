import logging
import re
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from fractions import Fraction
from typing import Tuple, Union

class QuantityStandardizer:
    def __init__(self):
        """
        Initializes the QuantityStandardizer with a Gemini model instance, logging configuration,
        and a measurement conversion table for common Indian household units.
        """
        # Configure Gemini
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            model_kwargs={
                "response_mime_type": "application/json"
            }
        )
        # Logger
        self.logger = logging.getLogger("QuantityStandardizer")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        if not self.logger.handlers:
            self.logger.addHandler(handler)

        # Household measurement standard conversion table (in ml/count for pieces and piece)
        self.measurements = {
            "pieces": 1,
            "piece": 1,
            "count": 1,
            "cup": 150,
            "katori": 150,
            "glass": 250,
            "teaspoon": 5,
            "tablespoon": 15,
            "teacup": 100,
        }

    def normalize_unit(self, unit: str) -> str:
        """
        Normalize a unit by converting it to lowercase, stripping whitespace and plural suffixes,
        and matching it against known household measurements.

        Args:
            unit (str): The unit to normalize.

        Returns:
            str: Normalized unit if found, or original unit for unknowns.
        """
        unit = unit.lower().strip()
        unit = re.sub(r's$', '', unit)  # remove plural
        for key in self.measurements:
            if key in unit:
                return key
        return unit  # unknown units will be handled by LLM

    def parse_quantity(self, text: str) -> Tuple[float, str]:
        """
        Parse a quantity string (e.g., "1 1/2 cups", "3/4 glass") into a float value and a unit.

        Args:
            text (str): The quantity string.

        Returns:
            Tuple[float, str]: The numerical quantity and the unit string.

        Raises:
            ValueError: If the quantity format is invalid.
        """
        try:
            text = text.strip()

            # Match mixed numbers, fractions, decimals, and integers, with optional units
            match = re.match(r"^(\d+\s+\d+/\d+|\d+/\d+|\d+\.?\d*|\d+)\s*([a-zA-Z\s]*)$", text)
            if not match:
                raise ValueError(f"Invalid quantity format: '{text}'")

            quantity_str, unit = match.groups()
            quantity_str = quantity_str.strip()

            if ' ' in quantity_str:
                whole, frac = quantity_str.split()
                quantity = float(whole) + float(Fraction(frac))
            elif '/' in quantity_str:
                quantity = float(Fraction(quantity_str))
            else:
                quantity = float(quantity_str)

            unit = unit.strip() if unit else ""
            return quantity, unit
        except Exception as e:
            raise ValueError(f"Invalid quantity format: '{text}'")

    def estimate_grams(self, ingredient: str, quantity_text: str) -> Union[float, dict]:
        """
        Estimate the weight in grams of an ingredient based on a quantity description.

        If the unit is a known household measurement, it is converted to ml or count, then
        a Gemini model is used to estimate the grams. If not known, the raw input is passed
        to the model for estimation.

        Args:
            ingredient (str): The name of the ingredient.
            quantity_text (str): The text representing quantity and unit.

        Returns:
            Union[float, dict]: The estimated weight in grams or an error dictionary if failed.
        """
        self.logger.info(f"Estimating grams for: '{quantity_text} of {ingredient}'")

        try:
            quantity, unit_raw = self.parse_quantity(quantity_text)
            unit = self.normalize_unit(unit_raw)
        except Exception as e:
            self.logger.error(str(e))
            return {"error": f"Invalid quantity format: '{quantity_text}'"}

        if unit in self.measurements:
            volume_or_count = self.measurements[unit] * quantity
            self.logger.info(f"Standardized measurement: {volume_or_count} ml/counts")

            prompt = (
                f"Estimate the weight in grams of {volume_or_count}ml or equivalent count "
                f"of '{ingredient}' based on common Indian household measurements. "
                f"Return only the number in grams, no explanation."
            )
        else:
            prompt = (
                f"Estimate the weight in grams of {quantity_text} of '{ingredient}' "
                f"based on common Indian household measurements. "
                f"Return only the number in grams, no explanation."
            )

        try:
            response = self.model.invoke(prompt)

            response_text = response if isinstance(response, str) else getattr(response, "content", None) or getattr(response, "text", None)

            if not isinstance(response_text, str):
                raise ValueError("Gemini response is not a valid string")

            match = re.search(r"\d+(\.\d+)?", response_text)
            if not match:
                raise ValueError("Could not extract number from Gemini response")

            grams = float(match.group())
            self.logger.info(f"Estimated grams: {grams}")
            return grams
        except Exception as e:
            self.logger.error(f"Failed to parse Gemini response: {e}")
            return {"error": "Could not estimate grams."}
