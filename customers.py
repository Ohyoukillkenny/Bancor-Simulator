from smartToken import *
from market import *

class Customer(object):
    '''
    _smartToken: class of the token customers want to buy or sell -- SmartToken()
    _market: instance of the market customers buy or sell 
    _tokenBalance: number of smart tokens a customer has
    _reserveBalance: number of reserve tokens a customer has
    _valuation: how much money customers are willing to finish the transaction
    _originalCash: original money cust has
    _cash: net profit or loss to date
    '''
    def __init__(self, smartToken, market ,tokenBalance = 0, reserveBalance = 0, valuation = 0.0):
        self._smartToken = smartToken
        self._market = market
        self._tokenBalance = tokenBalance
        self._reserveBalance = reserveBalance
        self._originalCash = float(self._reserveBalance + self._tokenBalance * self._smartToken.getPrice())
        self._cash = 0.0
        self._valuation = valuation

        self._BUY = 1
        self._SELL = -1

    def printInfo(self):
        currentCash = float(self._smartToken.getPrice() * self._tokenBalance + self._reserveBalance)
        self._cash = currentCash - self._originalCash
        print '------'
        print 'smartToken Name:', self._smartToken._Name, '| valuation:', self._valuation
        print 'reserveBalance:', self._reserveBalance, '| tokenBalance:', self._tokenBalance

    def getReserveBalance(self):
        return self._reserveBalance

    def changeReserveBalance(self, changeValue):
        self._reserveBalance = self._reserveBalance + changeValue

    def getTokenBalance(self):
        return self._tokenBalance

    def changeTokenBalance(self, changeValue):
        self._tokenBalance = self._tokenBalance + changeValue

    def getCash(self):
        currentCash = float(self._smartToken.getPrice() * self._tokenBalance + self._reserveBalance)
        self._cash = currentCash - self._originalCash
        return self._cash

    def getValuation(self):
        return self._valuation

    '''
    If customer has a new valuation, he will generate a new transaction request, 
    and market will give responce for this request.
    Therefore, in main function, we can call cust.changeValuation(newValuation, currentMarketPrice) to try to launch orders.
    '''
    def changeValuation(self, newValuation, marketPrice):
        self._valuation = newValuation
        '''
        In Bancor Market, cancelOrder function means no extra operation, and always return True.
            as the order launched by customer will be finished or passed for changing properties of Bancor market.
        While in Classic Market, cancelOrder means
        '''
        if self._market.ifFinishedOrder(self):
            '''
            What getCurrentPrice() returns in Bancor market should be different with the real time price of Smart Token. 
            This is because since every time slot many customers come into the market simultaneously, 
                what they see is the final price at the end of previous time slot.
            '''
            if self._valuation > marketPrice and self._reserveBalance > 0:
                # XXX issues a buy order 
                self._market.buy(self, self._reserveBalance) 
            elif self._valuation < marketPrice and self._tokenBalance > 0:
                # XXX issue a sell order
                self._market.sell(self, self._tokenBalance) 
            else:
                # nothing to do
                pass

        else:
            # nothing to do, since the order is remained in Classic Market without being touched.
            pass

def cust_main():
    
    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.2, initPrice=1.0, initIssueNum=300000)
    
    # test for Bancor Market
    # market1 = BancorMarket(smartToken = KennyCoin)
    # Alice = Customer(smartToken=KennyCoin, market=market1, tokenBalance=200, reserveBalance=100)
    # market1.sychronize(0)
    # Alice.printInfo()
    # Alice.changeValuation(1.5)
    # Alice.printInfo()
    # KennyCoin.printInfo()
    # Alice.changeValuation(0.9)
    # Alice.printInfo()
    # KennyCoin.printInfo()
    # print market1.getCanceledTransactionNum() , 'being canceled.'

    # test for Classic Market
    market2 = ClassicMarket(smartToken = KennyCoin)
    Alice = Customer(smartToken=KennyCoin, market=market2, tokenBalance=200, reserveBalance=100)
    Bob = Customer(smartToken=KennyCoin, market=market2, tokenBalance=305, reserveBalance=333)
    Alice.changeValuation(1.5)
    Alice.printInfo()
    Bob.changeValuation(1.6)
    Bob.changeValuation(0.7)
    Alice.printInfo()
    Bob.printInfo()
    Alice.changeValuation(1.4)

if __name__ == '__main__':
    cust_main()
