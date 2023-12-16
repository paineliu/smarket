from product import Product

class User:
    NOT_ENTER = 0
    ENTER = 1
    LEAVE = 2

    def __init__(self):        
        
        self.status = self.NOT_ENTER
        self.goods = {Product.COLA:0, Product.MILK:0}
    
    def get_status(self):
        return self.status
    
    def enter(self):
        self.status = self.ENTER
        self.goods = {Product.COLA:0, Product.MILK:0}

    def get_total(self, gid):
        return self.goods[gid]
    
    def buy(self, gid):
        self.goods[gid] += 1

    def need_pay(self):
        total = 0
        for g in self.goods:
            total += self.goods[g]
        return total > 0

    def pay(self):
        self.goods = {Product.COLA:0, Product.MILK:0}

    def leave(self):
        self.status = self.LEAVE