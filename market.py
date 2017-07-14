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
                self._OrderList.pop(s)
                break
    '''
    Becuase in Bancor Market, after every transaction, the price of smart token will be changed.
    Update the orderlist by recursion after every time transaction being made is too time-comsuming.
    Here, we just scan the orderlist once if the price being changed. 
        E.g., every time the price of token changes, we will sequence through the orderlist to see whether some orders can be satisfied.
    And this method offers almost same accuracy with recursion function.
    '''
    def updateOrderList(self):
        s = 0
        while s < len(self._OrderList):
            if ((self._OrderList[s][2] == self._BUY) and (self._OrderList[s][0].getValuation()>=self._smartToken.getPrice()) ):
                receivedSmartTokens = self._smartToken.purchasing(self._OrderList[s][1])
                self._OrderList[s][0].changeReserveBalance(-self._OrderList[s][1])
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
            print '** ERROR, should use integer number of reserveTokens to buy', Transaction_Value
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
            print '** ERROR, should use integer number of smartTokens to sell', Transaction_Value
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
Once customers' orders come into market, market will update the order list.
And if customers want to change their valuation, their old orders will be canceled, 
  which means the order is failed (or partially failed -- 
  e.g. Customer XXX generates a sell order of 100 tokens, he successfully sells 50, but still 50 remaining in orderlist)
