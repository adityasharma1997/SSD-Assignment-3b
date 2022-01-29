from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager, login_manager, UserMixin
from werkzeug.wrappers import response
import csv

app = Flask(__name__)

username = "root"
password = "aditya1234"
server = "localhost:3306"
database = "bill"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{server}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'root'
app.config['SESSION_TYPE'] = "sqlalchemy"

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
sessn = Session(app)
login_manager = LoginManager()
login_manager.init_app(app)


# User db Model
class User(UserMixin, db.Model):
    """This class defines model used for User table in Database."""

    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type


class UserTransactions(db.Model):
    """This class defines table in Database which shows
     relation between username and transaction IDs.
     """
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)

    def __init(self, username):
        self.username = username


class TransactionItems(db.Model):
    """
    This class defines table in Database which shows relation between
     TransactionID and items ordered in that transaction.
     """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.Integer, nullable=False)
    item_no = db.Column(db.Integer, primary_key=True, nullable=False)
    item_type = db.Column(db.String(10), primary_key=True, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_total = db.Column(db.Float, nullable=False)

    def __init__(self, tid, item_no, item_type, item_quantity, item_total):
        self.tid = tid
        self.item_no = item_no
        self.item_type = item_type
        self.item_quantity = item_quantity
        self.item_total = item_total


class TrancationBill(db.Model):
    """
    This class defines table in Database which shows relation
     between TransactionID and final bill of that transaction.
     """
    tid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    bill_total = db.Column(db.Numeric(10, 2), nullable=False)
    bill_tip = db.Column(db.Integer, nullable=False)
    bill_discount = db.Column(db.Float, nullable=False)
    bill_final_total = db.Column(db.Float, nullable=False)
    bill_person = db.Column(db.Integer, nullable=False)

    def __init__(
            self,
            tid,
            bill_total,
            bill_tip,
            bill_discount,
            bill_final_total,
            bill_person):
        self.tid = tid
        self.bill_total = bill_total
        self.bill_tip = bill_tip
        self.bill_discount = bill_discount
        self.bill_final_total = bill_final_total
        self.bill_person = bill_person


class FoodMenu(db.Model):
    """
    This class defines table in Database which contains
     Menu which has ItemNo and their full and half plate prices.
    """
    item_no = db.Column(db.Integer, primary_key=True)
    half_price = db.Column(db.Float, nullable=False)
    full_price = db.Column(db.Float, nullable=False)

    def __init__(self, item_no, half_price, full_price):
        self.item_no = item_no
        self.half_price = half_price
        self.full_price = full_price


def insert_menu():
    """
    Function to insert intial Menu in Database from Menu.csv
    """

    menu = open("Menu.csv")
    menu_reader = csv.reader(menu)
    next(menu_reader)
    for item in menu_reader:
        item_record = FoodMenu(item[0], item[1], item[2])
        db.session.add(item_record)
    db.session.commit()


@app.route('/signup', methods=['POST'])
def signUp():
    """
    Function to process User SignUp request
    """
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']
    type = user_data['type']
    session_user = session.get(username)
    check_user = User.query.filter_by(username=username).first()
    if(check_user is not None):
        return "User already registered, please LogIn!!"
    elif session_user is not None:
        return "Logout inorder to register!!"
    else:
        user = User(username=username, password=password, type=type)
        db.session.add(user)
        db.session.commit()
        return "User Registered Successfully!!"


@app.route('/login', methods=['POST'])
def login():
    """
    Function to process User login request
    """
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']
    session_user = session.get('username')
    check_user = User.query.filter_by(username=username).first()
    if(check_user is not None):
        if (session_user is not None) and (session_user == username):
            return "Already Logged In!!"
        if session_user is not None and session_user != username:
            return "User LoggedIn with username " + session_user + \
                ".\nLogout in order to use different account!!"
        elif(check_user.password == password):
            session['username'] = username
            return "Welcome " + username + ",you have loggedIn successfully!!"
        else:
            return "[ERROR] Incorrect Password!!"
    else:
        return "No such User exists"


@app.route('/logout')
def logout():
    """
    Function to process User logout request
    """
    sessn_user = session.get('username')
    if sessn_user is not None:
        session.pop('username', None)
        return "Logged out Successfuly!!"
    else:
        return "No User currently loggedIn !!"


@app.route('/getMenu', methods=['GET'])
def getMenu():
    """
    Return the Menu to be displaed to User
    """
    session_user = session.get('username')
    if session_user is None:
        return jsonify({"msg": -1})
    else:
        menu = FoodMenu.query.filter().all()
        menu_list = list()
        for item in menu:
            data = dict()
            data['item_no'] = item.item_no
            data['half_price'] = item.half_price
            data['full_price'] = item.full_price
            menu_list.append(data)

        response = jsonify({"list": menu_list, "msg": "1"})
        return response


@app.route('/storebill', methods=['POST'])
def store_bill():
    """
    Function to store current bill of User
    """

    session_user = session.get('username')
    response = request.get_json()
    item_detail = response['items']
    transaction = UserTransactions(username=session_user)
    db.session.add(transaction)
    db.session.commit()
    transaction_id = transaction.tid

    for item in item_detail:
        tid = transaction_id
        item_no = item['item_no']
        item_type = item['item_type']
        item_quantity = item['item_quantity']
        item_total = item['item_total']
        item_ordered = TransactionItems(
            tid, item_no, item_type, item_quantity, item_total)
        db.session.add(item_ordered)
    db.session.commit()

    bill_total = response['bill_total']
    bill_tip = response['bill_tip']
    bill_discount = response['bill_discount']
    bill_final_total = response['bill_final_total']
    bill_person = response['bill_person']

    bill_detail = TrancationBill(
        tid,
        bill_total,
        bill_tip,
        bill_discount,
        bill_final_total,
        bill_person)
    db.session.add(bill_detail)
    db.session.commit()
    response = {
        "tid": tid,
        "msg": "Order processed successfully!!"
    }

    return jsonify(response)


@app.route('/gettransactionids', methods=['GET'])
def get_transaction_id():
    """
    Function returns all the previous transaction IDs of client
    """

    sessn_user = session.get('username')
    if sessn_user is None:
        response = {"msg": "-1"}
        return jsonify(response)
    else:
        tid = UserTransactions.query.filter_by(username=sessn_user)
        if tid is None:
            response = {
                "trans_ids": [],
                "msg": "1"
            }
            return jsonify(response)
        else:
            tids = list()
            for i in tid:
                tids.append(i.tid)
            response = {
                "trans_ids": tids,
                "msg": "1"
            }
            return jsonify(response)


@app.route('/getbillbyid/<tid>', methods=['GET'])
def get_bill_by_tid(tid):
    """
    Returns the bill of the given transaction ID to client
        Parameters:
            tid : Transaction ID of Bill to display
    """
    sessn_user = session.get('username')
    tid_order = UserTransactions.query.filter_by(
        tid=tid, username=sessn_user).first()
    print(tid_order)
    if tid_order is not None:
        item_ordered = TransactionItems.query.filter_by(tid=tid)
        item_list = list()
        for item in item_ordered:
            data = {
                "item_no": item.item_no,
                "item_type": item.item_type,
                "item_qty": item.item_quantity,
                "item_price": item.item_total
            }
            item_list.append(data)
        bill_detail = TrancationBill.query.filter_by(tid=tid).first()
        print(bill_detail)
        bill_data = {
            "item": item_list,
            "bill_total": bill_detail.bill_total,
            "bill_tip": bill_detail.bill_tip,
            "bill_discount": bill_detail.bill_discount,
            "bill_final_total": bill_detail.bill_final_total,
            "bill_person": bill_detail.bill_person,
            "msg": "1"
        }
        return jsonify(bill_data)

    else:
        response = {"msg": "-1"}
        return jsonify(response)


@app.route('/additem', methods=['POST'])
def add_item():
    """
    Function to process add item request of client
    """
    sessn_user = session.get('username')
    if sessn_user is None:
        response = "[ERROR] You are not loggedIn. "
        response += "Please loginIn to process action!!"
        return response
    else:
        user = User.query.filter_by(username=sessn_user).first()
        if (user.type != "chef"):
            response = "[ERROR] Not Chef!! "
            response += "Only Chefs are allowed to add item in menu!!"
            return response
        else:
            response = request.get_json()
            item_no = response['item']
            check_item = FoodMenu.query.filter_by(item_no=item_no).first()
            if check_item is not None:
                return "[ERROR] ItemNo Already Present!!"
            half_price = response['half']
            full_price = response['full']
            menu_item = FoodMenu(
                item_no=item_no,
                half_price=half_price,
                full_price=full_price)
            db.session.add(menu_item)
            db.session.commit()
            return "Item Added Successfully!!"


if __name__ == '__main__':
    app.run(port=8000, debug=True)
