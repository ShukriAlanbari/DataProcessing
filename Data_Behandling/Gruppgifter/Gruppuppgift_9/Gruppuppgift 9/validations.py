import re

class Validation:
        
        
        @staticmethod
        def validate_is_alnum(value: str):
            if isinstance(value,str) and value.replace(" ", "").isalnum():
                return True
            else:
                return False
            
        @staticmethod
        def validate_str_alpha(value:str):
            if isinstance(value, str) and value.replace(" ", "").isalpha():
                return True
            else:
                return False
        
        @staticmethod
        def validate_int(value):
            return isinstance(value,int)
        
        @staticmethod
        def validate_float(value):
            return isinstance(value,float)
                

        
        @staticmethod
        def validate_item_type(value):
            return value.lower() in ("fragile", "solid")
        
        @staticmethod
        def validate_payment_method(value):
            return value.lower() in ("net", "debit", "credit")
        
        @staticmethod
        def validate_vehicle_type(value):
            return value.upper() in ("B", "T", "S")
        
        @staticmethod
        def validate_password(value:str):
            if len(value) < 8:
                print("\n[!] Bad Value - Password should at"
                      " least be 8 characters.\n")
                return False

            if len(value) >= 18:
                print("\n[!] Bad Value - Password can't be"
                      " over 18 characters.\n")
                return False

            spec_char = r"[!@#$%^&*()_+={}\[\]:;<>,.?~\\-]"
            if not re.search(spec_char, value):
                print("\n[!] Bad Value - Password should at least"
                      " include 1 special character.\n")
                return False
            
            if not any(char.isdigit() for char in value):
                print("\n[!] Bad Value - Password should at least"
                      " include 1 number.\n")
                return False
            
            if not any(char.isupper() for char in value):
                print("\n[!] Bad Value - Password should at least"
                      " have 1 uppercase letter.\n")
                return False
            
            if not any(char.islower() for char in value):
                print("\n[!] Bad Value - Password should at least"
                      " have 1 lowercase letter.\n")
                return False
            
            return True
        
        @staticmethod
        def validate_card_number(value:str):
            if not all(char.isdigit() for char in value):
                print("\n[!] Bad Value - Card Number must be only Digits\n")
                return False
            if len(value) != 16:
                print("\n[!] Bad Value - Card Number must be 16 Digits\n")
                return False
            
            return True
        
        @staticmethod
        def validate_company_id(value:str):
            if not len(value) == 12:
                print("[!] Bad Value - Has to be 12 characters long.")
                return False
            if not all(char.isdigit() for char in value):
                print("[!] Bad Value - Has to be digits only.")
                return False
            
            return True
            
        @staticmethod
        def read_in_int_value(validation_function, message:str):
            while True:
                user_input = input(message)
                if user_input.isnumeric() and \
                    validation_function(int(user_input)):
                    return int(user_input)
        
        @staticmethod
        def read_in_float(validation_function, message:str):
            while True:
                user_input = input(message)
                try:
                    float_value = float(user_input)
                except ValueError:
                    print("Invalid input. Please enter a valid float.")
                    continue
                if validation_function(float_value):
                    return float_value

        @staticmethod
        def read_in_value(validation_function,message:str):
            while True:
                user_input = input(message)
                if validation_function(user_input):
                    return user_input


        @staticmethod
        def validate_mob_num(value:str):
            regex = r"^\+[0-9]+(\s?[0-9\-\(\)\/\.]){6,15}[0-9]$"
            if re.match(regex, value):
                return True
            else:
                print("[!] Bad Value - Ex \"+yyxxxxxxxxx")
                return False
            
        def validate_email(value:str):
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,6}\b"
            if re.match(regex, value):
                return True
            else:
                print("\n[!] Bad Value - Ex \"xxxxx@yyyy.zzz\"\n")
                return False


        @staticmethod
        def valid_id(value:str):
            if isinstance(value, str) and len(value.strip()) == 10:
                return True
            else:
                return False