In Classical Market, the price of smart token will not change, but the customers' valuations will change.
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
        self._totallyFailedTransactionNum = 0
        self._ChangedOrderList = []


    '''
    Reset plotting parameters.
    '''
    def sychronize(self, timeSlot = 0):
        self._transactionNum = 0
        self._canceledTransactionNum = 0
        self._totallyFailedTransactionNum = 0

    def getCurrentPrice(self):
        return self._CurrentPrice

    def cancelOrder(self, cust):
        # Order format: [cust, transactionValue, buy_or_sell]
        for s in range(len(self._OrderList)):
            if self._OrderList[s][0] is cust:
                self._canceledTransactionNum = self._canceledTransactionNum + 1
                if cust not in self._ChangedOrderList:
                    self._totallyFailedTransactionNum = self._totallyFailedTransactionNum + 1
                else:
                    # Since the order will be canceled, the customer should be removed from ChangedOrderList.
                    self._ChangedOrderList.pop(self._ChangedOrderList.index(cust))
                self._OrderList.pop(s)
                break

    def updateOrderList(self, newOrder):
        cust = newOrder[0]
        custValuation = cust.getValuation()
        transactionValue =  newOrder[1]
        buy_or_sell = newOrder[2]

        # If the orderlist is empty, just add the new order into list
        if len(self._OrderList) == 0:
            self._OrderList.append(newOrder)
            return
        '''
        Buyer comes into the market, scan the market seller, find sellers who offers the valuation smaller than his valuation:
            If none of the sellers offers smaller valuation, push new order into list, return
            If there do exist some sellers, save [seller's valuation, seller, seller's index in orderList] into a seller list, 
            and sorted by sellers' valuations from small to large. 
            Then, buyer will try to make transaction with the seller in list one by one:
            Loop:
                if the buyer's demand can be satisfied by seller:
                    update the buyer's info in customer class,
                    update the seller's info in customer class, 
                    update the seller's info in order list. 
                    return
                if the buyer's demand can not be fully satisfied by seller:
                    update the buyer's info in customer class,
                    decrease buyer's demand
                    update the seller's info in customer class,
                    pop the seller out of order list
                    update other sellers in seller list's index info since one seller is poped out of orderlist 
            if buyer's demand still > 0:
                push buyer's remaining demand into order list
            else:
                just return, since the buyer's demand is satisfied by transaction

        Same thing goes with seller. But for seller, the buyer list should be sorted from high valuation to low valuation
        '''
        sellerList = []
        buyerList = []
        if buy_or_sell == self._BUY:
            for s in range(len(self._OrderList)):
                if self._OrderList[s][2] == self._SELL and custValuation >= self._OrderList[s][0].getValuation():
                    sellerValuation = self._OrderList[s][0].getValuation()
                    seller = self._OrderList[s][0]
                    # sellerList format: [valuation, seller, index of seller in orderList]
                    sellerList.append([sellerValuation,seller,s])

            if len(sellerList) == 0:
                self._OrderList.append(newOrder)
                return
            else:
                sorted(sellerList, key=lambda sellerOrders: sellerOrders[0]) # sorted from low to high

            for t in range(len(sellerList)):
                sellerValuation = sellerList[t][0]
                seller = sellerList[t][1]
                indexInOrderList = sellerList[t][2]
                sellerMaxCouldSatisfy = int(self._OrderList[indexInOrderList][1] * sellerValuation)
                if transactionValue < sellerMaxCouldSatisfy:
                    cust.changeReserveBalance(-transactionValue)
                    cust.changeTokenBalance(int(transactionValue/sellerValuation))
                    seller.changeReserveBalance(transactionValue)
                    seller.changeTokenBalance(-int(transactionValue/sellerValuation))
                    self._OrderList[indexInOrderList][1] -= int(transactionValue/sellerValuation)
                    if seller not in self._ChangedOrderList:
                        # to count whether cust's order is totally failed
                        self._ChangedOrderList.append(seller)
                    break # cust's order is satisfied
                else: 
                # seller cannot satisfy buyer's need, transactionValue >= sellerMaxCouldSatisfy
                    cust.changeReserveBalance(-sellerMaxCouldSatisfy)
                    cust.changeTokenBalance(self._OrderList[indexInOrderList][1])
                    transactionValue -= sellerMaxCouldSatisfy
                    seller.changeReserveBalance(sellerMaxCouldSatisfy)
                    seller.changeTokenBalance(-self._OrderList[indexInOrderList][1])
                    self._OrderList.pop(indexInOrderList)
                    for item in sellerList:
                        if item[2] > indexInOrderList:
                            # update index info, since one seller is poped out from orderList
                            item[2] -= 1

            if transactionValue < 0:
                print '** Error, buyer buys too much in market class'
            elif transactionValue == 0:
                return
            else:
                # transactionValue > 0
                newOrder[1] = transactionValue
                self._OrderList.append(newOrder)
        else:
            # buy_or_sell == self._SELL
            for s in range(len(self._OrderList)):
                if self._OrderList[s][2] == self._BUY and custValuation <= self._OrderList[s][0].getValuation():
                    buyerValuation = self._OrderList[s][0].getValuation()
                    buyer = self._OrderList[s][0]
                    # buyerList format: [valuation, buyer, index of buyer in orderList]
                    buyerList.append([buyerValuation,buyer,s])

            if len(buyerList) == 0:
                self._OrderList.append(newOrder)
                return
            else:
                # sorted from high to low
                sorted(sellerList, key=lambda sellerOrders: sellerOrders[0], reverse=True) 

            for t in range(len(buyerList)):
                buyerValuation = buyerList[t][0]
                buyer = buyerList[t][1]
                indexInOrderList = buyerList[t][2]
                buyerMaxCouldBuy = int(self._OrderList[indexInOrderList][1] / buyerValuation)
                if transactionValue < buyerMaxCouldBuy:
                    cust.changeReserveBalance(int(transactionValue * buyerValuation))
                    cust.changeTokenBalance(-transactionValue)
                    buyer.changeReserveBalance(-int(transactionValue * buyerValuation))
                    buyer.changeTokenBalance(transactionValue)
                    self._OrderList[indexInOrderList][1] -= int(transactionValue * buyerValuation)
                    if buyer not in self._ChangedOrderList:
                        # to count whether cust's order is totally failed
                        self._ChangedOrderList.append(buyer)
                    break # cust's order is satisfied
                else:
                    # buyer cannot satisfy the seller's need, transactionValue >= buyerMaxCouldBuy
                    cust.changeReserveBalance(self._OrderList[indexInOrderList][1])
                    cust.changeTokenBalance(-buyerMaxCouldBuy)
                    transactionValue -= buyerMaxCouldBuy
                    buyer.changeReserveBalance(-self._OrderList[indexInOrderList][1])
                    buyer.changeTokenBalance(buyerMaxCouldBuy)
                    self._OrderList.pop(indexInOrderList)
                    for item in buyerList:
                        if item[2] > indexInOrderList:
                            # update index info, since one buyer is poped out from orderList
                            item[2] -= 1 

            if transactionValue < 0:
                print '** Error, Seller sells too much in market class'
            elif transactionValue == 0:
                return
            else:
                # transactionValue > 0
                newOrder[1] = transactionValue
                self._OrderList.append(newOrder)

    '''
    use #Transaction_Value reserveTokens to buy smartTokens -> smartToken price increase
    call smartTokens.purchasing() function
    '''
    def buy(self, cust, Transaction_Value):
        self.updateOrderList([cust, Transaction_Value, self._BUY])
        self._transactionNum = self._transactionNum + 1
        
    '''
    sell #Transaction_Value smartTokens to get reserveTokens -> smartToken price decrease
    call smartTokens.destroying() function
    '''
    def sell(self, cust, Transaction_Value):
        self.updateOrderList([cust, Transaction_Value, self._SELL])
        self._transactionNum = self._transactionNum + 1

    # functions for plotting
    def getTransactionNum(self):
        return self._transactionNum
        
    def getCanceledTransactionNum(self):
        return self._canceledTransactionNum

    def getTotallyFailedTransactionNum(self):
        return self._totallyFailedTransactionNum
