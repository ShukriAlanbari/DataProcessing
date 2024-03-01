import csv
import os
from datetime import datetime
from user import User
from customer import Customer
from address import Address
from validations import Validation as Vald
from vehicles import Vehicle, Bike, Truck, Ship
from order import Order
from items import Item
from payment import Payment
from location import Location
# Starting Menu
def show_menu():
    PROMPT_MENU = '''
1. Login as User
2. Create User
3. Create Customer
4. Order
'''
    print(PROMPT_MENU)
# Vehicle menu for User
def show_vehicle_menu():
    PROMPT_MENU = '''
1. Add bike
2. Add truck
3. Add ship
4. Go back
'''
    print(PROMPT_MENU)
# Vehicle info for picking the right Vehicle in Order
def show_vehicle_options():
    PROMPT_MENU = '''
Choice, Type, Weight, Items
 "B": ( Bike,   10,     2  )
 "T": (Truck,  3000,   10  )
 "S": ( Ship, 100000, 10000)
'''
    print(PROMPT_MENU)
# Menu for User
def show_user_options():
    PROMPT_MENU = '''
1. Users
2. Customers
3. Vehicles
4. Update Payment
5. Update Order & Location
6. Go back
'''
    print(PROMPT_MENU)
# Menu for change of Users
def show_user_menu():
    PROMPT_MENU = '''
1. Show User List
2. Update User
3. Remove User
4. Go back
'''
    print(PROMPT_MENU)
# Menu for change of Customers
def show_customer_menu():
    PROMPT_MENU = '''
1. Show Customer List
2. Update Customer
3. Remove Customer
4. Go back
'''
    print(PROMPT_MENU)
# Login for User to get to User menu
def user_login():
    while True:
        user_id = input("Enter your User ID('x' for Exit): ")
        password = input("Enter your Password('x' for Exit): ")

        found_user = User.get_user_by_id(user_id)
        if found_user and found_user.password == password:
            print("\nLogin Successful!")
            user_menu()
            break
        elif user_id.lower() == "x" or password.lower() == "x":
            break
        else:
            print("Login failed. Invalid user ID or password.")
            continue
# Where we can update the payment status by ID
def update_payment():
    while True:
        tran_id = input("Enter the ID for the transaction"
                        " that you want to update('x' for Exit): ")
        found_tran = Payment.get_payment_by_id(tran_id)
        if found_tran:
            print("Updating payment status to 'Paid'.")
            Payment.update_payment_status(tran_id)
            break
        elif tran_id.lower() == "x":
            break
        else:
            print("Invalid Transaction ID.")
            continue
# Where we can update the Order and vehicle Status by ID
# Also change location where the Vehicle is
def update_delivery_status():
    while True:
        order_id = input("Enter the Order ID to update('x' for Exit): ")
        found_order = Order.get_order_by_id(order_id)
        if found_order and found_order.order_status == "Processing":
            Order.update_order_status(order_id,"Delivering")
            vehicle = found_order.vehicle
            if vehicle.startswith("B"):
                db = "bike_db.csv"
            if vehicle.startswith("T"):
                db = "truck_db.csv"
            if vehicle.startswith("S"):
                db = "ship_db.csv"
            latitude = Vald.read_in_float(
                validation_function=Vald.validate_float, 
                message="Update Latitude degree: ")
            longitude = Vald.read_in_float(
                validation_function=Vald.validate_float, 
                message="Update Longitude degree: ")
            country = Vald.read_in_value(
                validation_function=Vald.validate_str_alpha, 
                message="Update the Country: "
            )
            location = Location(latitude=latitude,
                                longitude=longitude,
                                country=country)
            Vehicle.update_vehicle_location(db,vehicle,location)
            Vehicle.update_vehicle_stat(db,vehicle,"Delivering")
            print(f"\nOrder: {order_id} is on its way!.\n")
            return order_id
        elif found_order and found_order.order_status == "Delivering":
            Order.update_order_status(order_id,"Delivered")
            vehicle = found_order.vehicle
            if vehicle.startswith("B"):
                db = "bike_db.csv"
            if vehicle.startswith("T"):
                db = "truck_db.csv"
            if vehicle.startswith("S"):
                db = "ship_db.csv"
            location = Vehicle.start_location
            Vehicle.update_vehicle_stat(db,vehicle,"Free")
            Vehicle.update_vehicle_location(db, vehicle, location)
            print(f"\nOrder: {order_id} is delivered!\n")
            return order_id
        elif order_id.lower() == "x":
            break
        else:
            print("Invalid Order ID.")
            continue
