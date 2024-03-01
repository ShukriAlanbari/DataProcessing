import os
import csv
from validations import Validation as Vald

class Payment:
    def __init__(self, payment_method,
                 amount, payment_status,
                 card_number=None,
                 card_holder_info=None):
        if Vald.validate_payment_method(payment_method):
            self.payment_method = payment_method
        else:
            raise ValueError("[!] Bad Value - Enter 'Net','Debit' or"
                            " 'Credt' for payment method")
        self.transaction_id = Payment.get_next_tran_id()
        if Vald.validate_float(amount):
            self.amount = amount
        else:
            raise ValueError("[!] Bad Value - Amount")
        self.payment_status = payment_status
        self.card_number = card_number
        self.card_holder_info = card_holder_info
        if card_number is not None and card_number != "" and not \
                            Vald.validate_card_number(card_number):
            raise ValueError("[!] Bad Value - Card Number")

        if card_holder_info is not None and card_holder_info != "" and not \
                                Vald.validate_str_alpha(card_holder_info):
            raise ValueError("[!] Bad value - Enter your Full Name")
        

    def __str__(self):
        amount_sek = f"{self.amount} SEK"
        payment_info = f"Transaction ID: {self.transaction_id}\n"\
            f"Payment Method: {self.payment_method}\n"\
                    f"Amount: {amount_sek}\n"
        if self.card_number:
            payment_info += f"Card Number: {self.card_number}\n"\
                        f"Card Holder Info: {self.card_holder_info}\n"
        payment_info += f"Payment Status: {self.payment_status}"
        return payment_info
# Returns the next Transaction ID    
    @staticmethod
    def get_next_tran_id():
        tran_count = Payment.count_existing_tran()
        return f"T{tran_count + 1}"
# Counts the Transactions in the csv
    @staticmethod
    def count_existing_tran():
        try:
            with open("transaction_db.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                tran_count = sum(1 for _ in reader)
                return tran_count
        except FileNotFoundError:
            return 0
# Creates a csv file for cardinfo_db if none exists
    @staticmethod
    def create_csv_file_card_info():
        if not os.path.isfile("cardinfo_db.csv"):
            with open("cardinfo_db.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Card Number", "Card Holder"])
# Saves the card info if user pay with Debit or Credit
# Also checks if the Card_number already exists in the csv and than returns
# The card holder info for that card
    def save_card_info_to_csv(self):
        self.create_csv_file_card_info()
        card_info = Payment.load_card_info_from_csv("cardinfo_db.csv")
        card_number_exists = False

        if self.card_number is not None:
            for existing_card_number, existing_card_holder_info in card_info:
                if self.card_number == existing_card_number:
                    card_number_exists = True
                    self.card_holder_info = existing_card_holder_info
                    break
        
        if not card_number_exists:
            # Card number not found in the CSV, ask for the card holder info
            if self.card_number:
                self.card_holder_info = input("Enter the card holder's name: ")

                with open("cardinfo_db.csv", mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([self.card_number, self.card_holder_info])
# We can get the card information  
    @staticmethod
    def load_card_info_from_csv(filename):
        card_info = []
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    card_number, card_holder_info = row
                    card_info.append((card_number, card_holder_info))
        return card_info
# Creates a csv file for transaction_db if none exists  
    @staticmethod
    def create_csv_file_tran_info():
        if not os.path.isfile("transaction_db.csv"):
            with open("transaction_db.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Tran ID","Payment Method",
                                 "Amount(SEK)","Payment Status",
                                 "Card Number","Card Holder"])
# Saves the transaction to the csv
    def save_to_csv(self):
        self.create_csv_file_tran_info()
        with open("transaction_db.csv", mode='a', newline='') as file:
            writer = csv.writer(file)

            if self.payment_method == "Net":
# For "Net" payments, write only payment method,
# transaction ID, amount, and payment status
                writer.writerow([self.transaction_id,self.payment_method,
                                 self.amount, self.payment_status,
                                 self.card_number, self.card_holder_info])
            else:
# For other payment methods, write all details including card information
                self.save_card_info_to_csv()
                writer.writerow([self.transaction_id, self.payment_method,
                                 self.amount, self.payment_status,
                                 self.card_number, self.card_holder_info])
# Updates the payment status for the specific Transaction ID
    def update_payment_status(transaction_id):
        updated_payment_data = []
        payment_updated = False

        with open("transaction_db.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not payment_updated and row["Tran ID"] == transaction_id:
                    row["Payment Status"] = "Paid"
                    payment_updated = True
                updated_payment_data.append(row)

        with open("transaction_db.csv", mode="w", newline="") as file:
            fieldnames = ["Tran ID","Payment Method",
                                 "Amount(SEK)","Payment Status",
                                 "Card Number","Card Holder"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_payment_data)
# Gets the transaction by the ID
    def get_payment_by_id(transaction_id):
        with open("transaction_db.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Tran ID"] == transaction_id:
                    payment_method = row["Payment Method"]
                    amount = float(row["Amount(SEK)"])
                    payment_status = row["Payment Status"]
                    card_number = row["Card Number"]
                    card_holder_info = row["Card Holder"]

                    return Payment(payment_method=payment_method,
                                   amount=amount, payment_status=payment_status,
                                   card_number=card_number  ,
                                   card_holder_info=card_holder_info)

        return None  # Payment not found
