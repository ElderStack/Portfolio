class Inventory():
    
    def __init__(self):
        self.coins = 0
        self.double_jump = False
        
    def getCoins(self):
        return self.coins
    
    def increaseCoins(self):
        self.coins += 1
    
    def decreaseCoins(self):
        self.coins -= 1
        
    def getDoubleJump(self):
        return self.double_jump
    
    def setDoubleJump(self, jump):
        self.double_jump = jump