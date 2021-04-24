import hashlib
import sys


class User:
    def __init__(self, username, password, first_name=None, last_name=None, email=None, address=None):
        """
        :param username: name of user for login
        :param password: password of user for login
        """
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address

    @staticmethod
    def register(username, password):
        """
        This method records user information as a manager or client. ----> Admin / Customer
        """
        with open('user_file.txt', 'a+') as user_info:
            hash_password = (hashlib.sha256(password.encode())).hexdigest()
            user_info.write(f"\nUsername: {username} Password: {hash_password}\n")
            print(f"{username} your username and password has been made.")
            with open('user_list.txt', 'a+') as user_list_name:
                user_list_name.write(username + ',')  # Append username to user_list

    @staticmethod
    def login(username):
        """
        This method allows the user to login as a manager or client by entering information.
        # if username==admin then save in log ---> this should be handle in Phase2
        """
        count = 0
        success = False
        while count <= 3 and not success:
            password = input('Please enter your password:')
            hash_password = (hashlib.sha256(password.encode())).hexdigest()
            with open("user_file.txt", "r") as username_finder:
                for line in username_finder:
                    if ("Username: " + username + " Password: " + hash_password) == line.strip():
                        print(f"{username} You are logged in system. now choose what you want.")
                        success = True
                        break
                if not success:
                    print("Sorry, this username or password does not exist please try again or register.")
                    count += 1
                if count == 3:  # save in log in phase2
                    print("------------------- Note ---------------------------")
                    print("You entered the wrong password 3 times."
                          "You have been locked out please restart to try again.")
                    sys.exit()

    @classmethod
    def get_user_list(cls):
        with open('user_list.txt') as user_list:  # in this file all username is stored
            user = user_list.read().split(',')
        return user

    def logging(self):
        """
        This method save logs user information. for Phase2
        Log the following events:
        Administrator login
        New product definition
        Issuance of a new invoice
        Check out the product in stock
        Errors and warnings
        """
        pass
