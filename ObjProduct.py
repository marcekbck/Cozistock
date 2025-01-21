# MANAGE PRODUCT 
class Product:
    def __init__(self, id, name, quantity, price, expire_date, image_path):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.expire_date = expire_date
        self.image_path = image_path
    def __str__(self):
        return f"Product: {self.name}, Quantity: {self.quantity}, Price: {self.price}, Expire Date: {self.validade}, Image Path: {self.image_path}"
