import csv
import sys
import pandas as pd
import hashlib
import logging

logging.basicConfig(filename='my_file.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class User:
    def __init__(self, username, password, first_name=None, last_name=None, email=None, address=None):
        """
        :param username: name of user for login
        :param password: password of user for login
        :param first_name: firs name for user
        :param last_name: last name for user
        :param email: email for user
        :param address: address for user
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
        hash_password = hashlib.sha256(password.encode("utf8")).hexdigest()
        obj_user = User(username, hash_password)
        row_user_info = [[obj_user.username, obj_user.password]]  # dataframe is a nested list [[]]
        try:
            with open("user_information.csv", 'a', newline='') as csv_user_info:
                csv_writer = csv.writer(csv_user_info)
                csv_writer.writerows(row_user_info)  # writing the data row
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
        else:
            print(f"{username.capitalize()} your username and password has been made.")

    @staticmethod
    def login(username):
        """
        This method allows the user to login as a manager or client by entering information.
        # if username==admin then save in log  and alert for inventory zero ---> this should be handle in Phase3
        """
        count = 0
        success = False
        while count <= 3 and not success:
            password = input('Please enter your password:')
            hash_password = hashlib.sha256(password.encode("utf8")).hexdigest()
            try:
                with open("user_information.csv", "r") as csv_user_info:
                    username_finder = csv.reader(csv_user_info)
                    for line in username_finder:
                        if line[0] == username and line[1] == hash_password:
                            print(f"{username.capitalize()} You are logged in system. now choose what you want.")
                            success = True
                            break
                    if not success:
                        print("Sorry, this username or password does not exist please try again or register.")
                        count += 1
                    if count == 3:  # save in log in phase3
                        logging.warning(f'{username} entered the wrong password 3 times')
                        print("------------------- Note ---------------------------")
                        print("You entered the wrong password 3 times."
                              "You have been locked out please restart to try again.")
                        sys.exit()
            except FileNotFoundError:
                print('Error: File user_information.csv Not Found')
                break

    @staticmethod
    def change_password():
        username = input("Please enter your Username for change_password:")
        try:
            df_user_info = pd.read_csv('user_information.csv')
            location = 0
            current_password = input("Enter Current password: ")
            hash_current_password = hashlib.sha256(current_password.encode("utf8")).hexdigest()
            with open('user_information.csv') as my_file:
                csv_reader = csv.DictReader(my_file)
                for row in csv_reader:
                    if username == row['username'] and hash_current_password == row['password']:
                        print("Your username and password are correct.")
                        new_password = input("Enter New password: ")
                        confirm_password = input("Enter New password confirmation: ")
                        if new_password == confirm_password:
                            hash_new_pass = hashlib.sha256(new_password.encode("utf8")).hexdigest()
                            df_user_info.loc[location, 'password'] = hash_new_pass
                            df_user_info.to_csv('user_information.csv', index=False)
                            print("Your password was changed successfully.")
                        else:
                            print('Confirm password is not equal to New password.')
                        break
                    location += 1
                else:
                    print('Your username or password is incorrect.')
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
