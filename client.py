import requests
import random

from requests.models import Response

sessn = requests.Session()


def choices():
    """Function to Display Choices Available to User"""

    print("1. SignUp ")
    print("2. Login ")
    print("3. Logout ")
    print("4. Display Menu")
    print("5. Order Item")
    print("6. Show Previous Trancations")
    print("7. Add new item in menu(Only Chef)")
    print("8. Exit")


def signup():
    """Helper Function for SignUp"""

    username = input("Enter username:")
    password = input("Enter password:")
    type = input("User Type: Customer(cust)/Chef(chef): ")
    data = {
        "username": username,
        "password": password,
        "type": type
    }
    response = sessn.post('http://localhost:8000/signup', json=data).content
    response = response.decode()
    print(response)
    return


def login():
    """Helper Function for LogIn"""

    username = input("Enter username:")
    password = input("Enter password:")

    data = {
        "username": username,
        "password": password
    }

    response = sessn.post('http://localhost:8000/login', json=data).content
    response = response.decode()
    print(response)
    return


def logout():
    """Helper Function for Logout"""

    response = sessn.get('http://localhost:8000/logout').content
    response = response.decode()
    print(response)
    return


def display_menu(response):
    """
    Function to Display Menu to User
        Parameters :
            Response['list']
        Return:
            Dictionary with item id as key and half
            and full price of item id as its value
    """
    header = ["ItemNo", "Half", "Full"]
    for k in header:
        print(f"{k:<15}", end='  ')
    print()
    # dict_item_temp
    dict_item = dict()
    for item in response:

        itemNo = item['item_no']
        half_price = item['half_price']
        full_price = item['full_price']
        # temp
        if(half_price.is_integer()):
            half_price = int(half_price)
        if(full_price.is_integer()):
            full_price = int(full_price)
        dict_item[int(itemNo)] = {'half': float(
            half_price), 'full': float(full_price)}
        print(
            f"{itemNo:^9}" +
            "      " +
            f"{half_price:^10}" +
            "      " +
            f"{full_price:^11}")
    print()
    return dict_item


def calculateTotal(dict, tip):
    """
    Calculates Total Cost of Ordered Items + tip given
        Parameters:
            dict: Dictionary having ordered item number and plate type
            tip : Tip Percentage
        Return:
            Total Cost
    """

    total = 0
    j = 1
    for i in dict:
        total = total + dict[i]['half'] + dict[i]['full']
        j += 1
    tip_given = (tip * total) / 100
    print("Bill")
    print("Item Cost: {:.2f}".format(total))
    print("Tip: {:.2f}".format(tip_given))
    print("Total Cost: {:.2f}".format(total + tip_given))
    return total + tip_given


def lucky_draw():
    """Function for luck draw which selects
    decrease/increase applicable on total bill
    as per given criterion."""

    sample_list = [-50, -25, -10, 0, 20]
    random_list = random.choices(sample_list, weights=(5, 10, 15, 20, 50), k=1)
    return random_list[0]


def pattern1():
    """Function for printing pattern on discount."""

    print(" ****             **** ")
    print("|    |           |    |")
    print("|    |           |    |")
    print("|    |           |    |")
    print(" ****             **** ")
    print()
    print("          {}           ")
    print("    ______________     ")


def pattern2():
    """Function for printing pattern on zero/increase in value."""

    print(" **** ")
    print("*    *")
    print("*    *")
    print("*    *")
    print("*    *")
    print(" **** ")


