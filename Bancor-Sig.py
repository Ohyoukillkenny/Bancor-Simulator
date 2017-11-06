from smartToken import *
from customers import *
from market import *
import random
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

'''
In sychroization, we reset variables which record experiments' results for analysis.
'''
def sychronizeMarket(market):
    market.sychronize()

TimeSlotNum = 1000
for TE in [50]:
    for R in [2.0]:
        for N in [1000]:
            for sig in [0.001, 0.005, 0.01, 0.03, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
                            
                # the seeds of pseudo-random numbers
                mySeeds = [0,1,2,3,4,5,6,7,8,9]

                # variables for statistic usage
                All_TXNUM = 0
                ALL_CANCELEDNUM = 0
                ALL_SLIP = 0
                ALL_MEDIUMSLIP = 0
                ALL_HUGESLIP = 0

                for mySeed in mySeeds:
                    np.random.seed(mySeed)
                    print 'T:',TE, 'R:', R, 'Nc:', N, 'sig:', sig, 'seed:', mySeed, 'processing...'         
                    '''
                    Issue a new smart token called KennyCoin, with initialized price 10 ETH, and create the Bancor Market.
                    '''
                    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH', initCRR=0.5, initPrice= 10, initIssueNum=800000)
                    MyBancorMarket = BancorMarket(smartToken = KennyCoin)

                    '''
                    First of all, we initialize the customer's tokenBalance and reserveBalance
                        -- tokenBalance: 200, reserveBalance: 200
                    To avoid the smart tokens held in customers' hand are more than those issued in initialization,
                        here we use "if custInitTokenBalance * N > (initIssueNum * (1 - CRR)):" to detect this bug. 
                    '''
                    custInitReserveBalance = 200
                    custInitTokenBalance = 200
                    if custInitTokenBalance * N > (800000 * (1 - 0.5)):
                        print 'ERROR, too many init smart tokens holding by customers.'
                        sys.exit(0)

                    ''' 
                    Here we initialize customers in market.
                    We name single customer as Joe, and manage "Joe"s in custList.
                    '''
                    custList = []
                    for i in range(N):
                        Joe = Customer(smartToken = KennyCoin, market = MyBancorMarket, 
                                        tokenBalance = custInitTokenBalance, 
                                        reserveBalance = custInitReserveBalance)
                        custList.append(Joe)

                    '''
                    Initialize several lists for experiment results recording. 
                        -- priceTracker records the change of the smart token's price in Bancor market
                        -- transaction tracker records the transations' number in each time slot
                        -- canceled transaction tracker records the canceled transactions' number in each time slot
                    '''
                    priceTracker = []
                    txTracker = []
                    canceledTxTracker = []

                    '''
                    In the loop of "for j in range(TimeSlotNum):", we start our simulation of Bancor Market.
                    To begin with, based on the price of smart token, i.e., P, 
                      we generate the market valuation of smart token per time epoch as Vtp, by which the mean valuations Vt can be generated. 
                    After we get Vt, every customer's valuation is generated based on Vt and sig.
                    '''
                    Vt_list = []
                    for j in range(TimeSlotNum):
                        sychronizeMarket(MyBancorMarket)
                        '''
                        First of all, we randomize mean valuations per time epochs, and save in Vt_list list. 
                        For instance, 0-49 time slot comprise the first time epoch.
                        If the Vtp is 20 ETH, in 0 - 49 time slots, 
                            customers generate their orders based on 19.4 ETH, 21.2 ETH ...
                        '''
                        P = KennyCoin.getPrice()
                        if j % TE == 0:
                            # reset the Vt_list
                            Vt_list = []
                            if bool(random.getrandbits(1)):
                                Vtp = random.uniform(P/R, P)
                            else:
                                Vtp = random.uniform(P, P*R)
                            Vt_list = np.random.normal(Vtp, 1, TE).tolist()

                        Vt = Vt_list[j % TE]
                        custValuation_list = np.random.normal(Vt, sig, N)
                        '''
                        Here, based on Vt and sig, we have generated every customer's valuation.
                        Since customer does not want to sell their token in free, 
                            we give them a small valuation when generated valuation in Gaussian is smaller than 0.
                        '''
                        for i in range(N):
                            if custValuation_list[i] < 0:
                                custList[i].changeValuation(0.001*P,P)
                            else:
                                custList[i].changeValuation(custValuation_list[i],P)

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

                    '''Plotting'''
                    # if mySeed == 0:
                    #     # # Figure about price changing
                    #     pricePlot = []
                    #     myX_P = []
                    #     for j in range(TimeSlotNum):
                    #         pricePlot.append(priceTracker[j])
                    #         myX_P.append(j)
                    #     x_P = np.asarray(myX_P[::5])
                    #     y_P = np.asarray(pricePlot[::5])
                    #     plt.plot(x_P, y_P, 'o-',color = 'navy', alpha = 0.8)
                    #     plt.title('Price Change For Bancor Market',fontsize = 25)
                    #     plt.xlabel('t',fontsize = 15)
                    #     plt.ylabel('Price of Smart Token (ETH)', fontsize = 15)
                    #     plt.savefig('Figures/Bancor/Sig/Price-TE-'+str(TE)+
                    #         'BG-'+str(R)+'CN-'+str(N)+'Sig-'+str(sig)+'Seed-'+str(mySeed)+'.pdf', bbox_inches='tight')
                    #     plt.close()

                    '''Statistic Data'''
                    # File about transactions counting
                    fw_trax = open('Result/Bancor/Tx_T-'+str(TimeSlotNum)+'TE-'+str(TE)+
                        'BG-'+str(R)+'CN-'+str(N)+'Sig-'+str(sig)+'Seed-'+str(mySeed)+'.txt', 'w')
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
                    fw_slip = open('Result/Bancor/Slip_T-'+str(TimeSlotNum)+'TE-'+str(TE)+
                        'BG-'+str(R)+'CN-'+str(N)+'Sig-'+str(sig)+'Seed-'+str(mySeed)+'.txt', 'w')
                    fw_slip.write('Slip:'+'\t'+str(priceSlip)+'\tMedium-slip:'+'\t'
                        +str(mediumPriceSlip)+'\tHuge-slip:'+'\t'+str(hugePriceSlip))
                    ALL_SLIP += priceSlip
                    ALL_MEDIUMSLIP += mediumPriceSlip
                    ALL_HUGESLIP += hugePriceSlip
                    fw_slip.close()

                '''
                We collect data of 10 loops, i.e., 10 times of experiment. 
                Then, we average this data and save the final results in "Figures/Bancor" folder's specific files.
                '''
                avg_All_TXNUM = All_TXNUM / float(len(mySeeds))
                avg_ALL_CANCELEDNUM = ALL_CANCELEDNUM / float(len(mySeeds))
                Canceled_TX_Ratio = avg_ALL_CANCELEDNUM / avg_All_TXNUM

                avg_ALL_SLIP = ALL_SLIP / float(len(mySeeds))
                avg_ALL_MEDIUMSLIP = ALL_MEDIUMSLIP / float(len(mySeeds))
                avg_ALL_HUGESLIP = ALL_HUGESLIP / float(len(mySeeds))

                Slip_Ratio = avg_ALL_SLIP / float(TimeSlotNum)
                MediumSlip_Ratio = avg_ALL_MEDIUMSLIP / float(TimeSlotNum)
                HugeSlip_Ratio = avg_ALL_HUGESLIP / float(TimeSlotNum)

                fw_statistic = open('Figures/Bancor/Sig/TE-'+str(TE)+
                        'BG-'+str(R)+'CN-'+str(N)+'Sig-'+str(sig)+'.txt','w')
                fw_statistic.write(str(avg_All_TXNUM)+'\t'+str(avg_ALL_CANCELEDNUM)+'\t'+str(Canceled_TX_Ratio)
                    +'\t'+str(avg_ALL_SLIP)+'\t'+str(avg_ALL_MEDIUMSLIP)+'\t'+str(avg_ALL_HUGESLIP)+'\t'
                    +str(Slip_Ratio)+'\t'+str(MediumSlip_Ratio)+'\t'+str(HugeSlip_Ratio))
                fw_statistic.close()