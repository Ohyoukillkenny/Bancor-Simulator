class Smartcoin(object):
    '''
    _Name: Name of Smart token
    _ReservetokenName: Name of Reserve Token
    _CRR: CRR
    _Price: the current Price of smart token
    _Supply: the number of issued smart tokens
    _ReserveBalance: the balance of the reserve pool
    '''
    def __init__(self, name='kennycoin', reservetokenName='aCoin', initCRR=0.5, initPrice=1.0, initIssueNum=100):
        self._Name = name
        self._ReservetokenName = reservetokenName
        self._CRR = initCRR
        self._Price = initPrice
        self._Supply = float(initIssueNum)
        self._ReserveBalance = float(initCRR*initIssueNum)

        # _initPrice is used to set the init Price of Market
        self._initPrice = initPrice

    def printInfo(self):
        print '---------'
        print 'NAME:', self._Name, '| RESERVE NAME:', self._ReservetokenName, 'CRR:', self._CRR
        print 'PRICE:',self._Price
        print 'SUPPLY:', int(self._Supply), '| RESERVE BALANCE:', int(self._ReserveBalance)

    def saveInfo(self, fw):
        fw.write('---------\n')
        fw.write('NAME: '+str(self._Name)+' | RESERVE NAME: '+str(self._ReservetokenName) + ' | CRR: '+str(self._CRR)+'\n')
        fw.write('PRICE: '+str(self._Price))
        fw.write('SUPPLY: '+str(self._Supply)+' | RESERVE BALANCE: '+str(self._ReserveBalance)+'\n')
        
    def getInitPrice(self):
        return self._initPrice

    def updatePrice(self, reserveBalance, supply, CRR):
        newPrice = reserveBalance / (supply * CRR)
        return newPrice
    
    def setCRR(self, newCRR = 0.5):
        oldCRR = self._CRR
        self._CRR = newCRR
        print 'CRR', oldCRR, '->', newCRR

    def getPrice(self):
        return self._Price

    def purchasing(self, convertIntoNum=0):
        # E.g., ETH be convert into BNT, convertInto Num
        issuedtokenNum = round( self._Supply * (((self._ReserveBalance + convertIntoNum)/self._ReserveBalance)**(self._CRR) - 1) )
        self._Supply = self._Supply + issuedtokenNum
        self._ReserveBalance = self._ReserveBalance + convertIntoNum
        # Update the price after purchasing, e.g. ETH is converted into BNT (cust uses eth to buy bnt)
        oldPrice = self._Price
        self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
        increaseRatio = (self._Price - oldPrice)/oldPrice
        return int(issuedtokenNum)

    def destroying(self, convertOutNum=0):
        # E.g., BNT be converted out to ETH, convertOutNum is BNT's num
        destroyedtokenNum = convertOutNum
        reserveReceivedNum = round(self._ReserveBalance*(1 - ((self._Supply - convertOutNum) / self._Supply) ** (1/self._CRR)))
        self._Supply = self._Supply - destroyedtokenNum
        self._ReserveBalance = self._ReserveBalance - reserveReceivedNum
        # Update the price after destroying, e.g. BNT is converted into ETH (cust sells bnt to get eth)
        oldPrice = self._Price
        self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
        decreaseRatio = (oldPrice-self._Price)/oldPrice
        return int(reserveReceivedNum)

def smarttoken_main():
    ''' 
    This part is consistent with the example offered by white paper, 
        which shows our codes realize the idea of Bancor according to its white paper.
    '''
    BNTCoin = Smartcoin(name='BNT',reservetokenName='ETH',initCRR=0.5, initPrice=1,initIssueNum=800000)
    BNTCoin.printInfo()
    print BNTCoin.purchasing(400000)
    BNTCoin.printInfo()
    BNTCoin.destroying(731371/2)
    print '~ ~ ~ ~ ~ ~ ~ ~ ~'
    print 365685/2 + BNTCoin.purchasing(433578/2)
    print 433578/2 + BNTCoin.destroying(365685/2)
    BNTCoin.printInfo()


if __name__ == '__main__':
    smarttoken_main()