def processOrder(dictItemList):
    """
    Function to process Bill for the items ordered by User.
    Also displays the final bill transcript
        Parameters:
            dictItemList : Dictionary having Menu of Hotel
    """
    dict_order = {}
    for i in dictItemList:
        dict_order[i] = {'half': 0, 'full': 0}
    print("No. of Items to order")
    n = int(input())
    orderList = []
    print("Enter Order in following format:")
    print("ItemNo Full/Half Quantity (Space Separated)")
    for i in range(n):
        inputs = list(map(str, input().split()))
        itemId = int(inputs[0])
        itemType = inputs[1]
        quantityItem = int(inputs[2])
        if itemType.lower() == 'half':
            dict_order[itemId][itemType.lower(
            )] += (float(dictItemList[itemId]['half']) * quantityItem)
        else:
            dict_order[itemId][itemType.lower(
            )] += (float(dictItemList[itemId]['full']) * quantityItem)
        orderList.append([itemId, itemType, quantityItem])

    print("Please choose from tip options: 0%,10%,20%")
    tip = int(input())
    print()
    totalCost = calculateTotal(dict_order, tip)
    print("No. of people you want to split bill")
    no_of_person = int(input())
    print(
        "Per Person Cost(Split Bill): {:.2f} ".format(
            totalCost /
            no_of_person))
    print()
    print("Restaurant has a limited time event called Test Your Luck")
    print("Would you like to participate in Test Your Luck-Yes or No")
    userPref = input()

    discWon = 0
    if userPref.lower() == "yes":
        discWon = lucky_draw()
        discWon = (totalCost * discWon) / 100
        if(discWon < 0):
            print("Congratulations!! You won a discount",
                  "of value: {:.2f}\n".format(discWon))
            pattern1()
        elif discWon == 0:
            print(
                "Sorry!!, You received a discount of value: {:.2f}\n"
                .format(discWon))
            pattern2()
        else:
            print(
                "Sorry!! Your bill got increased by value: {:.2f}\n"
                .format(discWon))
            pattern2()

    j = 1
    bill_total = 0
    halfQuantity = 0
    fullQuantity = 0
    item_ordered = list()

    print("--------------------------------------------")
    for i in dict_order:
        halfQuantity = 0
        fullQuantity = 0
        if (dict_order[i]['half'] > 0) or (dict_order[i]['full'] > 0):
            if dict_order[i]['half'] > 0:
                bill_total = bill_total + dict_order[i]['half']
                halfQuantity = int(
                    dict_order[i]['half'] / (dictItemList[i]['half']))
                item_to_add = {
                    "item_no": i,
                    "item_type": "Half",
                    "item_quantity": int(halfQuantity),
                    "item_total": float(dict_order[i]['half'])
                }
                print("Item " +
                      str(i) +
                      "[Half]" +
                      "[" +
                      str(int(halfQuantity)) +
                      "]:  ", str(dict_order[i]['half']))
                item_ordered.append(item_to_add)

            elif dict_order[i]['full'] > 0:
                bill_total = bill_total + dict_order[i]['full']
                fullQuantity = int(
                    dict_order[i]['full'] / (dictItemList[i]['full']))
                item_to_add = {
                    "item_no": i,
                    "item_type": "Full",
                    "item_quantity": int(fullQuantity),
                    "item_total": float(dict_order[i]['full'])
                }
                print("Item " +
                      str(i) +
                      "[Full]" +
                      "[" +
                      str(int(fullQuantity)) +
                      "]:  ", str(dict_order[i]['full']))
                item_ordered.append(item_to_add)
            j += 1

    print("Total: {:.2f}".format(bill_total))
    print("Tip Percentage: {}%".format(tip))
    bill_total += ((bill_total * tip) / 100)
    print("Discount/Increase: {:.2f}".format(discWon))
    bill_totalAfterDisc = bill_total + discWon
    print("Final Total: {:.2f} ".format(bill_totalAfterDisc))
    print(
        "Updated Shared/Per Person cost: {:.2f}"
        .format(bill_totalAfterDisc / no_of_person))

    final_bill = {
        "items": item_ordered,
        "bill_total": bill_total,
        "bill_tip": tip,
        "bill_discount": discWon,
        "bill_final_total": bill_totalAfterDisc,
        "bill_person": float(bill_totalAfterDisc / no_of_person)
    }

    response = sessn.post(
        'http://localhost:8000/storebill',
        json=final_bill).json()
    print("--------------------------------------------")
    print(response['msg'])
    print("Trancation ID of Order: ", response['tid'])


def order_food():
    """
    Helper Function to take Order of User
    """
    response = sessn.get('http://localhost:8000/getMenu').json()
    # response = response.decode()
    if(response['msg'] == -1):
        print("[ERROR] User Not Logged In!!")
        return

    dictItemList = display_menu(response['list'])
    processOrder(dictItemList)


def previous_transaction():
    """
    Function to Display Bill of previour transactions of User.
    """
    response = sessn.get('http://localhost:8000/gettransactionids').json()
    status = response['msg']
    if(status == "1"):
        transaction_ids = response['trans_ids']
        if len(transaction_ids) == 0:
            print("No previous transaction found!!")
            return
        else:
            print("Previous Orders Transcation IDs: ")
            for tid in transaction_ids:
                print(tid)
            print("Enter the Transaction ID for the bill: ")
            trans_id = input()
            url = 'http://localhost:8000/getbillbyid/' + trans_id
            response = sessn.get(url).json()
            if(response['msg'] == "-1"):
                print(
                    "[Error] TransactionID entered doesn't match ",
                    "any of the previous Transaction ID!!")
            # Display Bill
            else:
                items = response['item']
                print("--------------------------------------------")
                print("|                 Bill Detail              |")
                print("--------------------------------------------")
                for item in items:
                    print("Item " +
                          str(item['item_no']) + " [" +
                          item['item_type'] + "]" +
                          "[" +
                          str(item['item_qty']) +
                          "]:  {:.2f}".format(float(item['item_price'])))

                print("Total: {:.2f}".format(float(response['bill_total'])))
                print(
                    "Tip Percentage: {}%".format(
                        float(
                            response['bill_tip'])))
                # bill_total += ((bill_total * tip) / 100)
                print(
                    "Discount/Increase: {:.2f}"
                    .format(float(response['bill_discount'])))
                # bill_totalAfterDisc = bill_total + discWon
                print(
                    "Final Total: {:.2f} ".format(
                        float(
                            response['bill_final_total'])))
                print(
                    "Updated Shared/Per Person cost: {:.2f}"
                    .format(float(response['bill_person'])))
                print("--------------------------------------------")

    elif(status == "-1"):
        print("[ERROR] You are not loggedIn. Please login to process action!!")

        return


def add_new_item():
    """
    Function to add new item to Menu
    """
    item_no = input("Enter the ID of Item: ")
    half_price = input("Enter the Half plate price of Item: ")
    full_price = input("Enter the Full plate price of Item: ")
    data = {
        "item": item_no,
        "half": half_price,
        "full": full_price
    }
    response = sessn.post('http://localhost:8000/additem', json=data).content
    response = response.decode()
    print(response)
    return


if __name__ == "__main__":
    flag = True
    while(flag):
        choices()
        print("Enter Choice: ")
        inp = input()

        if inp == str(1):
            signup()

        elif inp == str(2):
            login()

        elif inp == str(3):
            logout()

        elif inp == str(4):
            response = sessn.get('http://localhost:8000/getMenu').json()
            # response = response.decode()
            if(response['msg'] == -1):
                print("[ERROR] User Not Logged In!!")
            else:
                display_menu(response['list'])

        elif inp == str(5):
            order_food()

        elif inp == str(6):
            previous_transaction()

        elif inp == str(7):
            add_new_item()

        elif inp == str(8):
            print("Thank You for using our services")
            flag = False

        else:
            print("[ERROR] Invalid Command!!")
        print()
