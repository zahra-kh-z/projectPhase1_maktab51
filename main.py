# =============================================================================
#       *****In the Name of God*****
#          zahra.kh2005@gmail.com
#       Author Name : Zahra khalifeh-zadeh
#         Code Name : Maktab51-python project-final Phase2
# =============================================================================
"""
*Note: in first_run you should registered an Admin by special password==1.
        this controlled if someone interacts with the program as an admin.
"""

import customer
import menu
import user
from user import User
import logging

logging.basicConfig(filename='my_file.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def main():
    """
    This method for ask from user to login/register/change_information.
    The user login first. If he does not have an account, create an account and if he has an account, login.
    and check if you want register Admin so get a message for handling this task.
    """
    menu.print_menu_register_login()
    username_list = menu.file_path_username_list()
    choice = 0
    while choice != "4":
        choice = input("Please enter your choice:")
        if choice == "1":
            username = input("Please enter your Username for register:\n")
            if username in username_list:
                if username == "admin":
                    print('You are not Admin. an admin is exist.')
                    main()
                else:
                    print(f"Username {username.capitalize()} is exist in system. please enter another username.")
                    main()
            else:
                password = input(f"{username.capitalize()} please enter your password for register:\n")
                if username == "admin" and password == '1':  # for secure admin entry
                    user.User.register(username, password)
                    main()
                elif username == "admin" and password != 1:
                    print('You are not Admin. an admin has special password.')
                    main()
                else:
                    user.User.register(username, password)
                    main()

        elif choice == "2":
            username = input('Please enter your name for login:')
            if username == 'admin':  # show log if admin enter and inventory == 0, for phase3
                user.User.login(username)
                logging.warning('Admin logged in')
                print("************ Welcome Admin ***************")
                menu.check_inventory()
                menu.main_admin()
            else:
                if username in username_list:
                    customer.Customer.show_product()
                    print('If you want to buy should enter password.')
                    user.User.login(username)
                    print(f"************ Welcome {username.capitalize()} ***************")
                    menu.main_customer(username)
                else:
                    print("Your not registered. please first register then login, or login with True username.")
                    main()

        elif choice == "3":
            User.change_password()
            main()

        elif choice == "4":
            print("\n******  Goodbye ******")
        else:
            print("Invalid choice. Please try again.")


main()
