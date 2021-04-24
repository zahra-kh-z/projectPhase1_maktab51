from admin import Admin


class Customer(Admin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def buy_product(cls):  # sale()
        # (product_name, count)
        # invoice.csv ----> factor
        return print(f"From the available goods, the customer can choose a number to buy. "
                     f"The final purchase price of the customer is calculated "
                     f"and displayed based on the selected goods and their number.")

    @classmethod
    def invoice(cls):  # invoice should be saved in file and log / use buy_product()
        return print(f"An invoice is issued based on the customer's purchase.")

    @staticmethod
    def show_product_list():
        # only show product_name, brand and price  from product_list.csv
        # Product.show_product(product_name, brand, price)
        return print(f"you are a customer.\t "
                     f"The customer can see the list of goods. product: product_name, barcode, price. ")
