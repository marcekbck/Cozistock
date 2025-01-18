# MANAGE PRODUCT 
class Product:
    def __init__(self, id, name, quantity, price, expire_date):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.expire_date = expire_date

    def __str__(self):
        return f"Product: {self.name}, Quantity: {self.quantity}, Price: {self.price}, Expire Date: {self.validade}"
