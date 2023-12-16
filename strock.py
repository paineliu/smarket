from product import Product

class Stock:
    def __init__(self):
        self.goods = {Product.COLA:5, Product.MILK:5}
    
    def get_total(self, gid):
        return self.goods[gid]
    
    def sell(self, gid):
        if (self.goods[gid] > 0):
            self.goods[gid] -= 1