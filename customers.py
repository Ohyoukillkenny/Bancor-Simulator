from smartToken import *

class Customers(object):
    def __init__(self, smartToken, smartValue = 0, reserveValue = 500):
        # _smartToken is the token customers want to buy -- SmartToken()
        self._smartToken = smartToken
        # _ownedSmartToken refers to smart token's number customers have
        self._ownedSmartToken = float(0)
        # _smartValue is the value of ownedSmartTokens -- currentPrize * owned#
        self._smartValue = float(0)
        self._reserveValue = float(reserveValue)
        # _ownedvalue = _reserveValue + _smartValue
        self._ownedvalue = float(reserveValue)
        # gain or lose money comparing to the original state
        self._budget = float(0)
        
    def printinfo(self):
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._smartToken._Price * self._ownedSmartToken + self._reserveValue
        self._budget = self._budget + self._ownedvalue - oldownedValue
        print '------'
        print 'smartToken Name:', self._smartToken._Name
        print 'ownedvalue:', self._ownedvalue, 'budget:', self._budget
        
    def purchase(self, TokenNumber):
        oldPrice = self._smartToken._Price
        if oldPrice * TokenNumber > self._reserveValue:
            print 'Invalid Operation in Purchase'
            return
        self._ownedSmartToken = self._ownedSmartToken + TokenNumber
        self._reserveValue = self._reserveValue - oldPrice * TokenNumber
        # smartToken.purchasing means being purchased
        self._smartToken.purchasing(TokenNumber)
        newPrice = self._smartToken._Price
        self._smartValue = self._ownedSmartToken * newPrice
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._reserveValue + self._smartValue
        self._budget = self._budget + self._ownedvalue - oldownedValue
        
        
    def destroy(self, TokenNumber):
        oldPrice = self._smartToken._Price
        if self._ownedSmartToken < TokenNumber:
            print 'Invalid Operation in Destroy'
            return
        self._ownedSmartToken = self._ownedSmartToken - TokenNumber
        self._reserveValue = self._reserveValue + oldPrice*TokenNumber
        # smartToken.purchasing means being purchased
        self._smartToken.destroying(TokenNumber)
        newPrice = self._smartToken._Price
        self._smartValue = self._ownedSmartToken*newPrice
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._reserveValue + self._smartValue
        self._budget = self._budget + self._ownedvalue - oldownedValue

def cust_main():
    '''
    Customers with ETH want to buy SmartTokens called KennyCoin
    '''
    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=300000)
    Alice = Customers(smartToken=KennyCoin)
    Alice.purchase(100)
    Alice.printinfo()
    KennyCoin.printInfo()
    Bob = Customers(smartToken=KennyCoin)
    Bob.purchase(100)
    Bob.printinfo()
    Alice.printinfo()

if __name__ == '__main__':
    cust_main()
