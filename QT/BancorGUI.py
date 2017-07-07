#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui, QtCore
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
fw = open('Transaction-Record.txt','w')

def MarketSimulating(_timeRound, _custNum, _custOriginalReserve, _custOriginalSmartTokens, _sigma):
    # issue a new smart token
    initIssue = 20000000
    CRR = 0.2
    initTransaction = initIssue * (1-CRR)
    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=initIssue)

    '''
    init properties: 
    We have #TimeRound round,
    In each time round, #custNum customers come in, 
       with original reserve: #custOriginalReserve
       with original smarttokens: #custOriginalSmartTokens
    '''
    TimeRound = _timeRound
    custNum = _custNum
    custOriginalReserve = _custOriginalReserve
    custOriginalSmartTokens = _custOriginalSmartTokens
    sigma = _sigma

    if TimeRound * custOriginalSmartTokens > initTransaction:
        print 'WARNING, too many init smart tokens from customers'

    # PriceTracker records the change of the price
    PriceTracker = []
    # failedTracker records the transaction failure
    failedBuy_rateTracker = []
    failedSell_rateTracker = []
    failed_rateTracker = []

    alpha = 50 # 50% to buy, 50% to sell
    j=0
    while j < TimeRound:
        # failed num denotes the number of transactions failed in each time round
        failed_num = 0
        failed_buyNum = 0
        failed_sellNum = 0
        buyNum = 0
        sellNum = 0        
        i=0
        custlist = []
        CurrentPrice = KennyCoin.getPrice()
        # set the expectation of initPrice (first we fix it), Should it change with time ?
        initPrice = CurrentPrice
        ''' 
        First, we initialize the customers who come in at #j TimeRound.
        We assume in each TimeRound, #custNum customers come in, whose number is gaussian distributed with custExpectedPrice
        We assume when price is mu -- initPrice, customers' number is the largest
        Since we get customers #custNum involved, the normal should be sampled by custNum.
        '''
        mu = initPrice
        custExpectedPrice = np.random.normal(mu, sigma, custNum)
        while i < custNum:
    #         # the customer's expected price should not lower than the currentPrice since every one want to achieve the transaction
    #         if custExpectedPrice[i] <= CurrentPrice:
    #             np.random.seed(0)
    #             change_delta = random.uniform(0,0.001)
    #             custExpectedPrice[i] = CurrentPrice * (1 + change_delta)
            # create Joe who is the customer who want to hold KennyCoin, with expected Buy and Sell Price custExpectedPrice
            Joe = Customers(smartToken = KennyCoin, ownedSmartTokens = custOriginalSmartTokens, reserveValue = custOriginalReserve, expectedPrice = custExpectedPrice[i])
            custlist.append(Joe)
            i = i + 1
        for Joe in custlist:
            # uses seed to let the purchase or sell happen randomly by a certain ratio
            seed = random.randint(0, 100)
            if seed < alpha:
                buyNum = buyNum + 1
                if Joe.getExpectedPrice() >= KennyCoin.getPrice():
                    # Joe is purchasing
                    custReserve = Joe.getReserveValue()
                    randomBuy = random.uniform(0,custReserve)
                    Joe.purchase(reserveTokenNumber = randomBuy)
                else:
                    '''
                    Customers are smart, and already know the price.
                    No one will expect price lower than the standard prize?
                    Here this situation is simulated in BancorGUI-noAlpha.py
                    '''
                    failed_buyNum = failed_buyNum + 1
                    
            else:
                sellNum = sellNum + 1
                if Joe.getExpectedPrice() <= KennyCoin.getPrice():
                    # Joe is selling
                    custSmartToken_Num = Joe.getownedSmartToken()
                    randomSell = random.uniform(0,custSmartToken_Num)
                    Joe.destroy(smartTokenNumber = randomSell)
                else:
                    failed_sellNum = failed_sellNum + 1
            CurrentPrice = KennyCoin.getPrice()
            PriceTracker.append((CurrentPrice,j))
        print 'The',j,'round, BuyNum:',buyNum,'SellNum:',sellNum
        failed_num = failed_buyNum + failed_sellNum
        failedBuy_rateTracker.append((float(failed_buyNum) / buyNum , j))
        failedSell_rateTracker.append((float(failed_sellNum) / sellNum , j))
        failed_rateTracker.append((float(failed_num) / (buyNum+sellNum) , j))
        fw.write('After Round '+ str(j) + '\n')
        KennyCoin.saveInfo(fw)
        j = j + 1
    # fw.close()

    # draw failure rate fig
    j = 0
    failedBuyRate = []
    failedSellRate = []
    failedRate = []
    myX = []
    while j < TimeRound:
        myX.append(j)
        failedRate.append(failed_rateTracker[j][0])
        failedBuyRate.append(failedBuy_rateTracker[j][0])
        failedSellRate.append(failedSell_rateTracker[j][0])
        j = j + 1
    x = np.asarray(myX)
    y1 = np.asarray(failedRate)
    y2 = np.asarray(failedBuyRate)
    y3 = np.asarray(failedSellRate)
    plt.plot(x,y1,'o-',color = 'navy',alpha = 0.8)
    plt.title('Failure Rate Change For All Rounds',fontsize = 25)
    plt.xlabel('Round #',fontsize = 15)
    plt.ylabel('Failure Rate of Transaction', fontsize = 15)
    plt.savefig('Failure/FailureRate-All.png', bbox_inches='tight')
    plt.close()
    plt.plot(x,y2,'o-',color = 'navy',alpha = 0.8)
    plt.title('Buy Failure Rate Change For All Rounds',fontsize = 25)
    plt.xlabel('Round #',fontsize = 15)
    plt.ylabel('Failure Rate of Buy Transaction', fontsize = 15)
    plt.savefig('Failure/FailureRate-Buy.png', bbox_inches='tight')
    plt.close()
    plt.plot(x,y3,'o-',color = 'navy',alpha = 0.8)
    plt.title('Sell Failure Rate Change For All Rounds',fontsize = 25)
    plt.xlabel('Round #',fontsize = 15)
    plt.ylabel('Failure Rate of Sell Transaction', fontsize = 15)
    plt.savefig('Failure/FailureRate-Sell.png', bbox_inches='tight')
    plt.close()

    # draw price change fig
    j = 0
    PriceAllRound = []
    my_Xall = []
    while j < TimeRound:
        myX = []
        Price_eachRound = []
        i = 0
        while i < custNum:
            myX.append(i+1)
            Price_eachRound.append(PriceTracker[i+j*custNum][0])
            i = i + 1
        PriceAllRound.append(Price_eachRound[custNum-1])
        if _timeRound <= 150:
            x = np.asarray(myX)
            y = np.asarray(Price_eachRound)
            plt.plot(x,y,'o-',color = 'navy',alpha = 0.8)
            plt.title('Price Change in Round \"'+str(j)+'\"',fontsize = 25)
            plt.xlabel('Customer #',fontsize = 15)
            plt.ylabel('Price of Smart Token', fontsize = 15)
            plt.savefig('Price/PriceRound/Price_inRound'+str(j)+'.png', bbox_inches='tight')
            plt.close()
            print 'Price Change Fig, Round '+str(j)+' Over...'
        my_Xall.append(j)
        j = j + 1
    allX = np.asarray(my_Xall)
    ally = np.asarray(PriceAllRound)
    plt.plot(allX,ally,'o-',color = 'navy',alpha = 0.8)
    plt.title('Price Change For All Round',fontsize = 25)
    plt.xlabel('Round #',fontsize = 15)
    plt.ylabel('Price of Smart Token', fontsize = 15)
    plt.savefig('Price/Price_Change.png', bbox_inches='tight')
    plt.close()
    return

