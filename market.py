from smartToken import *
from customers import *

class Market(object):
    def __init__(self):
        self._buyers = {}
        self._sellers = {}
        # smaller order, higher priviledge
        self._buyerOrder = 0
        self._sellerOrder = 0

    def addBuyer(self, Joe):
        self._buyers[Joe] = self._buyerOrder
        self._buyerOrder = self._buyerOrder + 1

    def addSeller(self, Joe):
        self._sellers[Joe] = self._sellerOrder
        self._sellerOrder = self._sellerOrder + 1

    def removeBuyer(self, Joe):
        if Joe in self._buyers:
            del self._buyers[Joe]
        else:
            print '** ERROR, customer is not in the buyer list'
            return

    def removeSeller(self, Joe):
        if Joe in self._sellers:
            del self._sellers[Joe]
        else:
            print '** ERROR, customer is not in the seller list'
            return

    def getBuyers(self):
        return self._buyers

    def getSellers(self):
        return self._sellers
