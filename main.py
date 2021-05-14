# =============================================================================
#       *****In the Name of God*****
#          zahra.kh2005@gmail.com
#       Author Name : Zahra khalifeh-zadeh
#         Code Name : Maktab51-python project-final Phase3
# =============================================================================
"""
*Note: in first_run you should registered an Admin by special password==1.
        this controlled if someone interacts with the program as an admin.
"""

import menu
import user
from user import User
import my_log
import product
import sys


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
            if not username:  # check that username is not empty
                main()  # break loop if is empty
            if username in username_list:
                if username == "admin":
                    print('You are not Admin. an admin is exist.')
                    my_log.logger.warning('Someone tried to register as admin.')
                    main()
                else:
                    print(f"Username {username.capitalize()} is exist in system. please enter another username.")
                    main()
            else:
                password = input(f"{username.capitalize()} please enter your password for register:\n")
                if username == "admin" and password == '1':  # for secure admin entry
                    user.User.register(username, password)  # Only one admin is allowed to register and login.
                    my_log.logger.info('Admin created successfully.')
                    main()
                elif username == "admin" and password != 1:
                    print('You are not Admin. an admin has special password.')
                    my_log.logger.warning('Someone tried to register as an admin with an insecure password.')
                    main()
                else:
                    user.User.register(username, password)
                    main()

        elif choice == "2":
            username = input('Please enter your name for login:')
            if not username:  # check that username is not empty
                main()  # break loop if is empty
            if username == 'admin':
                user.User.login(username)
            else:
                if username in username_list:
                    table = product.Product.show_product(username)
                    print(table.table)
                    print('If you want to buy should enter password.')
                    user.User.login(username)
                else:
                    print("Your not registered. please first register then login, or login with True username.")
                    main()

        elif choice == "3":
            username = input("Please enter your Username for change_password:")
            if not username:  # check that username is not empty
                main()  # break loop if is empty
            current_password = input("Enter Current password: ")
            new_password = input("Enter New password: ")
            confirm_password = input("Enter New password confirmation: ")
            User.change_password(username, current_password, new_password, confirm_password)
            main()

        elif choice == "4":
            print("\n******  Goodbye ******")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


main()
