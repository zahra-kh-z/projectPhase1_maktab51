import csv
import os.path
from terminaltables import AsciiTable
import pandas as pd
import my_log


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

    def creat_product(self):
        """
        This method get information from admin and creat instance from class.
        Entry and registration of information is done by the manager(admin.add_product()).
        """
        try:
            file_exists = os.path.isfile('product_list.csv')
            with open('product_list.csv', 'a', newline='') as write_product_list:  # creat product_list.csv file
                fieldnames = ['product_id', 'barcode', 'price', 'brand', 'product_name', 'inventory_number']
                csv_writer = csv.DictWriter(write_product_list, fieldnames=fieldnames)
                if not file_exists:
                    csv_writer.writeheader()  # file doesn't exist yet, write a header
                csv_writer.writerow({'product_id': self.product_id, 'barcode': self.barcode, 'price': self.price,
                                     'brand': self.brand, 'product_name': self.product_name,
                                     'inventory_number': self.inventory_number})
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')

    def sale(username, my_choice_id, buy_basket):
        """
        From the available goods, the customer can choose a number to buy. the final purchase price of the customer is
        calculated and displayed based on the selected goods and their number.
        """
        with open('product_list.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if my_choice_id == int(row['product_id']):
                    while True:
                        try:
                            count_product = int(input('Enter num for buy this product:'))
                            break
                        except ValueError:
                            print('You did not enter a number!')
                    try:
                        assert count_product <= int(row['inventory_number'])
                        new_inventory_number = int(row['inventory_number']) - count_product
                        Product.update_inventory(my_choice_id, new_inventory_number)  # if zero save in log
                        total_price = int(row['price']) * count_product
                        basket_element = ({'product_name': row['product_name'], 'price': row['price'] + ' $',
                                           'count_product': count_product, 'total_price': total_price})
                        buy_basket.append(basket_element)
                    except AssertionError:
                        print(f'inventory has {int(row["inventory_number"])} product')
                        if int(row["inventory_number"]) == 0:
                            my_log.logger.warning(f'{username} requested purchase from zero inventory.')

    @staticmethod
    def update_inventory(my_choice_id, new_inventory_number):
        """
        This method reading the product_list.csv file.use importing the pandas library.
        updating the column value/data. Inventory is updated with each customer purchase.
        """
        try:
            df = pd.read_csv("product_list.csv")  # reading the csv file
            df.loc[my_choice_id - 1, 'inventory_number'] = new_inventory_number  # update the column 'inventory_number'
            df.to_csv("product_list.csv", index=False)  # writing into the file
            if new_inventory_number == 0:
                my_log.logger.warning(f'Inventory is empty for product_id:{my_choice_id}')
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')

    @staticmethod
    def delete_product(my_choice_id):
        """
        This method delete a product from product_list.csv file
        """
        try:
            df = pd.read_csv("product_list.csv")  # reading the csv file
            df = df.drop(df.index[my_choice_id - 1])  # delete product
            df.to_csv("product_list.csv", index=False)  # writing into the file
            my_log.logger.info(f'Admin delete product_id:{my_choice_id}')
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')

    @classmethod
    def show_product(cls, username):
        """
        This method show all product for admin in table format. This method show product list for customer but
        the customer can see the list of products: product_id, product_name, brand, price.
        """
        total_row = []
        if username == 'admin':
            table_column_headers = ['product_id', 'barcode', 'price', 'brand', 'product_name', 'inventory_number']
        else:
            table_column_headers = ['product_id', 'product_name', 'brand', 'price']
        total_row.append(table_column_headers)
        try:
            with open('product_list.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if username == 'admin':
                        rows = [row['product_id'], row['barcode'], row['price'] + ' $', row['brand'],
                                row['product_name'], row['inventory_number']]
                    else:
                        rows = [row['product_id'], row['product_name'], row['brand'], row['price'] + ' $']
                    total_row.append(rows)
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
        return table
