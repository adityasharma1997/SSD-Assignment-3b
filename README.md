
# Assignment_3B

## Prerequisites
#### Followinfg modules should be installed before running python files
* pip install Flask
* pip install Flask-Session
* pip install Flask-SQLAlchemy
* pip install requests

## Steps to run:
It contains following files:
* server.py
Command to run: 
``` python server.py ```

* client.py
Command to run: 
``` python client.py ```

## Working:
* app.py will run a server on http://localhost:8000
* client.py have cli interface to interact with sever.
* Following choices are available to User:
    ```
    1. SignUp
        Which has two category of users : Chef and Customers
    2. Login
    3. Logout
    4. Display Menu
    5. Order Item
    6. Show Previous Trancations
    7. Add new item in menu(Only Chef)
    8. Exit

    ```
#### SignUp
* During signup user will be asked for username(should be unique), password, and user category (chef or customer)	

#### For Order Food
*  User will be asked to give total number of items he/she want to order. (Input should be an integer)
*  Then User should give the order in the following format
    ItemNo. Full/Half (Not case sensitive) Quantity
    Ex: 1 Full 2
*  User will be giving option to choose the tip out of (0%/10%/20%). To select any of above type that number without % sign
    Ex: For 0% type 0, for 10% type 10 and for 20% type 20.
*  User will be asked in how many people bill will be splitted.(Input should be an integer).
*  User will be given a choice if he/she want to play the on going Test Your Luck contest by entering Yes or No.
* Final Bill will be printed and stored in database for future reference.

#### Note: Non logged in users can only be able to access signup and login routes. Customers will be unable to access the route for modifying the menu.

### Chef User:
* Usename : admin Password: admin