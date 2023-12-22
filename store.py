from product import Product

class Store:
    def __init__(self):
        self.products = {Product.COLA:5, Product.MILK:5}
    
    def get_total(self, gid):
        return self.products[gid]
    
    def sell(self, gid):
        if (self.products[gid] > 0):
            self.products[gid] -= 1