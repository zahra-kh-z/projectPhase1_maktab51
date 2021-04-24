# =============================================================================
#       *****In the Name of God*****
#          zahra.kh2005@gmail.com
#       Author Name : Zahra khalifeh-zadeh
#         Code Name : Maktab51-python project-final Phase1
# =============================================================================
"""
This code suggest by Zahra for Phase1 Store-accounting project.
*Note: you first should creat user_list.txt and user_file.txt then run main. or use my ready files.
*Note: in first_run you should registered an Admin by special password==1.
        this controlled if someone interacts with the program as an admin.
Note: in Phase1 all function just print a message from class function.
"""
import user
import customer
import menu


def main():
    """
    This method for ask from user to login_or_register.
    The user login first. If he does not have an account, create an account and if he has an account, login.
    and check if you want register Admin so get a message for handling this task.
    """
    print('If you have an account, login and if you do not have one, create an account with a registry.')
    login_or_register = input('Now do you want to login or register? [login=L/register=R]')

    if login_or_register == "R":
        username = input("Please enter your Username for register:\n")
        password = input(f"{username} please enter your password for register:\n")
        if username in user.User.get_user_list():
            if username == "admin":
                print('You are not Admin. an admin is exist.')
                main()
            else:
                print(f"username {username} is exist in system. please enter another username.")
                main()
        else:
            if username == "admin" and password == '1':  # for secure admin entry
                user.User.register(username, password)
                main()
            elif username == "admin" and password != 1:
                print('You are not Admin. an admin has special password.')
                main()
            else:
                user.User.register(username, password)
                main()

    elif login_or_register == "L":
        username = input('please enter your name for login:')
        if username == 'admin':
            user.User.login(username)
            print("************ Welcome Admin ***************")
            menu.main_admin()
        else:
            if username in user.User.get_user_list():
                customer.Customer.show_product_list()
                print('if you want to buy should enter password.')
                user.User.login(username)
                print(f"************ Welcome {username} ***************")
                menu.main_customer()
            else:
                print("your not registered. please first register then login, or login with true username.")
                main()
    else:
        main()


main()
