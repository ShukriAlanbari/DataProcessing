""" We shall create an API using Flask library"""

from flask import Flask

# To create a Flask APP, you do 2 steps
## Step 1 is to create flask server in app object
## and connect it to your .py file

## Step 2 is to run this object.

## Step 1:
app = Flask(__name__)

@app.route("/info")
def info():
    
    return "<h1 style='color: red; font-size: 24px; text-align: center; padding: 20px;'>Using an API in Flask enables efficient,\
        scalable and flexible data exchange between your application and others,\
        fostering integration and automation possibilities.</h1>"



@app.route("/operations/<int:a>/<int:b>")
def operations(a, b):
    add= a+b
    subtract= a-b
    multiply= a*b
    divide = "Infinity" if b == 0 else a / b
    return (f"<h1> Sum: {add} </h1><br>"
                f"<h1> Subtract: {subtract} </h1><br>"
                f"<h1> Multiply: {multiply} </h1><br>"
                f"<h1> Divide: {divide} </h1>")



    











if __name__ == "__main__":
    ## Step 2
    app.run()