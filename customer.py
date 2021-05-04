from admin import Admin
from product import Product
import csv
import os.path
from terminaltables import AsciiTable
import logging

logging.basicConfig(filename='my_file.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class Customer(Admin):
    def __init__(self, username, password, buy_basket=None, total_price=0):
        super().__init__(username, password)
        """
        :param basket: buy_basket for customer
        :param total_price: total_price for each element in basket
        """
        self.basket = buy_basket
        self.total_price = total_price

    def buy_product(username):
        """
        From the available goods, the customer can choose a number to buy. the final purchase price of the customer is
        calculated and displayed based on the selected goods and their number.
        """
        try:
            file = open("product_list.csv")
            reader = csv.reader(file)
            lines = len(list(reader))
            all_id = lines - 1

            buy_basket = []  # basket for add basket_element with count and total price for each product is selected
            # counter = 0
            # num = int(input('Enter a number for count of products you want to buy: '))
            # print('Enter "product_id" and count from above table to buy a product. press "s" for stop.')
            stop = False
            while not stop:
                print('Enter "product_id" and count from above table to buy a product. press "0" for stop.')
                while True:
                    try:
                        my_choice_id = int(input('my_choice_id:'))
                        assert my_choice_id <= all_id
                        break
                    except ValueError:
                        print('You did not enter a number!')
                    except AssertionError:
                        print(f'You can select id from 1-{all_id} product_id!')
                if my_choice_id != 0:
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
                                    Product.update_inventory(my_choice_id, new_inventory_number)  # if zero save log
                                    total_price = int(row['price']) * count_product
                                    basket_element = (
                                        {'product_id': row['product_id'], 'product_name': row['product_name'],
                                         'brand': row['brand'], 'price': row['price'] + ' $',
                                         'count_product': count_product,
                                         'total_price': total_price})
                                    buy_basket.append(basket_element)
                                except AssertionError:
                                    print(f'inventory has {int(row["inventory_number"])} product')
                        # counter += 1
                else:
                    stop = True
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
        else:
            """for calculate total price invoice for each buy_basket"""
            list_total_price = [int(product['total_price']) for product in buy_basket]
            sum_invoice = sum(list_total_price)

            """for print buy_basket and price invoice for each buy in table format"""
            total_row = []
            table_column_headers = ['product_id', 'product_name', 'brand', 'price', 'count_product', 'total_price']
            total_row.append(table_column_headers)
            print('Your buy_basket is:')
            for product in buy_basket:
                product_row = [product['product_id'], product['product_name'], product['brand'],
                               product['price'], product['count_product'], product['total_price']]
                total_row.append(product_row)
            data = total_row
            table = AsciiTable(data)
            print(table.table)
            print(f'Your price_invoice is: {sum_invoice} $')

            """
            An invoice is issued based on the customer's purchase.
            invoice should be saved in invoice.csv file and log / use buy_product()
            """
            # new_invoices save in log for phase3
            file_exists = os.path.isfile('invoice.csv')
            with open('invoice.csv', 'a', newline='') as write_invoice:
                fieldnames = ['customer_name', 'price_invoice', 'buy_basket']
                csv_writer = csv.DictWriter(write_invoice, fieldnames=fieldnames)
                if not file_exists:
                    csv_writer.writeheader()  # file doesn't exist yet, write a header
                csv_writer.writerow(
                    {'customer_name': username, 'price_invoice': sum_invoice, 'buy_basket': buy_basket})
                logging.warning(f'send a invoice to customer for {username}')

    @staticmethod
    def invoice(username):
        """
        This method show all invoice for each customer.
        If a customer has purchased more than once, all his invoices will be displayed.
        An invoice is issued based on the customer's purchase.
        """
        total_row = []
        table_column_headers = ['customer_name', 'sum_invoice', 'buy_basket']
        total_row.append(table_column_headers)
        try:
            with open('invoice.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row['customer_name'] == username:
                        rows = [row['customer_name'], row['price_invoice'] + ' $', row['buy_basket']]
                        total_row.append(rows)
        except FileNotFoundError:
            print('Error: File invoice.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
            print(table.table)

    @staticmethod
    def show_product():
        """
        This method show product list for customer.
        The customer can see the list of products: product_id, product_name, brand, price.
        """
        total_row = []
        table_column_headers = ['product_id', 'product_name', 'brand', 'price']
        total_row.append(table_column_headers)
        try:
            with open('product_list.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    rows = [row['product_id'], row['product_name'], row['brand'], row['price'] + ' $']
                    total_row.append(rows)
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
            print(table.table)
