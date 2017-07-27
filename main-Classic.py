from smartToken import *
from customers import *
from market import *
import random
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# the Classic Market has to be sychronized in every different time slot
def sychronizeMarket(market, timeSlot):
    market.sychronize(timeSlot)

# issue a new smart token
initIssue = 3000000
CRR = 0.2
KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=initIssue)

# create two different markets
MyClassicMarket = ClassicMarket(smartToken = KennyCoin)

'''
TimeSlotNum = 1000
bouncingInterval = 200
bouncingRange = 10.0
custNum = 2000
sigma = 0.01
'''
TimeSlotNum = 1000
for bouncingInterval in [50, 200]:
    for bouncingRange in [5.0, 10]:
        for custNum in [500, 2000]:
            for sigma in [0.01, 0.1, 1]:
                # the seeds of pseudo-random numbers
                mySeeds = [0,1,2,3,4]
                All_TXNUM = 0
                ALL_CANCELEDNUM = 0
                ALL_FAILEDTXNUM = 0

                for mySeed in mySeeds:
                    np.random.seed(mySeed)
                    myfw = open('Result/Classic/T-'+str(TimeSlotNum)+'BI-'+str(bouncingInterval)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'Seed-'+str(mySeed)+'.txt', 'w')

                    '''
                    First of all, we initialize the customer's tokenBalance and reserveBalance 
                    by Gaussian distributed random number (mu = 200, sigma = 0.1)
                    '''
                    custInitReserveBalance_mu = 200
                    custInitTokenBalance_mu = 200
                    custInitReserveBalance_list = np.random.normal(custInitReserveBalance_mu, 0.1, custNum) # 0.5 is sigma
                    custInitTokenBalance_list = np.random.normal(custInitTokenBalance_mu, 0.1, custNum) # 0.5 is sigma

                    if sum(custInitTokenBalance_list) > (initIssue * (1 - CRR)):
                        print 'ERROR, too many init smart tokens holding by customers.'
                        sys.exit(0)

                    custList = []
                    # here we name single customer as Joe. And every customer is initialized with 
                    # random value of token balance as well as reserve balance.
                    for i in range(custNum):
                        Joe = Customer(smartToken = KennyCoin, market = MyClassicMarket, 
                                        tokenBalance = int(custInitTokenBalance_list[i]), 
                                        reserveBalance = int(custInitReserveBalance_list[i]))
                        custList.append(Joe)

                    # cashTracker records custmers' cash
                    # cashTracker = []
                    # transaction tracker records the transations' number in each time slot
                    txTracker = []
                    # canceled transaction tracker records the canceled transactions' number in each time slot
                    canceledTxTracker = []
                    # failed transaction tracker records the totally failed transactions' number in each time slot
                    failedTxTracker = []

                    for j in range(TimeSlotNum):
                        # Sychronize the market
                        sychronizeMarket(MyClassicMarket, j)

                        # we assume that in every time slot, all customers change their valuation
                        currentMarketPrice = MyClassicMarket.getCurrentPrice()
                        if (j > 0) and (j % bouncingInterval == 0):
                            ''' 
                            We assume the valuation_mu is generated by random, which denotes the mean valuation
                            of customers when the good or bad news comes into market on a certain time slot,
                            which is divided by bouncing interval.
                            '''
                            valuation_mu = random.uniform(currentMarketPrice/bouncingRange, currentMarketPrice*bouncingRange)
                        else:
                            valuation_mu = currentMarketPrice

                        custValuation_list = np.random.normal(valuation_mu, sigma, custNum)
                        for i in range(custNum):
                            if custValuation_list[i] < 0:
                                # Customer does not want to sell their token in free. 
                                # Here we give them a small valuation when valuation < 0
                                custList[i].changeValuation(0.001*currentMarketPrice)
                            else:
                                custList[i].changeValuation(custValuation_list[i])

                        txTracker.append(MyClassicMarket.getTransactionNum())
                        canceledTxTracker.append(MyClassicMarket.getCanceledTransactionNum())
                        failedTxTracker.append(MyClassicMarket.getTotallyFailedTransactionNum())

                        # show some information in terminal
                        print ('In time slot:'+str(j)+' | '+str(MyClassicMarket.getTransactionNum())+
                            ' happens. And '+str(MyClassicMarket.getCanceledTransactionNum())+' transactions are canceled. | And '+
                            str(MyClassicMarket.getTotallyFailedTransactionNum())+' totally failed.')
                        myfw.write(str(j)+'\t'+str(MyClassicMarket.getTransactionNum())+'\t'+
                                    str(MyClassicMarket.getCanceledTransactionNum())+'\t'+
                                    str(MyClassicMarket.getTotallyFailedTransactionNum())+'\n')
                    myfw.close()
                    
                    '''Plotting'''

                    # Figure about transactions
                    txPlot = []
                    myX_T = []
                    for j in range(TimeSlotNum):
                        txPlot.append(txTracker[j])
                        myX_T.append(j)

                    x_T = np.asarray(myX_T)
                    y_T = np.asarray(txPlot)
                    plt.plot(x_T, y_T, 'o-',color = 'navy', alpha = 0.8)
                    plt.title('Transaction Num For Classic Market',fontsize = 25)
                    plt.xlabel('Time Slot #',fontsize = 15)
                    plt.ylabel('Transaction #', fontsize = 15)
                    plt.savefig('Figures/Classic/Transactions-Seed-'+str(mySeed)+'.pdf', bbox_inches='tight')
                    plt.close()

                    # Figure about canceled transactions
                    canceledTxPlot = []
                    myX_C = []
                    for j in range(TimeSlotNum):
                        canceledTxPlot.append(canceledTxTracker[j])
                        myX_C.append(j)

                    x_C = np.asarray(myX_C)
                    y_C = np.asarray(canceledTxPlot)
                    plt.plot(x_C, y_C, 'o-',color = 'navy', alpha = 0.8)
                    plt.title('Canceled Transaction Num For Classic Market',fontsize = 25)
                    plt.xlabel('Time Slot #',fontsize = 15)
                    plt.ylabel('Canceled Transaction #', fontsize = 15)
                    plt.savefig('Figures/Classic/CanceledTx-Seed-'+str(mySeed)+'.pdf', bbox_inches='tight')
                    plt.close()

                    # Figure about failed transactions
                    failedTxPlot = []
                    myX_F = []
                    for j in range(TimeSlotNum):
                        failedTxPlot.append(failedTxTracker[j])
                        myX_F.append(j)

                    x_F = np.asarray(myX_F)
                    y_F = np.asarray(failedTxPlot)
                    plt.plot(x_F, y_F, 'o-',color = 'navy', alpha = 0.8)
                    plt.title('Failed Transaction Num For Classic Market',fontsize = 25)
                    plt.xlabel('Time Slot #',fontsize = 15)
                    plt.ylabel('Failed Transaction #', fontsize = 15)
                    plt.savefig('Figures/Classic/FailedTx-Seed-'+str(mySeed)+'.pdf', bbox_inches='tight')
                    plt.close()

                    fw_trax = open('Result/Classic/Tx_T-'+str(TimeSlotNum)+'BI-'+str(bouncingInterval)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'Seed-'+str(mySeed)+'.txt', 'w')
                    fw_trax.write('All_Tx:'+'\t'+str(sum(txTracker))+'\tCanceled:'+'\t'+str(sum(canceledTxTracker))
                        +'\tTotally_failed:'+'\t'+str(sum(failedTxTracker)))
                    All_TXNUM += sum(txTracker)
                    ALL_CANCELEDNUM += sum(canceledTxTracker)
                    ALL_FAILEDTXNUM += sum(failedTxTracker)
                    fw_trax.close()


                avg_All_TXNUM = All_TXNUM / float(len(mySeeds))
                avg_ALL_CANCELEDNUM = ALL_CANCELEDNUM / float(len(mySeeds))
                avg_All_FAILEDNUM = ALL_FAILEDTXNUM / float(len(mySeeds))
                Canceled_TX_Ratio = avg_ALL_CANCELEDNUM / avg_All_TXNUM
                Failed_TX_Ratio = avg_All_FAILEDNUM / avg_All_TXNUM

                fw_statistic = open('Figures/Classic/Statistic-'+str(TimeSlotNum)+'BI-'+str(bouncingInterval)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'.txt','w')
                fw_statistic.write(str(avg_All_TXNUM)+'\t'+str(avg_ALL_CANCELEDNUM)+'\t'+str(avg_All_FAILEDNUM)
                    +'\t'+str(Canceled_TX_Ratio)+'\t'+str(Failed_TX_Ratio))
                fw_statistic.close()





