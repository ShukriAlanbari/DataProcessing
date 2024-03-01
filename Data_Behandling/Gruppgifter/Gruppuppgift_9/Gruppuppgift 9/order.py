import os
import csv
from datetime import datetime

class Order:
    def __init__(self, 
                 sender, to_location, 
                 payment_details, 
                 items:list, 
                 total_weight,
                 order_status:str,
                 order_place_datetime,
                 order_delivery_datetime:str, 
                 vehicle=None, vehicle_type=None):
        self.id = Order.get_next_order_id()
        self.sender = sender
        self.to_location = to_location
        self.payment_details = payment_details
        self.items = items
        self.order_status = order_status
        self.order_place_datetime = datetime.now().date()
        self.order_delivery_datetime = datetime.now() if \
                                    order_delivery_datetime else None
        self.vehicle = vehicle
        self.vehicle_type = vehicle_type
        self.total_weight = total_weight

    def __str__(self):
        return f"Order ID: {self.id}\n"\
            f"Sender/Customer: {self.sender}\n"\
            f"To Location: {self.to_location}\n"\
            f"Payment Details: {self.payment_details}\n"\
            f"Items: {len(self.items)}\n"\
            f"Total Weight: {self.total_weight}\n"\
            f"Order Status: {self.order_status}\n"\
            f"Order Place Date/Time: {self.order_place_datetime}\n"\
            f"Order Delivery Date/Time: {self.order_delivery_datetime}\n"\
            f"Vehicle ID: {self.vehicle if self.vehicle else 'N/A'}"
# Returns the next Order ID  
    @staticmethod
    def get_next_order_id():
        order_count = Order.count_existing_orders()
        return f"O{order_count + 1}"
# Counts the Orders in the csv
    @staticmethod
    def count_existing_orders():
        try:
            with open("order_db.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                order_count = sum(1 for _ in reader)
                return order_count
        except FileNotFoundError:
            return 0
# Updates the delivery status for the specific Order ID
    def update_order_status( order_id, new_status):
        updated_order_data = []
        order_updated = False
        with open("order_db.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not order_updated and row["order_id"] == order_id:
                    row["order_status"] = new_status
                    if new_status == "Delivered":
                        row["order_delivery_datetime"] = datetime.now(
                                                ).strftime('%Y-%m-%d')
                    order_updated = True
                updated_order_data.append(row)

        with open("order_db.csv", mode="w", newline="") as file:
            fieldnames = ["order_id", "sender", "to_location",
                        "payment_details","items", "total_weight",
                        "order_status", "order_place_datetime",
                        "order_delivery_datetime", "vehicle"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_order_data)
# Creates a csv file for order_db if none exists  
    @staticmethod
    def create_csv_file_if_not_exists():
        if not os.path.isfile("order_db.csv"):
            with open("order_db.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["order_id", "sender",
                        "to_location", "payment_details", "items",
                        "total_weight", "order_status", "order_place_datetime",
                        "order_delivery_datetime", "vehicle"])
# Saves the Order to the csv
    def save_orders_to_csv(self):
        self.create_csv_file_if_not_exists()
        with open("order_db.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.id, self.sender, self.to_location,
                            self.payment_details, len(self.items),
                            self.total_weight, self.order_status,
                            self.order_place_datetime.isoformat(),
                            self.order_delivery_datetime.isoformat() \
                                if self.order_delivery_datetime else "",
                            self.vehicle if self.vehicle else ""])
# Gets the order by the ID
    def get_order_by_id(order_id):
        with open("order_db.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["order_id"] == order_id:
                    sender = row["sender"]
                    to_location = row["to_location"]
                    payment_details = row["payment_details"]
                    items = len(row["items"])
                    total_weight = row["total_weight"]
                    order_status = row["order_status"]
                    order_place_datetime = row["order_place_datetime"]
                    order_delivery_datetime = row["order_delivery_datetime"]
                    vehicle = row["vehicle"]

                    return Order(
                        sender=sender,
                        to_location=to_location,
                        payment_details=payment_details,
                        items=items,
                        total_weight=total_weight,
                        order_status=order_status,
                        order_place_datetime=order_place_datetime,
                        order_delivery_datetime=order_delivery_datetime,
                        vehicle=vehicle)
        return None