# Function for the change of Users
def user_options():
    while True:
        show_user_menu()
        choice = input("Choice: ")
        if choice == "1":
            csv_data = csv_to_dict("user_db.csv")
            for row in csv_data:
                print(row["ID"],",", row["Full Name"],",", row["Address"],",",
                row["Mobile Number"],",", row["Email"],",", row["Password"])
            continue
        elif choice == "2":
            update_user()
            continue
        elif choice == "3":
            remove_user()
            continue
        elif choice == "4":
            break
        else:
            print("[!] Invalid Input")
# Function for the User Menu
def user_menu():
    while True:
        show_user_options()
        choice = input("Choice: ")
        if choice == "1":
            user_options()
            continue
        elif choice == "2":
            customer_options()
            continue
        elif choice == "3":
            vehicle_menu()
            continue
        elif choice == "4":
            update_payment()
            continue
        elif choice == "5":
            update_delivery_status()
            continue
        elif choice == "6":
            break
        else:
            print("[!] Invalid Input")
# Function for the change of Customers
def customer_options():
    while True:
        show_customer_menu()
        choice = input("Choice: ")
        if choice == "1":
            csv_data = csv_to_dict("customer_db.csv")
            for row in csv_data:
                print(row["ID"],",",
                      row["Company ID"],",",row["Company Name"],",", 
                      row["Full Name"],",", row["Address"],",",
                      row["Mobile Number"],",", row["Email"],",", 
                      row["Company Email"],",", row["Related Users"])
            continue
        elif choice == "2":
            update_customer()
            continue
        elif choice == "3":
            remove_customer()
            continue
        elif choice == "4":
            break
        else:
            print("[!] Invalid Input")
# Takes the csv and turns it into a Dict
def csv_to_dict(csv_filename):
    with open(csv_filename, mode="r") as file:
        return [row for row in csv.DictReader(file)]
# Function for the Vehicle Menu
def vehicle_menu():
    while True:
        show_vehicle_menu()
        choice = input("Choice: ")
        if choice == "1":
            Bike.create_new_bike(csv_file="bike_db.csv")
            print("\n[i] Creating Bike")
            continue
        elif choice == "2":
            Truck.create_new_truck(csv_file="truck_db.csv")
            print("\n[i] Creating Truck")
            continue
        elif choice == "3":
            Ship.create_new_ship(csv_file="ship_db.csv")
            print("\n[i] Creating Ship")
            continue
        elif choice == "4":
            break
        else:
            print("[!] Invalid Input")
# Read in the address from inputs      
def read_address():
    street_name = Vald.read_in_value(
            validation_function=Vald.validate_str_alpha,
            message= "Enter Street name: ")
    house_apt_num = Vald.read_in_value(
            validation_function=Vald.validate_is_alnum,
            message= "Enter House or apartment number: ")
    city_name = Vald.read_in_value(
            validation_function=Vald.validate_str_alpha,
            message= "Enter City name: ")
    zip_code = Vald.read_in_int_value(
            validation_function=Vald.validate_int,
            message= "Enter Zip code: ")
    new_address = Address(street_name=street_name,
                          house_apt_num=house_apt_num,
                          city_name=city_name,
                          zip_code=zip_code)
    return new_address
