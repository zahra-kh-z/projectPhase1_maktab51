from user import User
from product import Product


class Admin(User, Product):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def creat_product(cls):
        """
        This method is for defining and registering the product by the store manager.
        The store manager defines the goods: for each item, the barcode specifies the price, brand,
        product name and inventory number.
        # register new_product should be saved in log
        """
        # new_product = Product.creat_product()
        # return new_product
        # creat instance by Product class and then admin use it. then save in csv or json file
        return print(f"New product registration was done by the store manager. "
                     f"Product: barcode, price, brand, product_name, inventory_number")

    @classmethod
    def update_inventory(cls):  # if an item is empty then save in log
        return print(f"Inventory is updated with each customer purchase. "
                     f"If inventory in stock is zero, the manager is alerted. "
                     f"(Show the administrator the first time you log in.)")

    @classmethod
    def view_invoices(cls):  # new_invoices save in log
        # see invoices.csv
        return print(f"The store manager can view previous purchase invoices.")

    @classmethod
    def show_product_list(cls):
        # see product.csv
        return print(f"product: barcode, price, brand, product_name, inventory_number.")

# admin = Admin.creat_product()
# print(Product.show_product())
