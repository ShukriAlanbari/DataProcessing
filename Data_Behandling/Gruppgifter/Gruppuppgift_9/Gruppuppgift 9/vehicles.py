from location import Location
import os
import csv
from validations import Validation as Vald

class Vehicle:
    vehicle_id_counters = {}
    start_location = Location(latitude=57.7, longitude=11.95, country="Sweden")
    def __init__(self, vehicle_type,
                 max_cap_kg: float,
                 max_cap_items: int,
                 current_pos: str,
                 current_stat: str) -> None:
        if Vald.validate_vehicle_type(vehicle_type):
            self.vehicle_type = vehicle_type
        else:
            raise ValueError("[!] Bad Value - Vehicle Type ('B', 'T', 'S')")
        if vehicle_type not in Vehicle.vehicle_id_counters:
            Vehicle.vehicle_id_counters[vehicle_type] = 0
        Vehicle.vehicle_id_counters[vehicle_type] += 1
        self.vehicle_id = f"{self.vehicle_type}"\
            f"{str(Vehicle.vehicle_id_counters[vehicle_type]).zfill(3)}"
        self.max_cap_kg = max_cap_kg
        self.max_cap_items = max_cap_items
        self.current_pos = current_pos
        self.current_stat = current_stat
        self.left_cap_kg = max_cap_kg
        self.left_cap_items = max_cap_items

    def __str__(self):
        return f"Vehicle ID: {self.vehicle_id}\n"\
            f"Max Capacity (KG): {self.max_cap_kg}\n"\
            f"Max Capacity (Items): {self.max_cap_items}\n"\
            f"Current Position:\n{self.current_pos}\n"\
            f"Current Status: {self.current_stat}\n"\
            f"Left Capacity (KG): {self.left_cap_kg}\n"\
            f"Left Capacity (Items): {self.left_cap_items}\n"
# Inserts the vehicle into a Csv
    def insert_vehicle_data_into_csv(self, csv_file):
        is_new_file = not os.path.isfile(csv_file)
        with open(csv_file, mode="a", newline="") as file:
            fieldnames = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                          "max_capacity_items", "current_pos", "current_stat"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if is_new_file:
                writer.writeheader()

            writer.writerow({
                "vehicle_type": self.vehicle_type,
                "vehicle_id": self.vehicle_id,
                "max_capacity_kg": self.max_cap_kg,
                "max_capacity_items": self.max_cap_items,
                "current_pos": self.current_pos,
                "current_stat": self.current_stat
            })
# Load vehicles into a Dict
    @staticmethod
    def load_vehicles_from_csv(csv_file):
        vehicles = []
        if not os.path.isfile(csv_file):
            return vehicles

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                vehicle_type = row["vehicle_type"]
                if vehicle_type == "B":
                    vehicle = Bike(
                        current_pos=row["current_pos"],
                        current_stat=row["current_stat"]
                    )
                elif vehicle_type == "T":
                    vehicle = Truck(
                        current_pos=row["current_pos"],
                        current_stat=row["current_stat"]
                    )
                elif vehicle_type == "S":
                    vehicle = Ship(
                        current_pos=row["current_pos"],
                        current_stat=row["current_stat"]
                    )
                vehicles.append(vehicle)
        return vehicles
# Updates the vehicle status to Loading
    def loading_vehicle_stat(csv_filename, vehicle_id):
        updated_vehicle_data = []
        vehicle_updated = False
        
        with open(csv_filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not vehicle_updated and row["vehicle_id"] == vehicle_id \
                    and row["current_stat"] == "Free":
                    row["current_stat"] = "Loading"
                    vehicle_updated = True
                updated_vehicle_data.append(row)

        with open(csv_filename, mode="w", newline="") as file:
            fieldnames = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                          "max_capacity_items", "current_pos", "current_stat"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_vehicle_data)
