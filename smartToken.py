class Smartcoin(object):
	'''
	_Name: Name of Smart token
	_ReservetokenName: Name of Reserve Token
	_CRR: CRR
	_Price: the current Price of smart token
	_Supply: the number of issued smart tokens
	_ReserveBalance: the balance of the reserve pool
	'''
	def __init__(self, name='kennycoin', reservetokenName='aCoin', initCRR=0.5, initPrice=1, initIssueNum=100):
		self._Name = name
		self._ReservetokenName = reservetokenName
		self._CRR = float(initCRR)
		self._Price = float(initPrice)
		self._Supply = int(initIssueNum) # according to the white paper
		self._ReserveBalance = float(initCRR * initIssueNum)

	def printInfo(self):
		print '---------'
		print 'NAME:', self._Name, '| RESERVE NAME:', self._ReservetokenName, 'CRR:', self._CRR
		print 'PRICE:',self._Price
		print 'SUPPLY:', self._Supply, '| RESERVE BALANCE:', self._ReserveBalance

	def saveInfo(self, fw):
		fw.write('---------\n')
		fw.write('NAME: '+str(self._Name)+' | RESERVE NAME: '+str(self._ReservetokenName) + ' | CRR: '+str(self._CRR)+'\n')
		fw.write('PRICE: '+str(self._Price))
		fw.write('SUPPLY: '+str(self._Supply)+' | RESERVE BALANCE: '+str(self._ReserveBalance)+'\n')
        
	def updatePrice(self, reserveBalance, supply, CRR):
		newPrice = reserveBalance/(supply * CRR)
		return newPrice
    
	def setCRR(self, newCRR = 0.5):
		oldCRR = self._CRR
		self._CRR = newCRR
		print 'CRR', oldCRR, '->', newCRR

	def getPrice(self):
		return self._Price

	def purchasing(self, convertIntoNum=0):
		# e.g., ETH be convert into BNT, convertInto Num
		issuedtokenNum = round( self._Supply * (((self._ReserveBalance + convertIntoNum)/self._ReserveBalance)**(self._CRR) - 1) )
		self._Supply = self._Supply + issuedtokenNum
		self._ReserveBalance = self._ReserveBalance + convertIntoNum
		# update the price after purchasing, e.g. ETH convert into BNT (cust use eth to buy bnt)
		oldPrice = self._Price
		self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
		increaseRatio = (self._Price - oldPrice)/oldPrice
		return int(issuedtokenNum)

	def destroying(self, convertOutNum=0):
		# e.g., BNT be converted out to ETH, convertOutNum is BNT's num
		destroyedtokenNum = convertOutNum      
		reserveReceivedNum = round(self._ReserveBalance*(1 - ((self._Supply - convertOutNum)/self._Supply)**(1/self._CRR)))
		self._Supply = self._Supply - destroyedtokenNum
		self._ReserveBalance = self._ReserveBalance - reserveReceivedNum
		# update the price after destroying, e.g. BNT convert into ETH (cust sell bnt to get eth)
		oldPrice = self._Price
		self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
		decreaseRatio = (oldPrice-self._Price)/oldPrice
		return int(reserveReceivedNum)

def smarttoken_main():
	''' 
	This part is consistent with the example offered by white paper, 
	which shows our codes realize the idea of Bancor according to its white paper.
	'''
	BNTCoin = Smartcoin(name='BNT',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=300000)
	BNTCoin.printInfo()
	print BNTCoin.purchasing(300)
	print BNTCoin.purchasing(700)
	BNTCoin.printInfo()
	print BNTCoin.destroying(1302)
	BNTCoin.printInfo()
	print BNTCoin.purchasing(100)
	BNTCoin.printInfo()

if __name__ == '__main__':
	smarttoken_main()
