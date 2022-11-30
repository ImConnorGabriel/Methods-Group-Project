from classes import User
from classes import Cart
from classes import Inventory
from classes import TV
from classes import Laptop
import mysql.connector

mydb = mysql.connector.connect(
    host = "34.134.183.154",
    user = "root",
    password = "group16",
    database = "ElectronicStore"
)

mycursor = mydb.cursor(buffered = True)
mycursor2 = mydb.cursor(buffered = True)


def createNewUser(name):

    mycursor.execute("SELECT Username FROM Users;")

    for i in mycursor:
        if name == i[0]:
            return False

    password = input("Enter the password for your new account: ")
    address = input("Enter the address for your new account: ")
    cardNumber = input("Enter the card number for your new account: ")
    cardExp = input("Enter the card expiration date for your new account: ")
    cardPin = input("Enter the card security pin for your new account: ")
    cardZip = input("Enter the card zip code for your new account: ")

    user = User(name, password, address, cardNumber, cardExp, cardPin, cardZip)

    mycursor.execute("INSERT INTO Users (Username, Password, ShippingInfo, CardNumber, CardExp, CardPin, CardZip) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(user.username, user.password, user.shippingInfo, user.card_number, user.card_exp, user.card_sec_pin, user.card_zip))
    mydb.commit()
    return True


def login(username, password):

    mycursor.execute("SELECT Username, Password FROM Users WHERE Username = '{}' AND Password = '{}';".format(username, password))

    for i in mycursor:
        if i[0] == username and i[1] == password:
            return True

    return False


def viewInventory(itemType):
    laptopList = []
    TVList = []

    counter = 1

    if itemType == "laptop":
        mycursor.execute("SELECT * FROM Laptops;")
        print("Laptops available:")
        for i in mycursor:
            print("{}: ${} {} {} laptop ({} left).".format(counter, i[3], i[2], i[1], i[4]))
            counter += 1
            laptop = Laptop(i[0], i[2], i[1], i[3], i[4])
            newLaptop = Inventory(laptop.id, "laptop", laptop.size, laptop.pictureQuality, laptop.price, laptop.quantity)
            laptopList.append(newLaptop)
        return laptopList
    if itemType == "TV":
        mycursor.execute("SELECT * FROM TVs;")
        print("TVs available:")
        for i in mycursor:
            print("{}: ${} {} {} TV ({} left).".format(counter, i[3], i[2], i[1], i[4]))
            counter += 1
            TV1 = TV(i[0], i[2], i[1], i[3], i[4])
            newTV = Inventory(TV1.id, "TV", TV1.size, TV1.pictureQuality, TV1.price, TV1.quantity)
            TVList.append(newTV)
        return TVList


def viewCart(username):

    itemList = []
    mycursor.execute("SELECT * FROM Cart WHERE Username = '{}';".format(username))
    counter = 1
    print("Your Cart:")
    for i in mycursor:
        if i[1] == "laptop":
            mycursor2.execute("SELECT * FROM Laptops WHERE ItemID = '{}';".format(i[2]))
            for j in mycursor2:
                print("{}: ${} {} {} {}.".format(counter, i[3], j[2], j[1], i[1]))

        if i[1] == "TV":
            mycursor2.execute("SELECT * FROM TVs WHERE ItemID = '{}';".format(i[2]))
            for j in mycursor2:
                print("{}: ${} {} {} {}.".format(counter, i[3], j[2], j[1], i[1]))

        counter += 1
        cartitem = Cart(i[2], username, i[1], j[2], j[1], i[3])
        itemList.append(cartitem)

    return itemList

def OrderHistory(username):

    print()
    mycursor.execute("SELECT * FROM OrderHistory WHERE Username = '{}';".format(username))
    z = 0
    print("Order History:")
    for i in mycursor:
        print("{}: ${} {} {}".format(z, i[3], i[2], i[1][:-1]))
        z += 1

    print()

def addToCart(cart):

    mycursor.execute("INSERT INTO Cart (Username, itemType, itemID, Price) VALUES ('{}', '{}', '{}', '{}');".format(cart.username, cart.itemType, cart.id, cart.price))
    if cart.itemType == "laptop":
        mycursor.execute("UPDATE Laptops SET quantity = quantity - 1 WHERE itemID = '{}';".format(cart.id))
    if cart.itemType == "TV":
        mycursor.execute("UPDATE TVs SET quantity = quantity - 1 WHERE itemID = '{}';".format(cart.id))
    mydb.commit()


def remove(cart):
    mycursor.execute("DELETE FROM Cart WHERE ItemID = '{}' and Username = '{}';".format(cart.id, cart.username))
    if cart.itemType == "laptop":
        mycursor.execute("UPDATE Laptops SET quantity = quantity + 1 WHERE itemID = '{}';".format(cart.id))
    if cart.itemType == "TV":
        mycursor.execute("UPDATE TVs SET quantity = quantity + 1 WHERE itemID = '{}';".format(cart.id))
    mydb.commit()


def checkoutCart(username):

    mycursor.execute("SELECT * FROM Cart WHERE Username = '{}';".format(username))

    for i in mycursor:
        mycursor2.execute("INSERT INTO OrderHistory (Username, ItemID, ItemType, Price) VALUES ('{}', '{}', '{}', '{}');".format(i[0], i[2], i[1], i[3]))
        mydb.commit()

    mycursor.execute("DELETE FROM Cart WHERE Username = '{}';".format(username))
    mydb.commit()


def deleteAccount(username):
    mycursor.execute("DELETE FROM Cart WHERE Username = '{}';".format(username))
    mycursor.execute("DELETE FROM OrderHistory WHERE Username = '{}';".format(username))
    mycursor.execute(("DELETE FROM Users WHERE Username = '{}';".format(username)))
    mydb.commit()

loggedIn = False

while True:
    #this is the menuing before the user is logged in
    userChoice = int(input("MENU:\n1: Login.\n2: Create an account.\n3. Exit.\n> "))

    if userChoice == 1:
        username = input("\nUsername: ")
        password = input("Password: ")
        if login(username, password):
            print("\nSuccessfully logged in as {}\n".format(username))
            validUser = True
        else:
            print("\nIncorrect login information. Try again.\n")

    if userChoice == 2:
        username = input("Username: ")

        if createNewUser(username):
            print("\nUser created.\n")
        else:
            print("\nUsername is taken.\n")

    if userChoice == 3:
        print("Thank you for shopping with us.")
        break

    #this is the menuing after the user is logged in
    while validUser:
        userChoice = int(input("MENU:\n1: View TVs.\n2: View laptops.\n3: View cart.\n4: View account options.\n5: Logout.\n> "))

        if userChoice == 1:
            print()
            TVList = viewInventory("TV")
            itemChoice = int(input("\nEnter the number of a TV to add to cart. (0 to return to menu)\n>")) - 1
            if itemChoice == -1:
                print()
                continue
            else:
                newCart = Cart(TVList[itemChoice].id, username, "TV", TVList[itemChoice].size, TVList[itemChoice].quality, TVList[itemChoice].price)
                addToCart(newCart)
                print("\nItem added to cart.\n")

        if userChoice == 2:
            print()
            laptopList = viewInventory("laptop")
            itemChoice = int(input("\nEnter the number of a laptop to add to cart. (0 to return to menu)\n> ")) - 1
            if itemChoice == -1:
                print()
                continue
            else:
                newCart = Cart(laptopList[itemChoice].id, username, "laptop", laptopList[itemChoice].size, laptopList[itemChoice].quality, laptopList[itemChoice].price)
                addToCart(newCart)
                print("\nItem added to cart.\n")

        if userChoice == 3:
            print()
            cartList = viewCart(username)
            cartChoice = int(input("\nWould you like to:\n1: Remove an item. \n2. Checkout.\n3. Return to menu.\n> "))
            print()
            if cartChoice == 1:
                userInput = int(input("Enter the number of the item to remove: ")) - 1
                print("\nRemoved item from cart.\n")
                remove(cartList[userInput])
            if cartChoice == 2:
                checkoutCart(username)
                print("You have successfully checked out.\n")
            if cartChoice == 3:
                continue

        if userChoice == 4:
            accountChoice = int(input("\nWould you like to:\n1: Edit shipping info\n2: Edit payment info\n3: View order history\n4: Delete account\n> "))

            if accountChoice == 1:
                newAddress = input("\nEnter your new shipping address: ")
                print()
                mycursor.execute("UPDATE Users SET ShippingInfo = '{}' WHERE Username = '{}';".format(newAddress, username))
                mydb.commit()
                print("Your shipping info has been successfully changed.\n")
            if accountChoice == 2:
                cardnum = input("\nEnter your new card number: ")
                cardexp = input("Enter your new card expiration date: ")
                cardpin = input("Enter your new card security pin: ")
                cardzip = input("Enter your new card zip code: ")
                print()
                mycursor.execute("UPDATE Users SET CardNumber = '{}' and CardExp = '{}' and CardPin = '{}' and CardZip = '{}' WHERE Username = '{}';".format(cardnum, cardexp, cardpin, cardzip, username))
                mydb.commit()
                print("Your payment info has been successfully changed.\n")
            if accountChoice == 3:
                OrderHistory(username)
            if accountChoice == 4:
                deleteAccount(username)
                validUser = False
                print("\nAccount successfully deleted.\n")

        if userChoice == 5:
            validUser = False
            print("\nSuccessfully logged out.\n")