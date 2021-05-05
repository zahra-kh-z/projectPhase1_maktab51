from user import User
from product import Product
import csv
from terminaltables import AsciiTable
import pandas as pd
import logging

logging.basicConfig(filename='my_file.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    @staticmethod
    def add_product():
        """
        New product registration was done by the store manager.
        creat instance by Product class and then admin use it. then save in csv or json file
        This method is for defining and registering the product by the store manager.
        The store manager defines the goods: for each item, the barcode specifies the price, brand,
        product name and inventory number.
        # register new_product should be saved in log for phase3
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
        else:
            print(f'Enter information for product:')
            while True:
                try:
                    barcode = int(input('Barcode:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            while True:
                try:
                    price = int(input('Price:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            while True:
                try:
                    inventory_number = int(input('Inventory_number:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            brand = input('Brand:')
            product_name = input('Product_name:')
            product_instance = Product(product_id + 1, barcode, price, brand, product_name, inventory_number)
            product_instance.creat_product()
            logging.warning('Admin add product')
            return product_instance

    @staticmethod
    def add_update_inventory():
        """
        This method reading the product_list.csv file.use importing the pandas library.
        updating the column value/data. The number of inventory is increased by the manager.
        """
        try:
            file = open("product_list.csv")
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
        else:
            reader = csv.reader(file)
            lines = len(list(reader))
            all_id = lines - 1

            while True:
                try:
                    product_id = int(input('Enter product_id for update:'))
                    assert 0 < product_id <= all_id
                    break
                except ValueError:
                    print('You did not enter a number!')
                except AssertionError:
                    print(f'You can select id from 1-{all_id} product_id!')
            while True:
                try:
                    new_inventory_number = int(input('Enter inventory_number for add:'))
                    break
                except ValueError:
                    print('You did not enter a number!')

            df = pd.read_csv("product_list.csv")  # reading the csv file
            df.loc[product_id - 1, 'inventory_number'] += new_inventory_number  # updating the column 'inventory_number'
            df.to_csv("product_list.csv", index=False)  # writing into the file

    @classmethod
    def view_invoices(cls):
        """
        The store manager can view previous purchase invoices.
        """
        total_row = []
        table_column_headers = ['customer_name', 'sum_invoice', 'buy_basket']
        total_row.append(table_column_headers)
        try:
            with open('invoice.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    rows = [row['customer_name'], row['price_invoice'], row['buy_basket']]
                    total_row.append(rows)
        except FileNotFoundError:
            print('Error: File invoice.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
            print(table.table)
