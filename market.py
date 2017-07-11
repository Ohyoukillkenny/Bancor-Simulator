from smartToken import *
from customers import *
class BancorMarket(object):
    def __init__(self, smartToken):
        self._smartToken = smartToken
        # Order format: (cust, transactionValue, buy_or_sell)
        self._OrderList = []
        self._CurrentPrice = smartToken.getInitPrice()
        self._timeList = []
        self._time = 0

        self._BUY = 1
        self._SELL = -1
        self._ERROR = -2

        # parameters for plotting:
        self._transactionNum = 0
        self._canceledTransactionNum = 0

    '''
    To tell market new time slot is coming, 
        and the currentPrice market offers to customers should be different from the previous one.
    '''
    def sychronize(self, timeSlot):
        self._time = timeSlot

    # what getCurrentPrice() returns in Bancor market should be different with the real time price of Smart Token. 
    # This is because since every time slot many customers come into the market simultaneously, 
    # what they see is the final price at the end of previous time slot
    def getCurrentPrice(self):
        if self._time in self._timeList:
            return self._CurrentPrice
        else:
            self._timeList.append(self._time)
            self._CurrentPrice = self._smartToken.getPrice()
            return self._CurrentPrice

    def cancelOrder(self, cust):
        # Order format: (cust, transactionValue, buy_or_sell)
        for s in range(len(self._OrderList)):
            if self._OrderList[s][0] is cust:
                self._canceledTransactionNum = self._canceledTransactionNum + 1
                _OrderList.pop(s)
                break

    def updateOrderList(self):
        s = 0
        while s < len(self._OrderList):
            if ((self._OrderList[s][2] == self._BUY) and (self._OrderList[s][0].getValuation()>=self._smartToken.getPrice()) ):
                receivedSmartTokens = self._smartToken.purchasing(self._OrderList[s][1])
                self._OrderList[s][0].changeReserveBalance(-_OrderList[s][1])
                self._OrderList[s][0].changeTokenBalance(receivedSmartTokens)
                self._OrderList.pop(s)
                s = s - 1
            elif ((self._OrderList[s][2] == self._SELL) and (self._OrderList[s][0].getValuation()<=self._smartToken.getPrice()) ):
                receivedReserveTokens = self._smartToken.destroying(self._OrderList[s][1])
                self._OrderList[s][0].changeReserveBalance(receivedReserveTokens)
                self._OrderList[s][0].changeTokenBalance(-self._OrderList[s][1])
                self._OrderList.pop(s)
                s = s - 1
            else:
                # nothing to do
                pass
            s = s + 1
    '''
    use #Transaction_Value reserveTokens to buy smartTokens -> smartToken price increase
    call smartTokens.purchasing() function
    '''
    def buy(self, cust, Transaction_Value):
        self._transactionNum = self._transactionNum + 1
        if Transaction_Value < 0:
            print '** ERROR, cannot buy with negative number of reserveToken'
        if not isinstance(Transaction_Value,int):
            print '** ERROR, should use integer number of reserveTokens to buy'
        if cust.getValuation() >= self._smartToken.getPrice():
            receivedSmartTokens = self._smartToken.purchasing(Transaction_Value)
            cust.changeReserveBalance(-Transaction_Value)
            cust.changeTokenBalance(receivedSmartTokens)
            '''
            Since the price of smart token is changed, maybe some transaction requests in orderlist is now acceptable, 
                we need to update the OrderList Now.
            '''
            self.updateOrderList()
        else:
            # add buy order into orderlist
            self._OrderList.append((cust, Transaction_Value, self._BUY))
            
        
    '''
    sell #Transaction_Value smartTokens to get reserveTokens -> smartToken price decrease
    call smartTokens.destroying() function
    '''
    def sell(self, cust, Transaction_Value):
        self._transactionNum = self._transactionNum + 1
        if Transaction_Value < 0:
            print '** ERROR, cannot sell negative number of smartToken'
        if not isinstance(Transaction_Value,int):
            print '** ERROR, should use integer number of smartTokens to sell'
        if cust.getValuation() <= self._smartToken.getPrice():
            receivedReserveTokens = self._smartToken.destroying(Transaction_Value)
            cust.changeReserveBalance(receivedReserveTokens)
            cust.changeTokenBalance(-Transaction_Value)
            '''
            Since the price of smart token is changed, maybe some transaction requests in orderlist is now acceptable, 
                we need to update the OrderList Now.
            '''
            self.updateOrderList()
        else:
            # add sell order into orderlist
            self._OrderList.append((cust, Transaction_Value, self._SELL))


    # functions for plotting
    def getTransactionNum(self):
        return self._transactionNum
        
    def getCanceledTransactionNum(self):
        return self._canceledTransactionNum



