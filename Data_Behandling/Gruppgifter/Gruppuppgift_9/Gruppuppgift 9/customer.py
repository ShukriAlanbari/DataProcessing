from validations import Validation as Vald
from user import User
from address import Address
import csv
import os

class Customer(User):
    def __init__(self,
                 full_name, 
                 address, 
                 mobile_number, 
                 email,
                 company_id, 
                 company_name, 
                 company_email):
        super().__init__(full_name=full_name, address=address,
                         mobile_number=mobile_number,
                         email=email, password=None)
        
        self.id = Customer.get_next_customer_id()
        if Vald.validate_company_id(company_id):
            self.company_id = company_id
        else:
            raise ValueError("[!] Bad Value - Company ID.")

        if Vald.validate_is_alnum(company_name):
            self.company_name = company_name
        else:
            raise ValueError("[!] Bad Value - Company Name.")

        if Vald.validate_email(company_email):
            self.company_email = company_email
        else:
            raise ValueError("[!] Bad Value - Company Email.")
        
        self.related_users = []
        self.full_name = full_name
        self.address = address
        self.mobile_number = mobile_number
        self.email = email

    def __str__(self):
        return f"\nID: {self.id}\nCompany ID: {self.company_id}\n"\
            f"Company Name: {self.company_name}\nFull Name: {self.full_name}"\
            f"\nMobile Number: {self.mobile_number}\n"\
            f"Email: {self.email}\nCompany Email: {self.company_email}\n"\
            f"Related Users: {self.related_users}"
# Returns the next Customer ID 
    @staticmethod
    def get_next_customer_id():
        user_count = Customer.count_existing_customers()
        return f"C{user_count + 1}"
# Counts the Customer in the csv
    @staticmethod
    def count_existing_customers():
        try:
            with open("customer_db.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                user_count = sum(1 for _ in reader)
                return user_count
        except FileNotFoundError:
            return 0
# Creates a csv file for customer_db if none exists       
    @staticmethod
    def create_csv_file_if_not_exists():
        if not os.path.isfile("customer_db.csv"):
            with open("customer_db.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Company ID", "Company Name",
                                 "Full Name", "Address", "Mobile Number",
                                 "Email", "Company Email", "Related Users"])
# Saves the customer data into the csv
    def save_customer_data_into_csv(self):
        self.create_csv_file_if_not_exists()
        with open("customer_db.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.id, self.company_id, self.company_name,
                             self.full_name, str(self.address),
                             self.mobile_number, self.email,
                             self.company_email, self.related_users])
# Removes the data from the Customer ID
    def remove_customer_by_id(customer_id):
        with open("customer_db.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
        found = False
        updated_rows = []
        for row in rows:
            if row[0] == customer_id:
                found = True
            else:
                updated_rows.append(row)
        # If the user was found and removed, rewrite the CSV file
        if found:
            with open("customer_db.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            return True
        else:
            return False
# Checks if it exists a User with the specific ID
    def add_related_user(self, user_id):
        if user_id not in self.related_users:
            self.related_users.append(user_id)
# Load in the customers data into a dict
    def load_customer_info():
        customer_info = {}
        with open("customer_db.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer_info[row["ID"]] = row["Full Name"]
        return customer_info
# We can get the cusotmers info by Customer ID   
    def get_customer_by_id(customer_id):
        with open("customer_db.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                (id, company_id, company_name, full_name, address, \
                 mobile_number, email, company_email, * related_users) = row
                if id == customer_id:
                    address_values = address.split(", ")
                    if len(address_values) == 4:
                        street_name, house_apt_num, \
                        zip_code, city_name = address_values
                        address = Address(street_name, house_apt_num, 
                                          int(zip_code), city_name)
                        return Customer(
                            company_id=company_id, company_name=company_name,
                            full_name=full_name, address=address,
                            mobile_number=mobile_number, email=email,
                            company_email=company_email
                        )
        return None
