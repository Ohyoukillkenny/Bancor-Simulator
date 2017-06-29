# here, coin number is saved as float (complying with code from github, while contradicts white paper)
class Smartcoin(object):
	def __init__(self, name='kennycoin', reservetokenName='aCoin', initCRR=0.5, initPrice=1, initIssueNum=100):
		self._Name = name
		self._ReservetokenName = reservetokenName
		self._CRR = float(initCRR)
		self._Price = float(initPrice)
		self._Supply = float(initIssueNum)
		self._ReserveBalance = float(initCRR * initIssueNum)
		self._budget = float(0)

	def printInfo(self):
		print '---------'
		print 'NAME:', self._Name, '| RESERVE NAME:', self._ReservetokenName, 'CRR:', self._CRR
		print 'PRICE:',self._Price
		print 'SUPPLY:', self._Supply, '| RESERVE BALANCE:', self._ReserveBalance
		print 'BUDGET:', self._budget

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
		issuedtokenNum = self._Supply * (((self._ReserveBalance + convertIntoNum)/self._ReserveBalance)**(self._CRR) - 1)
		self._Supply = self._Supply + issuedtokenNum
		self._ReserveBalance = self._ReserveBalance + convertIntoNum
		oldPrice = self._Price
		self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
		increaseRatio = (self._Price - oldPrice)/oldPrice
		print '*********'
		print convertIntoNum, self._ReservetokenName+" convert into "+self._Name
		print "Current prize of "+self._Name+" is", self._Price, "with", increaseRatio, "increasing."
		self._budget = self._budget + self._Price*self._Supply - oldPrice*(self._Supply - issuedtokenNum)

	def destroying(self, convertOutNum=0):
		destroyedtokenNum = self._Supply * (1 - ((self._ReserveBalance - convertOutNum)/self._ReserveBalance)**(self._CRR))
		self._Supply = self._Supply - destroyedtokenNum
		self._ReserveBalance = self._ReserveBalance - convertOutNum
		oldPrice = self._Price
		self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
		decreaseRatio = (oldPrice-self._Price)/oldPrice
		print '*********'
		print convertOutNum, self._ReservetokenName+" convert out from "+self._Name
		print "Current prize of "+self._Name+" is", self._Price, "with", decreaseRatio, "decreasing."
		self._budget = self._budget + self._Price*self._Supply - oldPrice*(self._Supply + destroyedtokenNum)

def smarttoken_main():
	''' 
	This part is consistent with the example offered by white paper, 
	which shows our codes realize the idea of Bancor according to its white paper.
	'''
	BNTCoin = Smartcoin(name='BNT',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=300000)
	BNTCoin.printInfo()
	BNTCoin.purchasing(300)
	BNTCoin.printInfo()
	BNTCoin.purchasing(700)
	BNTCoin.printInfo()
	BNTCoin.destroying(1308)
	BNTCoin.printInfo()
	BNTCoin.purchasing(100)
	BNTCoin.printInfo()

if __name__ == '__main__':
	smarttoken_main()






