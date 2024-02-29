from product import Product

class Store:
    def __init__(self):
        self.reset()

    def reset(self):
        self.products = {Product.COLA:3, Product.MILK:3}
        
    def get_total(self, gid):
        return self.products[gid]
    
    def sell(self, gid):
        if (self.products[gid] > 0):
            self.products[gid] -= 1