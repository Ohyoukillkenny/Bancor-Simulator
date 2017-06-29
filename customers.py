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
        # since new reserve will be converted into or out the kenny coin, the budget could change
        # when print info, update the budget
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._smartToken._Price * self._ownedSmartToken + self._reserveValue
        self._budget = self._budget + self._ownedvalue - oldownedValue
        print '------'
        print 'smartToken Name:', self._smartToken._Name
        print 'ownedvalue:', self._ownedvalue, 'budget:', self._budget
        
    def getReserveValue(self):
        return self._reserveValue
        
    def purchase(self, reserveTokenNumber):
        oldPrice = self._smartToken._Price
        if reserveTokenNumber > self._reserveValue:
            print 'Invalid Operation in Purchase'
            return
        # smartToken.purchasing means being converted
        issuedSmartToken = self._smartToken.purchasing(reserveTokenNumber)
        newPrice = self._smartToken._Price      
        self._ownedSmartToken = self._ownedSmartToken + issuedSmartToken
        self._smartValue = self._ownedSmartToken * newPrice
        self._reserveValue = self._reserveValue - reserveTokenNumber
        # in fact, in this case ownedValue and budget actually does not change at all
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._reserveValue + self._smartValue
        self._budget = self._budget + self._ownedvalue - oldownedValue
        
        
    def destroy(self, smartTokenNumber):
        oldPrice = self._smartToken._Price
        if self._ownedSmartToken < smartTokenNumber:
            print 'Invalid Operation in Destroy'
            return
        self._ownedSmartToken = self._ownedSmartToken - smartTokenNumber
        # smartToken.purchasing means being purchased
        ReceivedToken = self._smartToken.destroying(smartTokenNumber)
        newPrice = self._smartToken._Price
        self._smartValue = self._ownedSmartToken*newPrice
        self._reserveValue = self._reserveValue + ReceivedToken
        # In fact, in this case ownedValue actually does not change at all
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
