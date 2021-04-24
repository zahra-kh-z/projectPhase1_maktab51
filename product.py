# we can create instance of product and save them in a product_list.csv or json in Phase2

class Product:
    def __init__(self, barcode, price, brand, product_name, inventory_number):
        """
        :param barcode: Product barcode
        :param price: Product price
        :param brand: Product brand
        :param product_name: Product name
        :param inventory_number: Product inventory_number
        """
        self.barcode = barcode
        self.price = price
        self.brand = brand
        self.product_name = product_name
        self.inventory_number = inventory_number

    @classmethod
    def creat_product(cls):  # use try exception in Phase2
        """
        This method get information from admin and creat instance from class.
        Entry and registration of information is done by the manager(admin.creat_product()).
        """
        print(f'enter information for product:')
        barcode = input('barcode:')
        price = input('price:')
        brand = input('brand:')
        product_name = input('product_name:')
        inventory_number = input('inventory_number')
        # product_instance = Product(barcode, price, brand, product_name, inventory_number)
        return cls(barcode, price, brand, product_name, inventory_number)

    def sale(self):
        # update inventory_number = inventory_number - count  # update in csv
        # if inventory_number==0 save to log and show warning to admin
        # total_price = count * price
        pass

    def show_product(self):
        return f'barcode: {self.barcode}, price: {self.price}, brand: {self.brand}, ' \
               f'product_name: {self.product_name}, inventory_number: {self.inventory_number}'
