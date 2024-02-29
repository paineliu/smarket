from product import Product

class User:
    NONE = 0
    ENTER = 1
    LEAVE = 2

    def __init__(self):        
        self.reset()
    
    def reset(self):
        self.status = self.NONE
        self.products = {Product.COLA:0, Product.MILK:0}

    def get_status(self):
        return self.status
    
    def enter(self):
        self.status = self.ENTER
        self.products = {Product.COLA:0, Product.MILK:0}

    def get_total(self, gid):
        return self.products[gid]
    
    def buy(self, gid):
        self.products[gid] += 1

    def need_pay(self):
        total = 0
        for g in self.products:
            total += self.products[g]
        return total > 0

    def pay(self):
        self.products = {Product.COLA:0, Product.MILK:0}

    def leave(self):
        self.status = self.LEAVE