class Customers(object):
    def __init__(self, smartToken, ownedSmartTokens = float(0), reserveValue = float(500),expectedPrice = 0):
        # _smartToken is the token customers want to buy -- SmartToken()
        self._smartToken = smartToken
        # _ownedSmartToken refers to smart token's number customers have
        self._ownedSmartToken = float(ownedSmartTokens)
        # _smartValue is the value of ownedSmartTokens -- currentPrice * owned#
        self._smartValue = smartToken.getPrice() * ownedSmartTokens
        self._reserveValue = float(reserveValue)
        # _ownedvalue = _reserveValue + _smartValue
        self._ownedvalue = float(reserveValue)
        # gain or lose money comparing to the original state
        self._budget = float(0)
        # expectedPrice denotes the how much money customers are willing to finish the transaction 
        self._expectedPrice = expectedPrice
        
    def printinfo(self):
        # since new reserve will be converted into or out the kenny coin, the budget could change
        # when print info, update the budget
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._smartToken._Price * self._ownedSmartToken + self._reserveValue
        self._budget = self._budget + self._ownedvalue - oldownedValue
        print '------'
        print 'smartToken Name:', self._smartToken._Name
        print 'ownedvalue:', self._ownedvalue, 'budget:', self._budget
        
    def getReserveValue(self):
        return self._reserveValue
    def getownedSmartToken(self):
        return self._ownedSmartToken
    
    # add customer's reserve amount
    def addReserve(self, addAmount):
        self._reserveValue = self._reserveValue + addAmount
        self._ownedvalue = self._smartToken._Price * self._ownedSmartToken + self._reserveValue
    
    # returned expected Price
    def getExpectedPrice(self):
        return self._expectedPrice
        
    # change the expected price
    def changeExpectedPrice(self, newExpectedPrice):
        self._expectedPrice = newExpectedPrice
        
    def purchase(self, reserveTokenNumber):
        oldPrice = self._smartToken._Price
        if reserveTokenNumber > self._reserveValue:
            print 'Invalid Operation in Purchase'
            return
        # smartToken.purchasing means being converted
        issuedSmartToken = self._smartToken.purchasing(reserveTokenNumber)
        newPrice = self._smartToken._Price      
        self._ownedSmartToken = self._ownedSmartToken + issuedSmartToken
        self._smartValue = self._ownedSmartToken * newPrice
        self._reserveValue = self._reserveValue - reserveTokenNumber
        # in fact, in this case ownedValue and budget actually does not change at all
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._reserveValue + self._smartValue
        self._budget = self._budget + self._ownedvalue - oldownedValue
        
        
    def destroy(self, smartTokenNumber):
        oldPrice = self._smartToken._Price
        if self._ownedSmartToken < smartTokenNumber:
            print 'Invalid Operation in Destroy'
            return
        self._ownedSmartToken = self._ownedSmartToken - smartTokenNumber
        # smartToken.purchasing means being purchased
        ReceivedToken = self._smartToken.destroying(smartTokenNumber)
        newPrice = self._smartToken._Price
        self._smartValue = self._ownedSmartToken*newPrice
        self._reserveValue = self._reserveValue + ReceivedToken
        # In fact, in this case ownedValue actually does not change at all
        oldownedValue = self._ownedvalue
        self._ownedvalue = self._reserveValue + self._smartValue
        self._budget = self._budget + self._ownedvalue - oldownedValue

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
        # ETH be convert into BNT
        issuedtokenNum = self._Supply * (((self._ReserveBalance + convertIntoNum)/self._ReserveBalance)**(self._CRR) - 1)
        self._Supply = self._Supply + issuedtokenNum
        self._ReserveBalance = self._ReserveBalance + convertIntoNum
        oldPrice = self._Price
        self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
        increaseRatio = (self._Price - oldPrice)/oldPrice
        # print '&&&&&&&&&&'
        # print round(convertIntoNum,2), self._ReservetokenName+" be converted into as", round(issuedtokenNum,2), self._Name
        # print "Current price of "+self._Name+" is", self._Price, "with", round(increaseRatio*100,4), "% increasing."
        self._budget = self._budget + self._Price*self._Supply - oldPrice*(self._Supply - issuedtokenNum)
        return issuedtokenNum

    def destroying(self, convertOutNum=0):
        # BNT be converted out to ETH
        destroyedtokenNum = convertOutNum      
        reserveReceivedNum = self._ReserveBalance*(1 - ((self._Supply - convertOutNum)/self._Supply)**(1/self._CRR))
        self._Supply = self._Supply - destroyedtokenNum
        self._ReserveBalance = self._ReserveBalance - reserveReceivedNum
        oldPrice = self._Price
        self._Price = self.updatePrice(self._ReserveBalance, self._Supply, self._CRR)
        decreaseRatio = (oldPrice-self._Price)/oldPrice
        # print '**********'
        # print round(convertOutNum,2), self._Name+" be converted out as", round(reserveReceivedNum,2), self._ReservetokenName
        # print "Current price of "+self._Name+" is", self._Price, "with", round(decreaseRatio*100,4), "% decreasing."
        self._budget = self._budget + self._Price*self._Supply - oldPrice*(self._Supply + destroyedtokenNum)
        return reserveReceivedNum

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self._timeRound = int(0)
        self._custNum = int(0)
        self._custOriginalReserve = float(-1)
        self._custOriginalSmartTokens = float(-1)
        self._sigma = float(0)
        self.initUI()
        
    def initUI(self): 

        self.label1 = QtGui.QLabel(self)   
        self.label1.move(40, 20)
        self.label1.setText('Time Round:')

        self.lbl1 = QtGui.QLabel(self)
        self.lbl1.move(200, 20)

        self.label2 = QtGui.QLabel(self)   
        self.label2.move(40, 40)
        self.label2.setText('# of Customers In:')

        self.lbl2 = QtGui.QLabel(self)
        self.lbl2.move(200, 40)

        self.label3 = QtGui.QLabel(self)   
        self.label3.move(280, 20)
        self.label3.setText('Cust Init Reserve:')

        self.lbl3 = QtGui.QLabel(self)
        self.lbl3.move(450, 20)

        self.label4 = QtGui.QLabel(self)   
        self.label4.move(280, 40)
        self.label4.setText('Cust Init SmartTokens:')

        self.lbl4 = QtGui.QLabel(self)
        self.lbl4.move(450, 40)

        self.label5 = QtGui.QLabel(self)   
        self.label5.move(40, 60)
        self.label5.setText('Sigma:')

        self.lbl5 = QtGui.QLabel(self)
        self.lbl5.move(200, 60)

        self.label_qle1 = QtGui.QLabel(self)   
        self.label_qle1.move(40, 90)
        self.label_qle1.setText('Rounds Input:')

        # receive the input of Time Round
        qle1 = QtGui.QLineEdit(self)
        qle1.move(350, 90)
        qle1.textChanged[str].connect(self.onChanged_qle1)

        self.label_qle2 = QtGui.QLabel(self)   
        self.label_qle2.move(40, 120)
        self.label_qle2.setText('#Customers Input:')

        # receive the input of Customers in
        qle2 = QtGui.QLineEdit(self)
        qle2.move(350, 120)
        qle2.textChanged[str].connect(self.onChanged_qle2)

        
        self.label_qle3 = QtGui.QLabel(self)   
        self.label_qle3.move(40, 150)
        self.label_qle3.setText('Cust Init Reserve:')

        # receive the input of cust original reserve
        qle3 = QtGui.QLineEdit(self)
        qle3.move(350, 150)
        qle3.textChanged[str].connect(self.onChanged_qle3)

        self.label_qle4 = QtGui.QLabel(self)   
        self.label_qle4.move(40, 180)
        self.label_qle4.setText('Cust Init SmartToken:')

        # receive the input of Cust original smartTokens
        qle4 = QtGui.QLineEdit(self)
        qle4.move(350, 180)
        qle4.textChanged[str].connect(self.onChanged_qle4)

        self.label_qle5 = QtGui.QLabel(self)   
        self.label_qle5.move(40, 210)
        self.label_qle5.setText('Gaussian Sigma:')

        # receive the input of Cust original smartTokens
        qle5 = QtGui.QLineEdit(self)
        qle5.move(350, 210)
        qle5.textChanged[str].connect(self.onChanged_qle5)

        # # time bar
        # self.pbar = QtGui.QProgressBar(self)
        # self.pbar.setGeometry(40, 250, 450, 25)
        self.timer = QtCore.QBasicTimer()
        self.step = 0

        self.btn = QtGui.QPushButton('Start', self)
        self.btn.move(100, 250)
        self.btn.clicked.connect(self.doAction)

        self.qbtn = QtGui.QPushButton('Quit', self)
        self.qbtn.move(300, 250)
        self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        self.label_status = QtGui.QLabel(self)   
        self.label_status.move(790, 280)
        # self.label_status.setText('Ready!')

        mylabel = QtGui.QLabel(self)
        pixmap = QtGui.QPixmap(os.getcwd() + '/bancor.png')
        mylabel.setPixmap(pixmap)
        mylabel.move(560, 40)

        self.myimg_Price = QtGui.QLabel(self)
        self.myimg_Price.move(60, 300)

        self.myimg_Failure = QtGui.QLabel(self)
        self.myimg_Failure.move(560, 300)
        
        # original 1000 * 500
        self.setGeometry(100, 100, 850, 300)
        self.setWindowTitle('Bancor Simulator')
        self.show()
    
    # get time round info
    def onChanged_qle1(self, text):
        try:
            self._timeRound = int(text)
        except Exception as e:
            self.lbl1.setText('WARNING: Input is not digit!')
            self.lbl1.adjustSize()
            return
        self.lbl1.setText(text)
        self.lbl1.adjustSize()
    # get cust# come in in each round info
    def onChanged_qle2(self, text):
        try:
            self._custNum = int(text)
        except Exception as e:
            self.lbl2.setText('WARNING: Input is not digit!')
            self.lbl2.adjustSize()
            return
        self.lbl2.setText(text)
        self.lbl2.adjustSize()

    # get cust Original Reserve
    def onChanged_qle3(self, text):
        try:
            self._custOriginalReserve = float(text)
        except Exception as e:
            self.lbl3.setText('WARNING: Input is not digit!')
            self.lbl3.adjustSize()
            return
        self.lbl3.setText(text)
        self.lbl3.adjustSize()

    # get cust Original SmartTokens
    def onChanged_qle4(self, text):
        try:
            self._custOriginalSmartTokens = float(text)
        except Exception as e:
            self.lbl4.setText('WARNING: Input is not digit!')
            self.lbl4.adjustSize()
            return
        self.lbl4.setText(text)
        self.lbl4.adjustSize()

    # get Gaussian's init Sigma
    def onChanged_qle5(self, text):
        try:
            self._sigma = float(text)
        except Exception as e:
            self.lbl5.setText('WARNING: Input is not digit!')
            self.lbl5.adjustSize()
            return
        self.lbl5.setText(text)
        self.lbl5.adjustSize()

    def timerEvent(self, e):
      
        if self.step >= 100:
        
            self.timer.stop()
            self.btn.setText('Start')
            self.step = 0
            return
            
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
    	self.label_status.setText('Running ...')
        if (self._timeRound == int(0)) or (self._custNum == int(0)) or (self._custOriginalReserve == float(-1)) or (self._custOriginalSmartTokens == float(-1) or (self._sigma == float(0))):
            print "Error, Lack of Input! "
            self.label_status.setText('Ready!')
            return
        # self.timer.start(100, self)        
        MarketSimulating(self._timeRound, self._custNum, self._custOriginalReserve, self._custOriginalSmartTokens, self._sigma)
        
        '''
        still don't know why these syntax doesn't work
        '''
        # self.label_status.setText('Ready!')
        # pixmap_Price = QtGui.QPixmap(os.getcwd() + '/Price/Price_Change.png')
        # self.myimg_Price.setPixmap(pixmap_Price)
        # pixmap_Failure = QtGui.QPixmap(os.getcwd() + '/Failure/FailureRate-All.png')
        # self.myimg_Price.setPixmap(pixmap_Failure)

        os.system('xdg-open '+os.getcwd() + '/Price/Price_Change.png')
        os.system('xdg-open '+os.getcwd() + '/Failure/FailureRate-All.png')

        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()