# Function to create the User
def create_user():
    #full_name = Vald.read_in_value(
           # validation_function=Vald.validate_str_alpha,
           # message= "Enter Full Name: ")
    address = read_address()
    #mobile_number = Vald.read_in_value(
           # validation_function=Vald.validate_mob_num,
           # message= "Enter mobile number: ")
    #email = Vald.read_in_value(
           # validation_function=Vald.validate_email,
            #message= "Enter your email: ")
    #password = None
    #while password is None:
        #password = Vald.read_in_value(
            #validation_function=Vald.validate_password,
            #message="Enter your Password: ")
    new_user = User(full_name="Test Testsson",
                    address=address,
                    mobile_number="+123456789",
                    email="test@test.test",
                    password="Testar1!")
    new_user.save_user_data_into_csv()
    print(new_user)
# Function to get the User ID and update that user
def update_user():
    updated_user_data = None
    while True:
        user_id_to_update = input("Enter the user ID to update('x' for Exit): ")
        found_user = User.get_user_by_id(user_id_to_update)
        if found_user:
            updated_user_data = update_user_info("user_db.csv", user_id_to_update)
            break
        elif user_id_to_update.lower() == "x":
            break
        else:
            print("Invalid user ID.")
            continue
    return updated_user_data

# Function for updating the User data
def update_user_info(csv_filename, user_id):
    updated_user_data = []
    temp_data = []
    # Read user data from the CSV file
    with open(csv_filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == user_id:
                print(f"Updating user with ID {user_id}")
                while True:
                    new_full_name = input("Enter new full name: ")
                    if Vald.validate_str_alpha(new_full_name):
                        row["Full Name"] = new_full_name
                        break
                    else:
                        raise ValueError("[!] Bad value - Entering Full Name.")    
                
                new_address = read_address()
                row["Address"] = str(new_address)
                while True:
                    new_mobile_number = input("Enter new mobile number: ")
                    if Vald.validate_mob_num(new_mobile_number):
                        row["Mobile Number"] = new_mobile_number
                        break
                    else:
                        raise ValueError("[!] Bad value - "
                                         "Entering Mobile Number.")
                while True:
                    new_email = input("Enter new email: ")
                    if Vald.validate_email(new_email):
                        row["Email"] = new_email
                        break
                    else:
                        raise ValueError("[!] Bad value - Entering Email.")
                while True:
                    new_password = input("Enter new password: ")
                    if Vald.validate_password(new_password):
                        row["Password"] = new_password
                        break
                    else:
                        raise ValueError("[!] Bad value - Entering Password.")
            updated_user = row
            temp_data.append(row)

    with open(csv_filename, mode="w", newline="") as file:
        fieldnames = ["ID", "Full Name", "Address", "Mobile Number", "Email", "Password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(temp_data)
    print(f"User information for user {user_id} updated successfully.")
    return updated_user

# Removes the User by their ID
def remove_user():
    while True:
        user_id = input("Enter the user ID to remove('x' for Exit): ")
        user_removed = User.remove_user_by_id(user_id)
        if user_removed:
            print(f"User with ID: {user_id} has been successfully removed.")
            return user_id
        elif user_id.lower() == "x":
            break
        else:
            print(f"User with ID: {user_id} was not found in the database.")
            continue
# Function to create the Customer
def create_customer():
    company_id = Vald.read_in_value(
            validation_function=Vald.validate_company_id,
            message= "Enter your Company ID: ")
    company_name = Vald.read_in_value(
            validation_function=Vald.validate_is_alnum,
            message= "Enter your Company name: ")
    full_name = Vald.read_in_value(
            validation_function=Vald.validate_str_alpha,
            message= "Enter Full Name: ")
    address = read_address()
    mobile_number = Vald.read_in_value(
            validation_function=Vald.validate_mob_num,
            message= "Enter mobile number: ")
    email = Vald.read_in_value(
            validation_function=Vald.validate_email,
            message= "Enter your email: ")
    company_email = Vald.read_in_value(
            validation_function=Vald.validate_email,
            message= "Enter your Company email: ")
    new_customer = Customer(company_id=company_id,  
                    company_name=company_name,
                    full_name=full_name,
                    address=address,
                    mobile_number=mobile_number,
                    email=email,
                    company_email=company_email)
    while True: 
        user_id = input("Enter Related User ID: ")
        found_user = User.get_user_by_id(user_id)
        if found_user:
            new_customer.add_related_user(user_id)
            break
        else:
            print("[!] Bad Value - No User ID in system.")
            continue
    new_customer.save_customer_data_into_csv()
    print(new_customer)
# Function to get the Customer ID and update that user
def update_customer():
    customer_update = None
    while True:
        customer_id_to_update = input("Enter the customer ID"
                                      " to update('x' for Exit): ")
        found_customer = Customer.get_customer_by_id(customer_id_to_update)
        if found_customer:
            customer_update = update_customer_info(customer_id_to_update)
            break
        elif customer_id_to_update.lower() == "x":
            break
        else:
            print("Invalid user ID.")
            continue
    return customer_update

# Function for updating the Customer data
def update_customer_info(customer_id):
    updated_customer_data = []
    updated_customer = []
    with open("customer_db.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == customer_id:
                print(f"Updating Customer with ID: {customer_id}")

                new_com_ID = input("Enter new Company ID: ")
                while not Vald.validate_company_id(new_com_ID):
                    print("[!] Bad value - Entering Company ID.")
                    new_com_ID = input("Enter new Company ID: ")
                row["Company ID"] = new_com_ID

                new_com_name = input("Enter new Company Name: ")
                while not Vald.validate_str_alpha(new_com_name):
                    print("[!] Bad value - Entering Company Name.")
                    new_com_name = input("Enter new Company Name: ")
                row["Company Name"] = new_com_name

                new_full_name = input("Enter new Full Name: ")
                while not Vald.validate_str_alpha(new_full_name):
                    print("[!] Bad value - Entering Full Name.")
                    new_full_name = input("Enter new Full Name: ")
                row["Full Name"] = new_full_name

                new_address = read_address()
                row["Address"] = str(new_address)

                new_mobile_number = input("Enter new Mobile Number: ")
                while not Vald.validate_mob_num(new_mobile_number):
                    print("[!] Bad value - Entering Mobile Number.")
                    new_mobile_number = input("Enter new Mobile Number: ")
                row["Mobile Number"] = new_mobile_number

                new_email = input("Enter new Email: ")
                while not Vald.validate_email(new_email):
                    print("[!] Bad value - Entering Email.")
                    new_email = input("Enter new Email: ")
                row["Email"] = new_email

                new_com_email = input("Enter new Company Email: ")
                while not Vald.validate_email(new_com_email):
                    print("[!] Bad value - Entering Company Email.")
                    new_com_email = input("Enter new Company Email: ")
                row["Company Email"] = new_com_email
            updated_customer = row    
            updated_customer_data.append(row)

    with open("customer_db.csv", mode="w", newline="") as file:
        fieldnames = ["ID", "Company ID", "Company Name", "Full Name", "Address", "Mobile Number", "Email", "Company Email", "Related Users"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_customer_data)

    print(f"Information for Customer {customer_id} updated successfully.")
    return updated_customer
# Removes the Customer by their ID
def remove_customer():
    while True:
        user_id = input("Enter the customer ID to remove('x' for Exit): ")
        customer_removed = Customer.remove_customer_by_id(user_id)
        if customer_removed:
            print(f"Customer with ID: {user_id} has been successfully removed.")
            return user_id
        elif user_id.lower() == "x":
            break
        else:
            print(f"Customer with ID: {user_id} was not found in the database.")
            continue
# Function to get an available vehicle for the order
def get_available_vehicle(order):
    if order.vehicle_type == "B":
        db = "bike_db.csv"
    if order.vehicle_type == "T":
        db = "truck_db.csv"
    if order.vehicle_type == "S":
        db = "ship_db.csv"

    available_vehicle_id = Vehicle.get_vehicle_by_free(
        db, order.vehicle_type, order.total_weight, len(order.items))

    if available_vehicle_id:
        # Vehicle found with sufficient capacity, assign it to the order
        order.vehicle = available_vehicle_id  # Assign the vehicle ID
        # Update the vehicle status to "Unavailable"
        Vehicle.loading_vehicle_stat(db, available_vehicle_id)  # Pass the vehicle ID
        print(f"Vehicle {available_vehicle_id} is assigned to order {order.id}.\n")
        print(order)
        order.save_orders_to_csv()
    return available_vehicle_id
# Function to create an order
def create_order():
    customer_info = Customer.load_customer_info()
    while True:
        customer_id = input("Enter your customer ID: ")
        if customer_id in customer_info:
            sender = customer_info[customer_id]
            break
        else:
            print(f"Customer with ID: {customer_id} was"
                  " not found in the database.")
            continue
    
    latitude = Vald.read_in_float(
        validation_function=Vald.validate_float, 
        message="Enter Latitude degree: ")
    longitude = Vald.read_in_float(
        validation_function=Vald.validate_float, 
        message="Enter Longitude degree: ")
    country = Vald.read_in_value(
        validation_function=Vald.validate_str_alpha, 
        message="Enter your Country: "
    )
    location = Location(latitude=latitude,
                        longitude=longitude,
                        country=country)
    items = []
    items_counter = Vald.read_in_int_value(
        validation_function=Vald.validate_int,
        message="How many items do you want to ship: ")
    item_counter = 1
    for _ in range(int(items_counter)):
        print(f"\nItem: {item_counter}")
        item_counter += 1
        weight = Vald.read_in_float(
            validation_function=Vald.validate_float,
            message="Enter the weight of the item in KG: ")
        item_type = Vald.read_in_value(
            validation_function=Vald.validate_item_type, 
            message="Enter the item type (Fragile or Solid): ")
        item = Item(weight=float(weight), item_type=item_type)
        items.append(item)
    total_price = Item.calculate_total_price(items)
    payment_method = Vald.read_in_value(
        validation_function=Vald.validate_payment_method,
        message="Enter the payment method (Net, Debit or Credit): ")
    payment_status = "Unpaid"
    card_number = None
    if payment_method.lower() != "net":
        card_number = Vald.read_in_value(
            validation_function=Vald.validate_card_number,
            message="Enter your card number (16 digits): ")
    payment_info = Payment(payment_method=payment_method,
    amount=total_price,
    payment_status=payment_status,
    card_number=card_number
    )
    payment_info.save_to_csv()
    today = datetime.now().date()
    while True:
        show_vehicle_options()
        total_weight = sum(item.weight for item in items)

        print(f"Your Order:\nWeight: {total_weight} kg\nItems: {len(items)}")
        vehicle_type = Vald.read_in_value(
            validation_function=Vald.validate_vehicle_type, 
            message="Choose a vehicle for the shipment ('B', 'T' or 'S'): ")
        
        order = Order(
        sender=sender,
        to_location=location,
        payment_details= payment_info.payment_method.upper(),
        items=items,
        total_weight=total_weight,
        order_status="Processing",
        order_place_datetime=today,
        order_delivery_datetime=None,
        vehicle_type=vehicle_type)
            
        available_vehicle = get_available_vehicle(order)
        print(available_vehicle)
        if available_vehicle is not None:
            return order.id
        else:
            continue
# Function to start the program with 3 vehicles of each category
def create_initial_vehicles():

    for _ in range(3):
        bike = Bike.create_new_bike("bike_db.csv")
        truck = Truck.create_new_truck("truck_db.csv")
        ship = Ship.create_new_ship("ship_db.csv")
# Function to create all the csv files
def create_all_csv_files():
    User.create_csv_file_if_not_exists()
    Customer.create_csv_file_if_not_exists()
    Payment.create_csv_file_card_info()
    Payment.create_csv_file_tran_info()
    Order.create_csv_file_if_not_exists()
"""
def run():
# Removes all the csv files before starting
    for file in ["bike_db.csv", "truck_db.csv",
                "ship_db.csv", "transaction_db.csv",
                "order_db.csv", "cardinfo_db.csv"]:
        if os.path.exists(file):
            os.remove(file)
# Creates new clean csv Files
    create_initial_vehicles()
    create_all_csv_files()
    while True:
        show_menu()
        choice = input("Choice: ")
        if choice == "1":
            user_login()
            continue
        elif choice == "2":
            create_user()
            continue
        elif choice == "3":
            create_customer()
            continue
        elif choice == "4":
            create_order()
            continue

run()
"""