from smartToken import *
from customers import *
from market import *
import random
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# the Bancor Market has to be sychronized in every different time slot
def sychronizeMarket(market):
    market.sychronize()

TimeSlotNum = 1000
for timeEpoch in [50, 200]:
    for bouncingRange in [2.0, 5.0]:
        for custNum in [1000]:
            for sigma in [1.0]:
                            
                # the seeds of pseudo-random numbers
                mySeeds = [0,1,2]

                All_TXNUM = 0
                ALL_CANCELEDNUM = 0
                ALL_SLIP = 0
                ALL_MEDIUMSLIP = 0
                ALL_HUGESLIP = 0

                for mySeed in mySeeds:
                    np.random.seed(mySeed)
                    # issue a new smart token
                    # initIssue = 3000000
                    initIssue = 800000
                    CRR = 0.5
                    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH', initCRR=CRR, initPrice= 10, initIssueNum=initIssue)

                    # create two different markets
                    MyBancorMarket = BancorMarket(smartToken = KennyCoin)

                    print 'T:',timeEpoch, 'R:', bouncingRange, 'Nc:', custNum, 'sig:', sigma, 'seed:', mySeed, 'processing...'

                    '''
                    First of all, we initialize the customer's tokenBalance and reserveBalance
                    tokenBalance: 200, reserveBalance: 200
                    '''
                    custInitReserveBalance = 200
                    custInitTokenBalance = 200
                    if custInitTokenBalance * custNum > (initIssue * (1 - CRR)):
                        print 'ERROR, too many init smart tokens holding by customers.'
                        sys.exit(0)

                    custList = []
                    # here we name single customer as Joe. And every customer is initialized with 
                    # random value of token balance as well as reserve balance.
                    for i in range(custNum):
                        Joe = Customer(smartToken = KennyCoin, market = MyBancorMarket, 
                                        tokenBalance = custInitTokenBalance, 
                                        reserveBalance = custInitReserveBalance)
                        custList.append(Joe)

                    # priceTracker records the change of the smart token's price in Bancor market
                    priceTracker = []
                    # transaction tracker records the transations' number in each time slot
                    txTracker = []
                    # canceled transaction tracker records the canceled transactions' number in each time slot
                    canceledTxTracker = []

                    valuation_Epoch = []

                    valuation_plot = []
                    for j in range(TimeSlotNum):
                        # Sychronize the market
                        sychronizeMarket(MyBancorMarket)
                        '''
                        First of all, we randomize mean valuations in time epochs, and save in valuation_Epoch list. 
                        For instance, 0-49 time slot comprise the first time epoch.
                        If the mean valuation is 20 ETH, in 0 - 49 time slots, 
                            customers generate their orders based on 19.4 ETH, 21.2 ETH ...
                        '''
                        # (Ps / R, Ps * R)
                        currentPrice = KennyCoin.getPrice()
                        if j % timeEpoch == 0:
                            # clean the valuation_Epoch list at first
                            valuation_Epoch = []
                            if bool(random.getrandbits(1)):
                                valuation_mu_Epoch = random.uniform(currentPrice/bouncingRange, currentPrice)
                            else:
                                valuation_mu_Epoch = random.uniform(currentPrice, currentPrice*bouncingRange)
                            # generate a random series of valuations in timeEpoch

                            # print 'valuation_mu in timeEpoch:', valuation_mu_Epoch
                            valuation_Epoch = np.random.normal(valuation_mu_Epoch, 1, timeEpoch).tolist()
                            valuation_plot.extend(valuation_Epoch)

                        valuation_mu = valuation_Epoch[j % timeEpoch]
                        custValuation_list = np.random.normal(valuation_mu, sigma, custNum)
                        for i in range(custNum):
                            if custValuation_list[i] < 0:
                                # Customer does not want to sell their token in free. 
                                # Here we give them a small valuation when valuation < 0
                                custList[i].changeValuation(0.001*currentPrice, currentPrice)
                            else:
                                custList[i].changeValuation(custValuation_list[i], currentPrice)

                        '''
                        In every time slot, record the information of this time slot in the market, 
                            such as Price, transactionNum and cancled Tx Num of this time slot
                        '''
                        priceTracker.append(KennyCoin.getPrice())
                        txTracker.append(MyBancorMarket.getTransactionNum())
                        canceledTxTracker.append(MyBancorMarket.getCanceledTransactionNum())

                        # show some information in terminal
                        # print ('In time slot:'+str(j)+' | '+str(sell)+
                        #     ' sells. And '+str(buy)+' buys.')
                    valuationPlot = []
                    myX_V = []
                    for j in range(TimeSlotNum):
                        valuationPlot.append(valuation_plot[j])
                        myX_V.append(j)
                    x_V = np.asarray(myX_V[::2])
                    y_V = np.asarray(valuationPlot[::2])
                    plt.plot(x_V, y_V, 'o-',color = 'navy', alpha = 0.8)
                    plt.title('Vt in Bancor Market',fontsize = 25)
                    plt.xlabel('t',fontsize = 15)
                    plt.ylabel('Vt of Smart Token (ETH)', fontsize = 15)
                    plt.savefig('Figures/Bancor/Valuation-TE-'+str(timeEpoch)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'Seed-'+str(mySeed)+'.pdf', bbox_inches='tight')
                    plt.close()

                    # '''Plotting'''
                    if mySeed == 0:
                        # # Figure about price changing
                        pricePlot = []
                        myX_P = []
                        for j in range(TimeSlotNum):
                            pricePlot.append(priceTracker[j])
                            myX_P.append(j)
                        x_P = np.asarray(myX_P[::5])
                        y_P = np.asarray(pricePlot[::5])
                        plt.plot(x_P, y_P, 'o-',color = 'navy', alpha = 0.8)
                        plt.title('Price Change For Bancor Market',fontsize = 25)
                        plt.xlabel('t',fontsize = 15)
                        plt.ylabel('Price of Smart Token (ETH)', fontsize = 15)
                        plt.savefig('Figures/Bancor/Price-TE-'+str(timeEpoch)+
                            'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'Seed-'+str(mySeed)+'.pdf', bbox_inches='tight')
                        plt.close()

                    # File about transactions counting
                    fw_trax = open('Result/Bancor/Tx_T-'+str(TimeSlotNum)+'TE-'+str(timeEpoch)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'Seed-'+str(mySeed)+'.txt', 'w')
                    fw_trax.write('All_Tx:'+'\t'+str(sum(txTracker))+'\tCanceled:'+'\t'+str(sum(canceledTxTracker)))
                    All_TXNUM += sum(txTracker)
                    ALL_CANCELEDNUM += sum(canceledTxTracker)
                    fw_trax.close()

                    # File about price slipping
                    priceSlip = 0
                    mediumPriceSlip = 0
                    hugePriceSlip = 0
                    for j in range(TimeSlotNum - 1):
                        if priceTracker[j+1] < priceTracker[j]:
                            priceSlip += 1
                            if priceTracker[j+1] < 0.95 * priceTracker[j]:
                                mediumPriceSlip += 1
                                if priceTracker[j+1] < 0.8 * priceTracker[j]:
                                    hugePriceSlip += 1
                        else:
                            continue
                    fw_slip = open('Result/Bancor/Slip_T-'+str(TimeSlotNum)+'TE-'+str(timeEpoch)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'Seed-'+str(mySeed)+'.txt', 'w')
                    fw_slip.write('Slip:'+'\t'+str(priceSlip)+'\tMedium-slip:'+'\t'
                        +str(mediumPriceSlip)+'\tHuge-slip:'+'\t'+str(hugePriceSlip))
                    ALL_SLIP += priceSlip
                    ALL_MEDIUMSLIP += mediumPriceSlip
                    ALL_HUGESLIP += hugePriceSlip
                    fw_slip.close()

                avg_All_TXNUM = All_TXNUM / float(len(mySeeds))
                avg_ALL_CANCELEDNUM = ALL_CANCELEDNUM / float(len(mySeeds))
                Canceled_TX_Ratio = avg_ALL_CANCELEDNUM / avg_All_TXNUM

                avg_ALL_SLIP = ALL_SLIP / float(len(mySeeds))
                avg_ALL_MEDIUMSLIP = ALL_MEDIUMSLIP / float(len(mySeeds))
                avg_ALL_HUGESLIP = ALL_HUGESLIP / float(len(mySeeds))

                Slip_Ratio = avg_ALL_SLIP / float(TimeSlotNum)
                MediumSlip_Ratio = avg_ALL_MEDIUMSLIP / float(TimeSlotNum)
                HugeSlip_Ratio = avg_ALL_HUGESLIP / float(TimeSlotNum)

                fw_statistic = open('Figures/Bancor/TE-'+str(timeEpoch)+
                        'BG-'+str(bouncingRange)+'CN-'+str(custNum)+'Sig-'+str(sigma)+'.txt','w')
                fw_statistic.write(str(avg_All_TXNUM)+'\t'+str(avg_ALL_CANCELEDNUM)+'\t'+str(Canceled_TX_Ratio)
                    +'\t'+str(avg_ALL_SLIP)+'\t'+str(avg_ALL_MEDIUMSLIP)+'\t'+str(avg_ALL_HUGESLIP)+'\t'
                    +str(Slip_Ratio)+'\t'+str(MediumSlip_Ratio)+'\t'+str(HugeSlip_Ratio))
                fw_statistic.close()

