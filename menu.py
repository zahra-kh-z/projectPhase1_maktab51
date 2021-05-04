import csv
import sys
import pandas as pd
from admin import Admin
from customer import Customer
from product import Product


def print_menu_register_login():
    print("******************************************")
    print("""What do you do?\t
    1: Register\t
    2: Login\t
    3: Change password\t
    4: Quit\t""")


def file_path_username_list():
    file_path = "user_information.csv"
    df_user_info = pd.read_csv(file_path)
    username_list = list(df_user_info['username'])  # cascade ---> Append username to user_list
    # print(username_list)
    return username_list


def print_menu_admin():
    print("******************************************")
    print("""What do you do?\t
    1: Add a product\t
    2: Show product list\t
    3: Update inventory (Recharge store inventory)\t
    4: View invoices\t
    5: Quit\t""")


def main_admin():
    print_menu_admin()
    choice = 0
    while choice != "5":
        choice = input("Please enter your choice:")
        if choice == "1":
            Admin.add_product()
            print_menu_admin()
        elif choice == "2":
            Product.show_product()
            print_menu_admin()
        elif choice == "3":
            Product.show_product()
            Admin.add_update_inventory()
            Product.show_product()
            print_menu_admin()
        elif choice == "4":
            Admin.view_invoices()
            print_menu_admin()
        elif choice == "5":
            print("\n******  Goodbye ******")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


def print_menu_customer():
    print("******************************************")
    print("""What do you do?\t
    1: Buy a product\t
    2: Show all product (product_name, brand, price)\t
    3: Show my invoices\t
    4: Quit\t""")


def main_customer(username):
    print_menu_customer()
    choice = 0
    while choice != "4":
        choice = input("Please enter your choice:")
        if choice == "1":
            Customer.buy_product(username)
            print_menu_customer()
        elif choice == "2":
            Customer.show_product()
            print_menu_customer()
        elif choice == "3":
            Customer.invoice(username)
            print_menu_customer()
        elif choice == "4":
            print("\n******  Goodbye  ******")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


def check_inventory():
    with open('product_list.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row['inventory_number']) == 0:
                print(f'Warning inventory is zero: product_id:{row["product_id"]} product_name:{row["product_name"]}')


def check_inventory():
    with open('product_list.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row['inventory_number']) == 0:
                print(f'Warning inventory is zero: product_id:{row["product_id"]} product_name:{row["product_name"]}')