# Updates the vehicle status to a New status
    def update_vehicle_stat(csv_filename, vehicle_id, new_status):
        updated_vehicle_data = []
        vehicle_updated = False
        
        with open(csv_filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not vehicle_updated and row["vehicle_id"] == vehicle_id:
                    row["current_stat"] = new_status
                    vehicle_updated = True
                updated_vehicle_data.append(row)

        with open(csv_filename, mode="w", newline="") as file:
            fieldnames = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                        "max_capacity_items", "current_pos", "current_stat"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_vehicle_data)
# Updates the vehicle location
    def update_vehicle_location(db_filename, vehicle_id, new_location):
        updated_vehicle_data = []

        with open(db_filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["vehicle_id"] == vehicle_id:
                    row["current_pos"] = new_location
                updated_vehicle_data.append(row)

        with open(db_filename, mode="w", newline="") as file:
            fieldnames = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                          "max_capacity_items", "current_pos", "current_stat"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_vehicle_data)
# Checks if there are a free vehicle and if it fit the requirements
    @staticmethod
    def get_vehicle_by_free(csv_file, vehicle_type,
                            required_weight, required_items):
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["current_stat"] == "Free" \
                    and row["vehicle_type"] == vehicle_type:
                    max_capacity_kg = float(row["max_capacity_kg"])
                    max_capacity_items = int(row["max_capacity_items"])

                    if max_capacity_kg >= required_weight \
                        and max_capacity_items >= required_items:
                        return row["vehicle_id"]
                    else:
                        print("[!] The order is too heavy"
                              f" or too big for vehicle: {vehicle_type}")
        print("[!] No Avalaible Vehicles")
        return None

    @classmethod
    def get_vehicle_capacity(cls, vehicle_type):
        if vehicle_type == "B":
            return 10, 2 
        elif vehicle_type == "T":
            return 3000, 100
        elif vehicle_type == "S":
            return 100000, 10000
        else:
            return None, None
# Bike Class and its specification  
class Bike(Vehicle):
    vehicle_type = "B"
    def __init__(self, current_pos, current_stat) -> None:
        max_cap_kg = 10
        max_cap_items = 2
        super().__init__(Bike.vehicle_type, max_cap_kg,
                         max_cap_items, current_pos, current_stat)

    @classmethod
    def create_new_bike(cls, csv_file):
        if not os.path.isfile(csv_file):
            header = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                      "max_capacity_items", "current_pos", "current_stat"]
            with open(csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
        
        new_bike = cls(current_pos=Vehicle.start_location, current_stat="Free")
        new_bike.insert_vehicle_data_into_csv(csv_file)
        return new_bike
# Truck Class and its specification  
class Truck(Vehicle):
    vehicle_type = "T"
    def __init__(self, current_pos, current_stat) -> None:
        max_cap_kg = 3000
        max_cap_items = 100
        super().__init__(Truck.vehicle_type, max_cap_kg,
                         max_cap_items, current_pos, current_stat)

    @classmethod
    def create_new_truck(cls, csv_file):
        if not os.path.isfile(csv_file):
            header = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                      "max_capacity_items", "current_pos", "current_stat"]
            with open(csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        new_truck = cls(current_pos=Vehicle.start_location, current_stat="Free")
        new_truck.insert_vehicle_data_into_csv(csv_file)
        return new_truck
# Ship Class and its specification  
class Ship(Vehicle):
    vehicle_type = "S"
    def __init__(self, current_pos, current_stat) -> None:
        max_cap_kg = 100000
        max_cap_items = 10000
        super().__init__(Ship.vehicle_type, max_cap_kg,
                         max_cap_items, current_pos, current_stat)

    @classmethod
    def create_new_ship(cls, csv_file):
        if not os.path.isfile(csv_file):
            header = ["vehicle_type", "vehicle_id", "max_capacity_kg",
                      "max_capacity_items", "current_pos", "current_stat"]
            with open(csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        new_ship = cls(current_pos=Vehicle.start_location, current_stat="Free")
        new_ship.insert_vehicle_data_into_csv(csv_file)
        return new_ship
