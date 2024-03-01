""" Module to setup and create and DB and API for it"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # pip install -U Flask-SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

# To create SQLite flask app we need to follow these 3 steps: 

## step#1 : assign path for our storage file for SQLite db
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
## step#2 : establish and connect our flask app to this DB.
### Create Flask APP
app = Flask(__name__)
### Alter  flask app configurations to add hosting file for our Database(db)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(basedir,"datav2.sqlite")
### set False for Tracking modifications to save RAM storage under running time
app.config["SQLALCHEMY_TRACK_MODIFICATIONs"] = False
### Connect our  Flask APP to Database object called db
db = SQLAlchemy(app=app)

# Let's configure our database
################################################################
###### USER TABLE for school system ############################
###### System ACCOUNT TABLE for USERS ##########################
###### HISTORY for USERS msg.s TABLE ###########################
################################################################

# Create USER TABLE in SQLALCHMEY
class User(db.Model):
    ### SPECIAL about Table or Class in DB
    ### 1 - create table name
    __tablename__ = 'user_info'
    ### 2 - Table columns declarations 
    # more info https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    ###### Very important to start with id column as primary key and never forget it
    id = db.Column(db.Integer,primary_key = True)
    # user_name is column that carry in name of the user in data format string
    user_name = db.Column(db.String, nullable = False)
    # user_email is column that hold e-mail address and must be existed and be unique
    user_email = db.Column(db.String, nullable = False,unique = True)
    # user_is_student is column that hold True if user is student.
    user_is_student = db.Column(db.Boolean)
    # user_course is column that hold name of the course that study in this school
    user_course = db.Column(db.String)
    # user_hobbies is column that hold hobbies of the user.
    user_hobbies = db.Column(db.String)
    # user_birthdate is column that hold data of birth for the user and is must exist.
    user_birthdate = db.Column(db.DateTime,nullable = False)
    # user_about is column to have text about the user like special notes etc...
    user_about_u = db.Column(db.Text)
    # created_on is column that log date and time for this record initialization 
    created_on = db.Column(db.DateTime(timezone = True),server_default = func.now())

    ### relations
    ## ONE2ONE with SystemAccount
    system_account = db.relationship("SystemAccount", # Class name for another side of relation
                                     backref = 'User', # Class name for front side of relation
                                     uselist = False) # One2One relation
    
    ## Many2One with History
    history_list = db.relationship("History",
                                   backref = "User",
                                   lazy = 'dynamic')
    
    ### 3 - add Constructor and any other Normal Python Methods
    def __init__(self,user_name:str,
                    user_email:str,
                    user_is_student:bool,
                    user_course:str,
                    user_hobbies:str,
                    user_birthdate:str,
                    user_about_u:str,
                    ) -> None:
        self.user_name = user_name.title()
        self.user_email = user_email.lower()
        self.user_is_student = user_is_student
        self.user_course = user_course
        self.user_hobbies = user_hobbies
        self.user_birthdate = user_birthdate
        self.user_about_u = user_about_u
        self.created_on = datetime.datetime.now()
    
    def __str__(self) -> str:
        rep = f"User ID:        {self.id}\n"+\
              f"User name:      {self.user_name}\n"+\
              f"Birthdate:      {self.user_birthdate}\n"+\
              f"E-Post:         {self.user_email}\n"+\
              f"Student:        {self.user_is_student}\n"+\
              f"Course:         {self.user_course}\n"+\
              f"Hobbies:        {self.user_hobbies}\n"+\
              f"About User:     {self.user_about_u}\n"+\
              f"Created on:     {self.created_on}\n"
        if self.system_account:
            rep += " --> Related system account info : \n"
            rep += self.system_account.__str__()
            return rep
        else:
            return rep
    
    def user_history(self):
        if self.history_list:
            output=str()
            for msg in self.history_list:
                output += msg.__str__()
            return output
        else:
            return None


###### System ACCOUNT TABLE for USERS ##########################
class SystemAccount(db.Model):
    __tablename__ = "account_info"
    id = db.Column(db.Integer,primary_key = True)
    # acc_user_email : will hold the user e-mail address that will log in to the system with
    acc_user_email = db.Column(db.String,unique = True, nullable = False)
    # pwdhash will hold hashing of user password to come in into our school system 
    acc_pwdhash = db.Column(db.String,nullable = False)
    # acc_role will hold one of these values [admin , student, teacher]
    acc_role = db.Column(db.String(10), nullable = False)
    # acc_status will hold on of these values [active(default) , inactive , suspended]
    acc_status = db.Column(db.String(15))
    # acc_created_on : will hold the date and time of record initialization.
    acc_created_on = db.Column(db.DateTime(timezone = True), server_default = func.now())
    # ONE2ONE Relation with USER Table
    user_id = db.Column(db.Integer, ## Must have same data type
                        db.ForeignKey('user_info.id')) # must use table name not class name
    
    def __init__(self,acc_user_email:str,
                 password:str,
                 acc_role:str,
                 user_id:int,
                 acc_status:str = "active",
                 ) -> None:
        self.acc_user_email = acc_user_email.lower()
        self.acc_pwdhash = generate_password_hash(password=password)
        # we can add python validation to be in [admin , student, teacher]
        self.acc_role = acc_role
        self.user_id = user_id
        self.acc_status = acc_status
        self.acc_created_on = datetime.datetime.now()
    
    def __str__(self) -> str:
        return f"Account Username:      {self.acc_user_email}\n"+\
               f"Account Role:          {self.acc_role}\n"+\
               f"Account_status:        {self.acc_status}\n"+\
               f"Account Created on:    {self.acc_created_on}\n"+\
               f"Account Owner ID:      {self.user_id}\n"
    
    def hash_password(self,password:str)->None:
        """ Method to hash password once needed and rec. to not return hashing"""
        self.acc_pwdhash = generate_password_hash(password=password)
        #return self.acc_pwdhash

    def check_hashed_password(self,password:str)->bool:
        """Method to check matching of plain password against saved hashed password"""
        return check_password_hash(self.acc_pwdhash,password=password)

###### HISTORY for USERS msg.s TABLE ###########################
class History(db.Model):
    __tablename__ = "history_info"
    id = db.Column(db.Integer,primary_key = True)
    # txt will hold msg. text
    his_txt = db.Column(db.Text,nullable = False)
    # his_status will hold status value from [active(default),archived]
    his_status = db.Column(db.String(10))
    # his_created_on will hold record creation date and time
    his_created_on = db.Column(db.DateTime(timezone = True), server_default = func.now())
    # Many2One Relation with User
    user_id = db.Column(db.Integer,db.ForeignKey('user_info.id'))

    def __init__(self,his_txt:str,user_id:int,his_status:str = "active") -> None:
        self.his_txt = his_txt
        self.user_id = user_id
        self.his_status = his_status
        self.his_created_on = datetime.datetime.now()
    
    def __str__(self) -> str:
        return f" Text:         {self.his_txt}\n"+\
               f"Status:        {self.his_status}\n"+\
               f"Created On:    {self.his_created_on}\n"+\
               f"Owner ID       {self.user_id}\n"
    
    def archive_history(self):
        """Method to change status to archive with confirmation"""
        self.his_status = "archived"
        return True

##########################################################
###################### API ###############################
#index to show all users. 
@app.route('/')
def index():
    all_users = User.query.all()
    output= str()
    for user in all_users:
        output += str(user) .replace("\n", "<br>")
        output += "<br>"
        output += "<br>---------------------------------<br>"
    return f"<h1> {output} </h1>"

# get User info per ID.
@app.route('/user/<user_id>')
def get_user (user_id:int):
    target_user = db.session.get(User,user_id)
    if target_user:
        target_user = str(target_user).replace("\n", "<br>")
        return f"<h1> {target_user} </h1>"
    else:
        return f"<h1> No Such User found has user_id = {user_id} </h1>" 


# get User History per ID.
@app.route('/history/<user_id>')
def get_user_history(user_id):
    target_user = db.session.get(User,user_id)
    if target_user:
        output = target_user.user_history().replace("\n","<br/>")
        return f"<h1> {output} </h1>"
    else:
        return f"<h1> No Such User found has user_id = {user_id} </h1>"

## step#3 : create database and run our app(app mean API).
if __name__ == '__main__':
    ### Push changes over different python scripts to keep data up and running 
    app.app_context().push()
    ### Create all table into my data file as Database
    app.run()


