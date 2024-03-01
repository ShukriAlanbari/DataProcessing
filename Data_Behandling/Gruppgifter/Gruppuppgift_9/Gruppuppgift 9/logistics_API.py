from flask import Flask
from vehicles import Bike as B, Truck as T, Ship as S
import pandas as pd
import main

app = Flask(__name__)

########################### API ##################################
#Home
@app.route('/')
def home():
    return '<h1> Logisticssystem </h1>'

#Create user
@app.route("/create_user")
def create_user_api():
    main.create_user()
    user_df = pd.read_csv('user_db.csv')
    user_data = user_df.iloc[-1].to_dict()
    html = """
    <html>
    <head>
        <title>New User Created</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .user-info {
                background-color: #f2f2f2;
                width: 50%;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .user-info h2 {
                color: #333;
            }
            .user-info p {
                color: #666;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="user-info">
            <h2>New User Details</h2>
    """
    for key, value in user_data.items():
        html += f"<p><strong>{key}:</strong> {value}</p>"
    html += """
        </div>
    </body>
    </html>
    """
    return html

#remove user
@app.route("/remove_user")
def remove_user_api():
    user_id = main.remove_user()

    html = """
    <html>
    <head>
        <title>User Removed</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #eef;
            }}
            .removal-message {{
                background-color: #fee;
                color: #a00;
                width: 50%;
                margin: 20px auto;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .removal-message h2 {{
                margin: 0 0 10px 0;
            }}
            .removal-message p {{
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="removal-message">
            <h2>User Removal Confirmation</h2>
            <p>User ID: <strong>{user_id}</strong> has been removed.</p>
        </div>
    </body>
    </html>
    """

    return html.format(user_id=user_id)


#Update user
@app.route("/update_user")
def update_user_api():
   update_info = main.update_user()
   return f"Users info has been updated to {update_info}"

#Create customer
@app.route("/create_customer")
def create_customer_api():
    main.create_customer()
    customer_df = pd.read_csv('customer_db.csv')
    customer_data = customer_df.iloc[-1].to_dict()

    html = """
    <html>
    <head>
        <title>New Customer Created</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .customer-info {
                background-color: #f2f2f2;
                width: 50%;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .customer-info h2 {
                color: #333;
            }
            .customer-info p {
                color: #666;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="customer-info">
            <h2>New Customer Details</h2>
    """

    for key, value in customer_data.items():
        html += f"<p><strong>{key}:</strong> {value}</p>"

    html += """
        </div>
    </body>
    </html>
    """
    return html

#Remove customer
@app.route("/remove_customer")
def remove_customer_api():
    customer_id = main.remove_customer()

    html = """
    <html>
    <head>
        <title>Customer Removed</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #eef;
            }}
            .removal-message {{
                background-color: #fee;
                color: #a00;
                width: 50%;
                margin: 20px auto;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .removal-message h2 {{
                margin: 0 0 10px 0;
            }}
            .removal-message p {{
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="removal-message">
            <h2>Customer Removal Confirmation</h2>
            <p>Customer ID: <strong>{customer_id}</strong> has been removed.</p>
        </div>
    </body>
    </html>
    """

    return html.format(customer_id=customer_id)

#Update customer
@app.route("/update_customer")
def update_customer_api():
   update_info = main.update_customer()
   return f"Customers info has been updated to {update_info}"

#Add bike
@app.route("/add_bike")
def add_bike_api():
    B.create_new_bike()
    bike_df = pd.read_csv('bike_db.csv')
    return bike_df.iloc[-1].to_dict()

#Add truck
@app.route("/add_truck")
def add_truck_api():
    T.create_new_truck()
    truck_df = pd.read_csv('truck_db.csv')
    return truck_df.iloc[-1].to_dict()

#Add ship
@app.route("/add_ship")
def add_ship_api():
    S.create_new_ship()
    ship_df = pd.read_csv('ship_db.csv')
    return ship_df.iloc[-1].to_dict()

# #Create shipment/order of items.
@app.route("/order")
def create_order_api():
    order_id = main.create_order()
    #
    #return f"Order with id {order_id} has been added!"
    html = """
        <html>
        <head>
            <title>Order Created</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #eef;
                }}
                .removal-message {{
                    background-color: #fee;
                    color: #333;
                    width: 50%;
                    margin: 20px auto;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .removal-message h2 {{
                    margin: 0 0 10px 0;
                }}
                .removal-message p {{
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="removal-message">
                <h2>Order Created Confirmation</h2>
                <p>Order ID: <strong>{order_id}</strong> is prossecsing.</p>
            </div>
        </body>
        </html>
        """

    return html.format(order_id=order_id)
    
#Update status of order
@app.route("/update_order")
def update_order_status_api():
    order_id = main.update_delivery_status()
    order_df = pd.read_csv('order_db.csv', encoding="ISO-8859-1")
    order_info =\
        order_df.loc[order_df['order_id'] == order_id].iloc[0].to_dict()
    
    html = """
    <html>
    <head>
        <title>Order Information</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .order-info {
                background-color: #f2f2f2;
                width: 50%;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .order-info h2 {
                color: #333;
            }
            .order-info p {
                color: #666;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="order-info">
            <h2>Order Information</h2>
"""

    for key, value in order_info.items():
        html += f"<p><strong>{key}:</strong> {value}</p>"

    html += """
            </div>
        </body>
        </html>
    """

    return html

##################################################################

if __name__ == '__main__':
    app.run()