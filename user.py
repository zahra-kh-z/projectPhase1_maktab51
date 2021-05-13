import csv
import pandas as pd
import hashlib
import my_log
import menu


class User:
    def __init__(self, username, password, status='Active', login=True, first_name=None, last_name=None, email=None,
                 address=None):
        """
        :param username: name of user for login
        :param password: password of user for login
        :param status: is status='Active' user is Active user, and if status='Blocked' user is Blocked user or locked
        :param first_name: firs name for user
        :param login: login or logout user
        :param last_name: last name for user
        :param email: email for user
        :param address: address for user
        """
        self.username = username
        self.password = password
        self.status = status
        self.login = login
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
        row_user_info = [
            [obj_user.username, obj_user.password, obj_user.status, obj_user.login]]  # dataframe is a nested list [[]]
        try:
            with open("user.csv", 'a', newline='') as csv_user_info:
                csv_writer = csv.writer(csv_user_info)
                csv_writer.writerows(row_user_info)  # writing the data row
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
            my_log.logger.error('File user_information.csv Not Found')
        else:
            print(f"{username.capitalize()} your username and password has been made.")

        # for add user_id to user_information.csv file, based on user.csv indexes.
        sample = pd.read_csv('user.csv')
        sample.index.name = 'user_id'
        sample.to_csv('user_information.csv', index=True)

    def logout(username, status, login):
        """
        This method is for changing the login/logout mode and the status of the user.
        """
        location = 0
        try:
            df = pd.read_csv("user_information.csv")  # reading the csv file
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
        else:
            with open('user_information.csv') as my_file:
                csv_reader = csv.DictReader(my_file)
                for row in csv_reader:
                    if username == row['username']:
                        df.loc[location, 'status'] = status  # locked/unlocked the column 'status' for username
                        df.loc[location, 'login'] = login
                        df.to_csv("user_information.csv", index=False)  # writing into the file
                    location += 1

    @staticmethod
    def login(username):
        """
        This method allows the user to login as a manager or client by entering information.
        """
        count = 0
        success_login = False
        while count <= 3 and not success_login:
            password = input('Please enter your password:')
            hash_password = hashlib.sha256(password.encode("utf8")).hexdigest()
            try:
                with open("user_information.csv", "r") as csv_user_info:
                    username_finder = csv.reader(csv_user_info)
                    for line in username_finder:
                        if line[1] == username and line[2] == hash_password and line[3] == 'Blocked':
                            print("Your username is Blocked. Only the admin can activate your username. "
                                  "If necessary, send an activation request email to the admin.")
                            User.logout(username, 'Blocked', 'False')
                            menu.print_menu_register_login()
                            success_login = True
                            break
                        elif line[1] == username and line[2] == hash_password and line[3] == 'Active':
                            print(f"{username.capitalize()} You are logged in system. now choose what you want.")
                            if username == 'admin':
                                my_log.logger.info('Admin logged in')
                                print("************ Welcome Admin ***************")
                                menu.check_inventory()
                                menu.main_admin(username)
                            else:
                                print(f"************ Welcome {username.capitalize()} ***************")
                                User.logout(username, 'Active', 'True')
                                menu.main_customer(username)
                            success_login = True
                            break
                    if not success_login:
                        print("Sorry, this username or password does not exist please try again or register.")
                        count += 1
                    if count == 3:
                        if username != 'admin':
                            User.logout(username, 'Blocked', 'False')
                            menu.print_menu_register_login()
                            my_log.logger.error(
                                f'{username} entered the wrong password 3 times, {username} is Blocked.')
                            break
                        else:
                            my_log.logger.error(f'{username} entered the wrong password 3 times.')
                        print("------------------- Note ---------------------------")
                        print("You entered the wrong password 3 times."
                              "You have been locked out please restart to try again.")
                        menu.print_menu_register_login()
                        break
            except FileNotFoundError:
                print('Error: File user_information.csv Not Found')
                my_log.logger.error('File user_information.csv Not Found')
                break

    @classmethod
    def change_password(cls, username, current_password, new_password, confirm_password):
        """
        This method for change password for special username
        """
        try:
            df_user_info = pd.read_csv('user_information.csv')
            location = 0
            hash_current_password = hashlib.sha256(current_password.encode("utf8")).hexdigest()
            with open('user_information.csv') as my_file:
                csv_reader = csv.DictReader(my_file)
                for row in csv_reader:
                    if username == row['username'] and hash_current_password == row['password']:
                        try:
                            assert new_password == confirm_password
                            hash_new_pass = hashlib.sha256(new_password.encode("utf8")).hexdigest()
                            df_user_info.loc[location, 'password'] = hash_new_pass
                            df_user_info.to_csv('user_information.csv', index=False)
                            print("Your password was changed successfully.")
                        except AssertionError:
                            print('Confirm password is not equal to New password.')
                        break
                    location += 1
                else:
                    print('Your username or password is incorrect.')
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
            my_log.logger.error('File user_information.csv Not Found')
