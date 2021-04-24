from admin import Admin
from customer import Customer


def print_menu_admin():
    print("******************************************")
    print("""what do you do?\t
    1: Add a product\t
    2: Show product list\t
    3: update inventory\t
    4: view invoices\t
    5: Quit\t""")


def main_admin():
    print_menu_admin()
    choice = 0
    while choice != "5":
        choice = input("Please enter your choice:")
        if choice == "1":
            Admin.creat_product()
            print_menu_admin()
        elif choice == "2":
            Admin.show_product_list()
            print_menu_admin()
        elif choice == "3":
            Admin.update_inventory()
            print_menu_admin()
        elif choice == "4":
            Admin.view_invoices()
            print_menu_admin()
        elif choice == "5":
            print("\n******  Goodbye ******")
        else:
            print("Invalid choice. Please try again.")


def print_menu_customer():
    print("******************************************")
    print("""what do you do?\t
    1: buy a product\t
    2: Show all product (product_name, barcode, price)\t
    3: show my factor\t
    5: Quit\t""")


def main_customer():
    print_menu_customer()
    choice = 0
    while choice != "5":
        choice = input("Please enter your choice:")
        if choice == "1":
            Customer.buy_product()
            print_menu_customer()
        elif choice == "2":
            Customer.show_product_list()
            print_menu_customer()
        elif choice == "3":
            Customer.invoice()
            print_menu_customer()
        elif choice == "5":
            print("\n******  Goodbye  ******")
        else:
            print("Invalid choice. Please try again.")
