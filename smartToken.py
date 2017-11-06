class Smartcoin(object):
    '''
    _Name: Name of smart token
    _ReservetokenName: Name of reserve Token
    _CRR: CRR
    _Price: the current Price of smart token
    _Supply: the number of issued smart tokens
    _ReserveBalance: the balance of the reserve pool
    _initPrice: the initial price of smart token
    '''
    def __init__(self, name='kennycoin', reservetokenName='aCoin', initCRR=0.5, initPrice=1.0, initIssueNum=100):
        self._Name = name
        self._ReservetokenName = reservetokenName
        self._CRR = initCRR
        self._Price = initPrice
        self._Supply = float(initIssueNum)
        self._ReserveBalance = float(initCRR * initIssueNum * self._Price) 
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
    '''
    By purchasing function, reserve tokens are converted into smart tokens.
        Input: the number of reserve tokens which are going to be converted.
        Output: the number of smart tokens created.
    '''
    def purchasing(self, convertIntoNum=0):
        issuedtokenNum = round( self._Supply * (((self._ReserveBalance + convertIntoNum)/self._ReserveBalance)**(self._CRR) - 1) )
        self._Supply = self._Supply + issuedtokenNum
        self._ReserveBalance = self._ReserveBalance + convertIntoNum
        '''Update the price after purchasing'''
        oldPrice = self._Price
        self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
        increaseRatio = (self._Price - oldPrice)/oldPrice
        return int(issuedtokenNum)

    '''
    By destroying function, smart tokens are converted into reserve tokens.
        Input: the number of smart tokens which are going to be converted.
        Output: the number of reserve tokens created.
    '''
    def destroying(self, convertOutNum=0):
        destroyedtokenNum = convertOutNum
        reserveReceivedNum = round(self._ReserveBalance*(1 - ((self._Supply - convertOutNum) / self._Supply) ** (1/self._CRR)))
        self._Supply = self._Supply - destroyedtokenNum
        self._ReserveBalance = self._ReserveBalance - reserveReceivedNum
        '''Update the price after destroying'''
        oldPrice = self._Price
        self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
        decreaseRatio = (oldPrice-self._Price)/oldPrice
        return int(reserveReceivedNum)

def smarttoken_main():
    BNTCoin = Smartcoin(name='BNT',reservetokenName='ETH',initCRR=0.5, initPrice=10,initIssueNum=800000)
    BNTCoin.printInfo()
    print BNTCoin.purchasing(4000000)
    BNTCoin.printInfo()

if __name__ == '__main__':
    smarttoken_main()
