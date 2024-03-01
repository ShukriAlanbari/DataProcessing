import csv
import os
import pandas as pd
from validations import Validation as Vald
from address import Address
class User:
    def __init__(self,
                 full_name,
                 address,
                 mobile_number,
                 email,
                 password:None):
        try:
            self.id = User.get_next_user_id()
            if Vald.validate_str_alpha(full_name):
                self.full_name = full_name
            else:
                raise ValueError("[!] Bad value - Enter your Full Name.")
            if isinstance(address,Address):
                self.address = address
            else:
                raise ValueError("[!] Bad Value - Address.")
            if Vald.validate_mob_num(mobile_number):
                self.mobile_number = mobile_number
            else:
                raise ValueError("[!] Bad Value - Mobile number.")
            if Vald.validate_email(email):
                self.email = email
            else:
                raise ValueError("[!] Bad Value - Email.")
            if password is not None:
                if Vald.validate_password(password):
                    self.password = password
                else:
                    raise ValueError("[!] Bad Value - Password")
        except Exception as error:
            print(error)

    def __str__(self):
        return f"\nUser ID: {self.id}\nFull Name: {self.full_name}"\
                f"Address: {self.address}\nMobile Number: {self.mobile_number}\n"\
                f"Email: {self.email}\nPassword: {self.password}"
# Returns the next user ID
    @staticmethod
    def get_next_user_id():
        user_count = User.count_existing_users()
        return f"U{user_count + 1}"
# Counts the users in the csv
    @staticmethod
    def count_existing_users():
        try:
            with open("user_db.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                user_count = sum(1 for _ in reader)
                return user_count
        except FileNotFoundError:
            return 0  # File doesn't exist, so no users yet
# Creates a csv file for user_db if none exists
    @staticmethod
    def create_csv_file_if_not_exists():
        # if not os.path.isfile("user_db.csv"):
        #     with open("user_db.csv", mode="w", newline="") as file:
        #         writer = csv.writer(file)
        #         writer.writerow(["ID", "Full Name", "Address",
        #                          "Mobile Number", "Email", "Password"])
        if not os.path.isfile("user_db.csv"):
            header = ["ID", "Full Name", "Address", "Mobile Number", "Email", "Password"]
            pd.DataFrame(columns=header).to_csv("user_db.csv", index=False)
# Saves the user data into the csv
    def save_user_data_into_csv(self):
        # self.create_csv_file_if_not_exists()
        # with open("user_db.csv", mode="a", newline="") as file:
        #     writer = csv.writer(file)
        #     writer.writerow([self.id, self.full_name, str(self.address),
        #                      self.mobile_number, self.email, self.password])
        user_data = {
        'id': [self.id],
        'full_name': [self.full_name],
        'address': [str(self.address)],
        'mobile_number': [self.mobile_number],
        'email': [self.email],
        'password': [self.password]
    }
        user_df = pd.DataFrame(user_data)

        user_df.to_csv('user_db.csv', mode='a', index=False, header=not os.path.exists('user_db.csv'))
# Removes the data from the Users ID
    def remove_user_by_id(user_id):
        with open("user_db.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
        found = False
        updated_rows = []
        for row in rows:
            if row[0] == user_id:
                found = True
            else:
                updated_rows.append(row)
        # If the user was found and removed, rewrite the CSV file
        if found:
            with open("user_db.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            return True
        else:
            return False
# We can get the users info by Users ID       
    def get_user_by_id(user_id):
        with open("user_db.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                user_id, full_name, address, \
                    mobile_number, email, user_password = row
                
                if user_id == user_id:
                    address_values = address.split(", ")
                    
                    if len(address_values) == 4:
                        street_name, house_apt_num, \
                            zip_code, city_name = address_values
                        address = Address(street_name, house_apt_num, 
                                            int(zip_code), city_name)
                        return User(full_name=full_name, address=address, 
                                    mobile_number=mobile_number, 
                                    email=email, password=user_password)
        return None 