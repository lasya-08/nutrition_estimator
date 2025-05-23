import logging

class CategorizeDishes:
    """
    CategorizeDishes class is used to categorize food items based on their weight.
    It uses predefined weight ranges to assign each dish into categories such as soups, rice items,
    flatbreads, chutneys, etc.
    """

    def __init__(self):
        """
        Initializes the CategorizeDishes class by setting up the logger to track categorization events.
        """
        self.logger = logging.getLogger("Categorize Dishes")
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(ch)

    def categorize_dish(self, weight: float) -> str:
        """
        Categorizes a dish based on its weight in grams or milliliters.

        Parameters:
        - weight (float): The weight of the dish.

        Returns:
        - str: A string representing the dish category, or None if no category matches.
        """
        category = ""

        # Conditional categorization based on weight
        if weight >= 250:
            category = "Mixed Soups / Hot Beverages / Beverages"
        elif 150 <= weight < 250:
            category = "Wet Rice Item / Veg Gravy / Non-Veg Gravy / Dals / Raita / Plain Soup"
        elif 125 <= weight < 150:
            category = "Dry Rice Item"
        elif weight == 124:
            category = "Dry Rice Item"
        elif 100 <= weight < 125:
            category = "Veg Fry / Non-Veg Fry / Dry Breakfast Item / Salads / Snacks / Stuffed Flatbreads"
        elif 130 <= weight < 150:
            category = "Wet Breakfast Item"
        elif 120 <= weight < 124:
            category = "Sweets"
        elif 100 <= weight == 120:
            category = "Stuffed Flatbreads"
        elif 15 <= weight < 50:
            category = "Plain Flatbread"
        elif weight <= 15:
            category = "Chutneys"
        else:
            self.logger.warning(f"No matching category for weight: {weight}g/ml")
            return None

        # Log and return the category
        self.logger.info(f"Weight {weight}g/ml categorized as: {category}")
        return category
