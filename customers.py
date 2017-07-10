from smartToken import *

class Customer(object):
    '''
    _smartToken: class of the token customers want to buy or sell -- SmartToken()
    _market: instance of the market customers buy or sell 

    _valuation: how much money customers are willing to finish the transaction
    _tokenBalance: number of smart tokens a customer has
    _reserveBalance: number of reserve tokens a customer has

    _originalCash: original money cust has
    _cash: net profit or loss to date
    '''
    def __init__(self, smartToken, ownedSmartTokens = 0, reserveTokens = 0, valuation = 0.0):
        self._smartToken = smartToken
        self._ownedSmartTokens = 0
        self._reserveTokens = int(reserveTokens)

        self._originalCash = self._reserveTokens
        self._cash = 0.0
        self._valuation = valuation
        
    def printinfo(self):
        # since new reserve will be converted into or out the smarttoken, Price will change
        # when print info, update the _ownedvalue
        self._ownedvalue = float(self._smartToken.getPrice() * self._ownedSmartTokens + self._reserveTokens * 1)
        self._moneyBalance = self._ownedvalue - self._originalMoney
        print '------'
        print 'smartToken Name:', self._smartToken._Name, '| expected price:', self._valuation
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
        return self._valuation

    # change the expected price
    def changeExpectedPrice(self, newExpectedPrice):
        self._valuation = newExpectedPrice
        if self._valuation > self._market.getCurrentPrice() and self._reserveBalance > 0:
            # XXX issue a buy order 
            self._market.buy(self._reserveBalance)
            # XXX see how many we ended up actually buying
            # XXX deduct reserveBalance by the amount paid
            # XXX increase tokens by the number acquired
            pass
        elif self._valuation < self._market.getCurrentPrice() and self._tokenBalance > 0:
            # XXX issue a sell order
            # 
            pass
        else:
            # nothing to do
            pass

    '''
    use reserveToken to buy smartToken -> smartToken price increase
    call smartTokens.purchasing() function
    '''
    def buy(self, reserveTokenNumber):
        if reserveTokenNumber < 0:
            print '** ERROR, cannot buy negative number of smartToken'sma
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
    Alice = Customers(smartToken=KennyCoin,ownedSmartTokens=100,reserveTokens=100,valuation = 2)
    Alice.printinfo()
    Alice.buy(90.12)
    Alice.buy(101)
    Alice.buy(100)
    Alice.printinfo()
    Alice.sell(124)
    Alice.printinfo()

if __name__ == '__main__':
    cust_main()
