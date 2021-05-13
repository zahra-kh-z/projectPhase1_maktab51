from user import User
from product import Product
import csv
from terminaltables import AsciiTable
import pandas as pd
import my_log
import menu
import os.path


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    @staticmethod
    def add_product(barcode, price, brand, product_name, inventory_number):
        """
        New product registration was done by the store manager.
        creat instance by Product class and then admin use it. then save in csv or json file
        This method is for defining and registering the product by the store manager.
        The store manager defines the goods: for each item, the barcode specifies the price, brand,
        product name and inventory number.
        """
        try:
            with open('product_list.csv', 'r') as csv_file:  # this is for set product_id base on csv file
                csv_reader = csv.DictReader(csv_file)
                line_count = 1
                for row in csv_reader:
                    if line_count == 1:
                        product_id = 1
                        line_count += 1
                    else:
                        product_id = line_count
                        line_count += 1
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')
        else:
            product_instance = Product(product_id + 1, barcode, price, brand, product_name, inventory_number)
            product_instance.creat_product()
            my_log.logger.info(f'Admin add product {product_name}')
            return product_instance

    @staticmethod
    def activate_account(username):
        """
        This method is for activating the username by the admin. Only the admin can unblock the customer.
        """
        username_list = menu.file_path_username_list()
        location = 0
        df = pd.read_csv("user_information.csv")  # reading the csv file
        with open('user_information.csv') as my_file:
            csv_reader = csv.DictReader(my_file)
            try:
                assert username in username_list
                for row in csv_reader:
                    if username == row['username']:
                        df.loc[location, 'status'] = 'Active'  # updating the column 'status' and Active username
                        df.loc[location, 'login'] = 'True'
                        df.to_csv("user_information.csv", index=False)  # writing into the file
                        my_log.logger.info(f'Admin activated customer_{username}')
                    location += 1
            except AssertionError:
                print('The username entered is not in the blocked list.')

    @classmethod
    def add_update_inventory(cls, product_id, new_inventory_number):
        """
        This method reading the product_list.csv file. use importing the pandas library.
        updating the column value/data. The number of inventory is increased by the manager.
        """
        df = pd.read_csv("product_list.csv")  # reading the csv file
        df.loc[product_id - 1, 'inventory_number'] += new_inventory_number  # updating the column 'inventory_number'
        df.to_csv("product_list.csv", index=False)  # writing into the file

    def save_to_invoice_file(username, time, sum_invoice, buy_basket):
        """
        An invoice is issued based on the customer's purchase.
        invoice should be saved in invoice.csv file and log / use buy_product()
        """
        try:
            file_exists = os.path.isfile('invoice.csv')
            with open('invoice.csv', 'a', newline='') as write_invoice:
                fieldnames = ['customer_name', 'timestamp', 'price_invoice', 'buy_basket']
                csv_writer = csv.DictWriter(write_invoice, fieldnames=fieldnames)
                if not file_exists:
                    csv_writer.writeheader()  # file doesn't exist yet, write a header
                csv_writer.writerow(
                    {'customer_name': username, 'timestamp': time, 'price_invoice': sum_invoice,
                     'buy_basket': buy_basket})
                my_log.logger.info(f'send new invoice to customer_name: {username}')
        except FileNotFoundError:
            print('Error: File invoice.csv Not Found')

    @classmethod
    def view_invoices(cls, username):
        """
        The store manager can view previous purchase invoices. This method show all invoice for each customer.
        also, If a customer has purchased more than once, all his invoices will be displayed.
        An invoice is issued based on the customer's purchase.
        """
        total_row = []
        table_column_headers = ['customer_name', 'timestamp', 'sum_invoice', 'buy_basket']
        total_row.append(table_column_headers)
        try:
            with open('invoice.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if username == 'admin':
                        rows = [row['customer_name'], row['timestamp'], row['price_invoice'] + ' $', row['buy_basket']]
                        total_row.append(rows)
                    else:
                        if row['customer_name'] == username:
                            rows = [row['customer_name'], row['timestamp'], row['price_invoice'] + ' $',
                                    row['buy_basket']]
                            total_row.append(rows)
        except FileNotFoundError:
            print('Error: File invoice.csv Not Found')
            my_log.logger.error('File invoice.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
        return table
