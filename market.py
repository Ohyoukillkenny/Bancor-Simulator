from smartToken import *
from customers import *

class BancorMarket(object):
    def __init__(self, smartToken):
        self._smartToken = smartToken
        # Order format: [cust, transactionValue, buy_or_sell]
        self._OrderList = []
        self._CurrentPrice = smartToken.getInitPrice()
        self._timeList = []
        self._time = 0

        self._BUY = 1
        self._SELL = -1
        self._ERROR = -2

        # parameters for plotting: txNum and canceledTxNum are reset to 0 in the beginning of every time slot:
        self._transactionNum = 0
        self._canceledTransactionNum = 0

    '''
    To tell market new time slot is coming, 
        and the currentPrice market offers to customers should be different from the previous one.
    '''
    def sychronize(self, timeSlot):
        self._time = timeSlot
        self._transactionNum = 0
        self._canceledTransactionNum = 0

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
        # Order format: [cust, transactionValue, buy_or_sell]
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
            self._OrderList.append([cust, Transaction_Value, self._BUY])
            
        
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
            self._OrderList.append([cust, Transaction_Value, self._SELL])

    # functions for plotting
    def getTransactionNum(self):
        return self._transactionNum
        
    def getCanceledTransactionNum(self):
        return self._canceledTransactionNum



'''
Custmers give their orders to Classical Market. Market will process these orders.
Every Time customers' orders come into market, market will update the order list.
And if customers want to change their valuation, their old orders will be canceled, 
  which means the order is failed (or partially failed -- 
  A generate a sell order of 100 tokens, he successfully sells 50, but still 50 remaining in orderlist)
In Classical Market, the price of smart token will not change.
'''
class ClassicalMarket(object):
    def __init__(self, smartToken):
        self._smartToken = smartToken
        # Order format: [cust, transactionValue, buy_or_sell]
        self._OrderList = []
        self._CurrentPrice = smartToken.getInitPrice()

        self._BUY = 1
        self._SELL = -1
        self._ERROR = -2

        # parameters for plotting:
        self._transactionNum = 0
        self._canceledTransactionNum = 0
        self._totallyFailedTransationNum = 0
        self._ChangedOrderList = []


    '''
    Reset plotting parameters.
    '''
    def sychronize(self, timeSlot = 0):
        self._time = timeSlot
        self._transactionNum = 0
        self._canceledTransactionNum = 0
        self._totallyFailedTransationNum = 0

    def getCurrentPrice(self):
        return self._CurrentPrice

    def cancelOrder(self, cust):
        # Order format: [cust, transactionValue, buy_or_sell]
        for s in range(len(self._OrderList)):
            if self._OrderList[s][0] is cust:
                self._canceledTransactionNum = self._canceledTransactionNum + 1
                if cust not in self._ChangedOrderList:
                    self._totallyFailedTransationNum = self._totallyFailedTransationNum + 1
                else:
                    self._ChangedOrderList.pop(self._ChangedOrderList.index(cust))
                self._OrderList.pop(s)
                break

    def updateOrderList(self, newOrder):
        cust = newOrder[0]
        custValuation = cust.getValuation()
        transactionValue =  newOrder[1]
        buy_or_sell = newOrder[2]

        s = 0
        while s < len(self._OrderList):
            if buy_or_sell == self._BUY:
                if self._OrderList[s][2] == self._SELL and custValuation >= self._OrderList[s][0].getValuation():
                    # sellerMaxTrxValue: the max reservetokens' number the seller could offer with his order
                    sellerMaxTrxValue = int(self._OrderList[s][1] * self._CurrentPrice)
                    if transactionValue < sellerMaxTrxValue:
                        cust.changeReserveBalance(-transactionValue)
                        cust.changeTokenBalance(int(transactionValue/self._CurrentPrice))
                        self._OrderList[s][0].changeReserveBalance(transactionValue)
                        self._OrderList[s][0].changeTokenBalance(-int(transactionValue/self._CurrentPrice))
                        # update the order's info in the orderlist
                        self._OrderList[s][1] = self._OrderList[s][1] - int(transactionValue/self._CurrentPrice)
                        self._ChangedOrderList.append(self._OrderList[s][0])
                        break
                    else:
                        # buy all seller's smarttokens and then try to buy another sellers' smarttokens
                        cust.changeReserveBalance(-sellerMaxTrxValue)
                        cust.changeTokenBalance(self._OrderList[s][1])
                        transactionValue = transactionValue - sellerMaxTrxValue
                        self._OrderList[s][0].changeReserveBalance(sellerMaxTrxValue)
                        self._OrderList[s][0].changeTokenBalance(-self._OrderList[s][1])
                        # clear seller's sell order in the list
                        self._OrderList.pop(s)
                        s = s - 1
            else:
                # buy_or_sell == self._SELL
                if self._OrderList[s][2] == self._BUY and custValuation <= self._OrderList[s][0].getValuation():
                    # buyerMaxTrxValue: the max smarttokens' number the buyer can buy with the his order
                    buyerMaxTrxValue = int(self._OrderList[s][1] / self._CurrentPrice)
                    if transactionValue < buyerMaxTrxValue:
                        cust.changeReserveBalance(int(transactionValue * self._CurrentPrice))
                        cust.changeTokenBalance(-transactionValue)
                        self._OrderList[s][0].changeReserveBalance(-int(transactionValue * self._CurrentPrice))
                        self._OrderList[s][0].changeTokenBalance(transactionValue)
                        # update the order's info in the orderlist
                        self._OrderList[s][1] = self._OrderList[s][1] - int(transactionValue * self._CurrentPrice)
                        self._ChangedOrderList.append(self._OrderList[s][0])
                        break
                    else:
                        cust.changeReserveBalance(self._OrderList[s][1])
                        cust.changeTokenBalance(-buyerMaxTrxValue)
                        transactionValue = transactionValue - buyerMaxTrxValue
                        self._OrderList[s][0].changeReserveBalance(-self._OrderList[s][1])
                        self._OrderList[s][0].changeTokenBalance(buyerMaxTrxValue)
                        # clear buyer's buy order in the list
                        self._OrderList.pop(s)
                        s = s - 1
            s = s + 1
        if transactionValue > 0:
            newOrder[1] = transactionValue
            self._OrderList.append(newOrder)

    '''
    use #Transaction_Value reserveTokens to buy smartTokens -> smartToken price increase
    call smartTokens.purchasing() function
    '''
    def buy(self, cust, Transaction_Value):
        self.updateOrderList([cust, Transaction_Value, self._BUY])
        
    '''
    sell #Transaction_Value smartTokens to get reserveTokens -> smartToken price decrease
    call smartTokens.destroying() function
    '''
    def sell(self, cust, Transaction_Value):
        self.updateOrderList([cust, Transaction_Value, self._SELL])

    # functions for plotting
    def getTransactionNum(self):
        return self._transactionNum
        
    def getCanceledTransactionNum(self):
        return self._canceledTransactionNum

    def getTotallyFailedTransactionNum(self):
        return self._totallyFailedTransationNum
