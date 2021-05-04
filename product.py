import csv
import os.path
import json
from terminaltables import AsciiTable
import pandas as pd
import logging

logging.basicConfig(filename='my_file.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class Product:
    def __init__(self, product_id, barcode, price, brand, product_name, inventory_number):
        """
        :param product_id: Product id in json file
        :param barcode: Product barcode
        :param price: Product price
        :param brand: Product brand
        :param product_name: Product name
        :param inventory_number: Product inventory_number
        """
        self.product_id = product_id
        self.barcode = barcode
        self.price = price
        self.brand = brand
        self.product_name = product_name
        self.inventory_number = inventory_number

    def creat_product(self):  # use try exception in Phase3
        """
        This method get information from admin and creat instance from class.
        Entry and registration of information is done by the manager(admin.creat_product()).
        """
        # creat product_list.csv file
        try:
            file_exists = os.path.isfile('product_list.csv')
            with open('product_list.csv', 'a', newline='') as write_product_list:
                fieldnames = ['product_id', 'barcode', 'price', 'brand', 'product_name', 'inventory_number']
                csv_writer = csv.DictWriter(write_product_list, fieldnames=fieldnames)
                if not file_exists:
                    csv_writer.writeheader()  # file doesn't exist yet, write a header
                csv_writer.writerow({'product_id': self.product_id, 'barcode': self.barcode, 'price': self.price,
                                     'brand': self.brand, 'product_name': self.product_name,
                                     'inventory_number': self.inventory_number})
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')

        # creat product_list.json file
        product_instance = {'product_id': self.product_id + 1, 'barcode': self.barcode, 'price': self.price,
                            'brand': self.brand, 'product_name': self.product_name,
                            'inventory_number': self.inventory_number}
        with open('product_list.json', 'a', newline='') as write_product_list:
            json.dump(product_instance, write_product_list, ensure_ascii=False)

    @staticmethod
    def update_inventory(my_choice_id, new_inventory_number):
        """
        This method reading the product_list.csv file.use importing the pandas library.
        updating the column value/data. Inventory is updated with each customer purchase.
        """
        try:
            df = pd.read_csv("product_list.csv")  # reading the csv file
            df.loc[
                my_choice_id - 1, 'inventory_number'] = new_inventory_number  # updating the column 'inventory_number'
            df.to_csv("product_list.csv", index=False)  # writing into the file
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')

        """
        Inventory is updated with each customer purchase. 
        If inventory in stock is zero, the manager is alerted.
        (Show the administrator the first time you log in.)
        """
        with open('product_list.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row["product_id"]) == my_choice_id and int(row["inventory_number"]) == 0:
                    logging.warning(f'Inventory is empty for product_id:{row["product_id"]},{row["product_name"]}')

    @staticmethod
    def show_product():
        """
        This method show all product for admin in table format
        """
        total_row = []
        table_column_headers = ['product_id', 'barcode', 'price', 'brand', 'product_name', 'inventory_number']
        total_row.append(table_column_headers)
        try:
            with open('product_list.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    rows = [row['product_id'], row['barcode'], row['price'] + ' $', row['brand'], row['product_name'],
                            row['inventory_number']]
                    total_row.append(rows)

        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
            print(table.table)

        # # show all product for admin from json file
        # with open('product_list.json', 'r', encoding='utf-8') as read_product_list:
        #     product_list = json.loads(read_product_list)
        #     for key, val in product_list.items():
        #         print(key, val)
        #     print(product_list)
        #     print(type(product_list))

# print(Product.show_product())
