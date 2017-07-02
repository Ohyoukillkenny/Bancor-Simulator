import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from smartToken import *
from customers import *
fw = open('Transaction-Record.txt','w')

# issue a new smart token
initIssue = 300000
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
TimeRound = 100
custNum = 100
custOriginalReserve = 100
custOriginalSmartTokens = 100
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
    sigma = 0.1
    np.random.seed(0)
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
        np.random.seed(0)
        seed = random.randint(1, 100)
        if seed <= alpha:
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
                '''
                # if CurrentPrice < Joe.getExpectedPrice():
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
fw.close()

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
    PriceAllRound.append(Price_eachRound[99])
    x = np.asarray(myX)
    y = np.asarray(Price_eachRound)
    plt.plot(x,y,'o',color = 'navy',alpha = 0.8)
    plt.title('Price Change in Round \"'+str(j)+'\"',fontsize = 25)
    plt.xlabel('Customer #',fontsize = 15)
    plt.ylabel('Price of Smart Token', fontsize = 15)
    plt.savefig('Price/PriceRound/Price_inRound'+str(j)+'.png', bbox_inches='tight')
    plt.close()
    my_Xall.append(j)
    print 'Price Change Fig, Round '+str(j)+' Over...'
    j = j + 1
allX = np.asarray(my_Xall)
ally = np.asarray(PriceAllRound)
plt.plot(allX,ally,'o',color = 'navy',alpha = 0.8)
plt.title('Price Change For All Round',fontsize = 25)
plt.xlabel('Round #',fontsize = 15)
plt.ylabel('Price of Smart Token', fontsize = 15)
plt.savefig('Price/Price_Change.png', bbox_inches='tight')
plt.close()
