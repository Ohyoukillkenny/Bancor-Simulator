from smartToken import *

class Customers(object):
    '''
    _smartToken: the token customers want to buy -- SmartToken()
    _ownedSmartToken: smart token's number customers have, being rounded as whitepaper
    _reserveTokens: reserve token's number customers have, being rounded as whitepaper
    _ownedvalue = _reserveValue + _smartValue: the total money cust has, using reserveToken as measurement
    _originalMoney: original money cust has
    _moneyBalance: value of money gained or lost, comparing to the original state
    _expectedPrice: how much money customers are willing to finish the transaction
    '''
    def __init__(self, smartToken, ownedSmartTokens = 0, reserveTokens = 0, expectedPrice = 0):
        self._smartToken = smartToken
        self._ownedSmartTokens = int(ownedSmartTokens)
        self._reserveTokens = int(reserveTokens)
        self._ownedvalue = float(smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
        self._originalMoney = self._ownedvalue
        self._moneyBalance = float(0)
        self._expectedPrice = float(expectedPrice)
        
    def printinfo(self):
        # since new reserve will be converted into or out the smarttoken, Price will change
        # when print info, update the _ownedvalue
        self._ownedvalue = float(self._smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
        self._moneyBalance = self._ownedvalue - self._originalMoney
        print '------'
        print 'smartToken Name:', self._smartToken._Name, '| expected price:', self._expectedPrice
        print 'ownedvalue:', self._ownedvalue, '| money Balance:', self._moneyBalance
    def getReserveTokens(self):
        return self._reserveTokens
    def getownedSmartTokens(self):
        return self._ownedSmartTokens
    def getmoneyBalance(self):
        self._ownedvalue = float(self._smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
        self._moneyBalance = self._ownedvalue - self._originalMoney
        return self._moneyBalance
    def getExpectedPrice(self):
        return self._expectedPrice
    # add customer's reserve amount
    def addReserve(self, addAmount):
        if isinstance(addAmount,int):
            self._reserveTokens = self._reserveTokens + addAmount
            self._ownedvalue = float(self._smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
            # this part money is independant with bancor balance
            self._originalMoney = self._originalMoney + addAmount * 1
        else:
            print "** ERROR, only can add integer # of reserveTokens to reserve"
    # change the expected price
    def changeExpectedPrice(self, newExpectedPrice):
        self._expectedPrice = newExpectedPrice

    '''
    use reserveToken to buy smartToken -> smartToken price increase
    call smartTokens.purchasing() function
    '''
    def buy(self, reserveTokenNumber):
        if reserveTokenNumber < 0:
            print '** ERROR, cannot buy negative number of smartToken'
            return
        if reserveTokenNumber > self._reserveTokens:
            print '** ERROR, invalid Operation in buy'
            return
        if not isinstance(reserveTokenNumber,int):
            print '** ERROR, should use integer number of reserveTokens to buy'
            return
        self._reserveTokens = self._reserveTokens - reserveTokenNumber
        issuedSmartToken = self._smartToken.purchasing(reserveTokenNumber)
        self._ownedSmartTokens = self._ownedSmartTokens + issuedSmartToken
        self._ownedvalue = float(self._smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
        self._moneyBalance = self._ownedvalue - self._originalMoney
        
    '''
    sell smartToken to get reserveToken -> smartToken price decrease
    call smartTokens.destroying() function
    '''        
    def sell(self, smartTokenNumber):
        if smartTokenNumber < 0:
            print '** ERROR, cannot sell negative number of smartToken'
            return
        if self._ownedSmartTokens < smartTokenNumber:
            print '** ERROR, invalid Operation in sell'
            return
        if not isinstance(smartTokenNumber,int):
            print '** ERROR, should use integer number of smartTokens to sell'
            return
        self._ownedSmartTokens = self._ownedSmartTokens - smartTokenNumber
        ReceivedToken = self._smartToken.destroying(smartTokenNumber)
        self._reserveTokens = self._reserveTokens + ReceivedToken
        self._ownedvalue = float(self._smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
        self._moneyBalance = self._ownedvalue - self._originalMoney

def cust_main():
    '''
    Customers with ETH want to buy SmartTokens called KennyCoin
    '''
    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=300000)
    # test for customers class
    Alice = Customers(smartToken=KennyCoin,ownedSmartTokens=100,reserveTokens=100,expectedPrice= 2)
    Alice.printinfo()
    Alice.buy(90.12)
    Alice.buy(101)
    Alice.buy(100)
    Alice.printinfo()
    Alice.sell(124)
    Alice.printinfo()

if __name__ == '__main__':
    cust_main()
