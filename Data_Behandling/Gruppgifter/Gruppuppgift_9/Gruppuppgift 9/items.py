from validations import Validation as Vald
class Item:

    def __init__(self, weight, item_type) -> None:

        self.price_per_kg = 70 if item_type.lower() == "fragile" else 50
        if Vald.validate_float(weight):
            self.weight = weight
        else:
            raise ValueError("[!] Bad value - Enter Weight in KG.")
        if Vald.validate_item_type(item_type):
            self.item_type = item_type
        else:
            raise ValueError("[!] Bad value - Enter 'Fragile' or"
                             " 'Solid' for item type.")
        

    def __str__(self):
        return f"Type: {self.item_type}\nPrice per kg: {self.price_per_kg} SEK"\
                f"\nWeight: {self.weight} kg"
# Calculates the total price in Items
    @staticmethod
    def calculate_total_price(items):
        total_price = 0
        for item in items:
            total_price += item.weight * item.price_per_kg
        return total_price