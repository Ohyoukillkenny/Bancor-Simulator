from smartToken import *
from customers import *

class BancorMarket(object):
    def __init__(self, smartToken):
        self._smartToken = smartToken
        '''Order format: [cust, transactionValue, buy_or_sell label]'''
        self._OrderList = []

        '''_Buy and _SELL are labels to distinguish buy orders and sell orders'''
        self._BUY = 1
        self._SELL = -1

        '''parameters for plotting: txNum and canceledTxNum are reset to 0 in the beginning of every time slot:'''
        self._transactionNum = 0
        self._canceledTransactionNum = 0

    '''
    sychronize function resets _transactionNum and _canceledTransactionNum to 0
    '''
    def sychronize(self):
        self._transactionNum = 0
        self._canceledTransactionNum = 0

    '''
    By Bancor Market's property, every launched order, which is not canceled by customer, can be finished by market.
    '''
    def ifFinishedOrder(self, cust):
        return True

    '''
    Use reserveTokens with the number of Transaction_Value to buy smartTokens.
    '''
    def buy(self, cust, Transaction_Value):
        self._transactionNum = self._transactionNum + 1
        if Transaction_Value < 0:
            print '** ERROR, cannot buy with negative number of reserveToken'
        if not isinstance(Transaction_Value, int):
            print '** ERROR, should use integer number of reserveTokens to buy', Transaction_Value
        if cust.getValuation() >= self._smartToken.getPrice():
            receivedSmartTokens = self._smartToken.purchasing(Transaction_Value)
            cust.changeReserveBalance(-Transaction_Value)
            cust.changeTokenBalance(receivedSmartTokens)
        else:
            # This order will be canceled, no extra operation.
            self._canceledTransactionNum += 1
            
        
    '''
    Sell smartTokens with the number of Transaction_Value to get reserveTokens.
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
        else:
            # This order will be canceled, no extra operation.
            self._canceledTransactionNum += 1

    # functions for statistic analysis
    def getTransactionNum(self):
        return self._transactionNum
    def getCanceledTransactionNum(self):
        return self._canceledTransactionNum



'''
Custmers give their orders to Classic Market. Market will process these orders.
Once customers' orders come into market, market will update the order list.
And if customers want to change their valuation, their old orders will be canceled, 
  which means the order is failed (or partially failed -- 
  e.g. Customer XXX generates a sell order of 100 tokens, he successfully sells 50, but still 50 remaining in orderlist)
In Classic Market, the price of smart token will not change, but the customers' valuations will change.
'''
class ClassicMarket(object):
    def __init__(self, smartToken):
        self._smartToken = smartToken
        '''Order format: [cust, transactionValue, buy_or_sell label]'''
        self._OrderList = []

        '''_Buy and _SELL are labels to distinguish buy orders and sell orders'''
        self._BUY = 1
        self._SELL = -1

        '''Parameters for plotting'''
        self._transactionNum = 0

        '''Order format: [cust], record the orders being partially satisfied'''
        self._ChangedOrderList = []


    '''
    sychronize function resets _transactionNum and _canceledTransactionNum to 0
    '''
    def sychronize(self):
        self._transactionNum = 0

    '''
    In classic market, customers transaction orders might be only partially fulfilled. 
    We can call this "ifFinishedOrder" to see whether a certain customer's transaction order being fulfilled by market.
    '''
    def ifFinishedOrder(self, cust):
        for i in range(len(self._OrderList)):
            # Order format: [cust, transactionValue, buy_or_sell]
            if cust is self._OrderList[i][0]:
                return False
        '''if the cust's order is not in the orderlist, return True'''        
        return True

    def updateOrderList(self, newOrder):
        '''newOrder: [cust, transactionValue, buy_or_sell]'''
        cust = newOrder[0]
        custValuation = cust.getValuation()
        transactionValue =  newOrder[1]
        buy_or_sell = newOrder[2]

        # If the orderlist is empty, just add the new order into list.
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
                if the buyer's demand can be satisfied by sellers:
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
                sellerList = sorted(sellerList, key=lambda sellerOrders: sellerOrders[0]) # sorted from low to high

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
                    transactionValue -= transactionValue # i.e. transactionValue = 0
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
                    if seller in self._ChangedOrderList:
                        # remove it as it is completed
                        self._ChangedOrderList.remove(seller)

            if transactionValue < 0:
                print '** Error, buyer buys too much in market class'
            elif transactionValue == 0:
                return
            else:
                if transactionValue < newOrder[1]:
                    self._ChangedOrderList.append(newOrder[0])
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
                buyerList = sorted(buyerList, key=lambda buyerOrders: buyerOrders[0], reverse=True)

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
                    transactionValue -= transactionValue # i.e. transactionValue = 0
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
                    if buyer in self._ChangedOrderList:
                        self._ChangedOrderList.remove(buyer)

            if transactionValue < 0:
                print '** Error, Seller sells too much in market class'
            elif transactionValue == 0:
                return
            else:
                if transactionValue < newOrder[1]:
                    self._ChangedOrderList.append(newOrder[0])
                newOrder[1] = transactionValue
                self._OrderList.append(newOrder)

    '''
    Use reserveTokens with the number of Transaction_Value to buy smartTokens.
    '''
    def buy(self, cust, Transaction_Value):
        if Transaction_Value < 0:
            print '** ERROR, cannot sell negative number of smartToken'
            return
        if not isinstance(Transaction_Value,int):
            print '** ERROR, should use integer number of smartTokens to sell', Transaction_Value
            return
        self.updateOrderList([cust, Transaction_Value, self._BUY])
        self._transactionNum = self._transactionNum + 1
        
    '''
    Sell smartTokens with the number of Transaction_Value to get reserveTokens.
    '''
    def sell(self, cust, Transaction_Value):
        if Transaction_Value < 0:
            print '** ERROR, cannot sell negative number of smartToken'
            return
        if not isinstance(Transaction_Value,int):
            print '** ERROR, should use integer number of smartTokens to sell', Transaction_Value
            return
        self.updateOrderList([cust, Transaction_Value, self._SELL])
        self._transactionNum = self._transactionNum + 1

    # functions for statistic analysis
    def getTransactionNum(self):
        return self._transactionNum
    def getCanceledTransactionNum(self):
        return len(self._OrderList)
    def getTotallyFailedTransactionNum(self):
        return len(self._OrderList) - len(self._ChangedOrderList)
