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
for TE in [10, 20, 30, 40, 50, 70, 80, 100, 150, 200, 500]:
    for R in [3.5]:
        for N in [1000]:
            for sig in [2.0]:
                # the seeds of pseudo-random numbers
                mySeeds = [0,1,2,3,4,5,6,7,8,9]

                # variables for statistic usage
                All_TXNUM = 0
                ALL_CANCELEDNUM = 0
                ALL_FAILEDTXNUM = 0

                for mySeed in mySeeds:
                    np.random.seed(mySeed)
                    print 'T:',TE, 'R:', R, 'Nc:', N, 'sig:', sig, 'seed:', mySeed, 'processing...'

                    '''
                    Issue a new smart token called KennyCoin, with initialized price 10 ETH, and create the Classic Market.
                    '''
                    KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.5, initPrice=10, initIssueNum=800000)
                    MyClassicMarket = ClassicMarket(smartToken = KennyCoin)

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
                        Joe = Customer(smartToken = KennyCoin, market = MyClassicMarket, 
                                        tokenBalance = int(custInitTokenBalance), 
                                        reserveBalance = int(custInitReserveBalance))
                        custList.append(Joe)

                    '''
                    Initialize several lists for experiment results recording. 
                        -- txTracker records the transations' number in each time slot.
                        -- canceledTxTracker helps to record the canceled transactions' number at the end.
                        -- failedTxTracker helps to record the failed transactions' number at the end.
                    '''
                    txTracker = []
                    canceledTxTracker = []
                    failedTxTracker = []

                    '''
                    In the loop of "for j in range(TimeSlotNum):", we start our simulation of Bancor Market.
                    To begin with, based on the price of smart token, 
                      we generate the market valuation of smart token per time epoch as Vtp, by which the mean valuations Vt can be generated. 
                    After we get Vt, every customer's valuation is generated based on Vt and sig.
                    '''
                    Vt_list = []
                    for j in range(TimeSlotNum):
                        # Sychronize the market
                        sychronizeMarket(MyClassicMarket)
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
                                custList[i].changeValuation(0.001*P, P)
                            else:
                                custList[i].changeValuation(custValuation_list[i], P)

                        '''
                        In every time slot, simulator records all kinds of information in the market.
                        '''
                        txTracker.append(MyClassicMarket.getTransactionNum())
                        canceledTxTracker.append(MyClassicMarket.getCanceledTransactionNum())
                        failedTxTracker.append(MyClassicMarket.getTotallyFailedTransactionNum())

                        # show some information in terminal
                        # print ('In time slot:'+str(j)+' | '+str(MyClassicMarket.getTransactionNum())+
                        #     ' Txs happens. '+str(MyClassicMarket.getCanceledTransactionNum())+' txs are remained in Market.')

                    LastCancelNum = canceledTxTracker[-1]
                    LastFailNum = failedTxTracker[-1]
                    
                    '''
                    Since in Classic Market, we assume the price of smart token does not change, 
                        there is no need to plot the fluctuation graph of price.
                    '''

                    '''Statistic Data'''
                    # File about transactions counting
                    fw_trax = open('Result/Classic/Tx_T-'+str(TimeSlotNum)+'TE-'+str(TE)+
                        'BG-'+str(R)+'CN-'+str(N)+'Sig-'+str(sig)+'Seed-'+str(mySeed)+'.txt', 'w')
                    fw_trax.write('All_Tx:'+'\t'+str(sum(txTracker))+'\tFinal_Canceled:'+'\t'+str(LastCancelNum)
                        +'\tFinal_failed:'+'\t'+str(LastFailNum))
                    All_TXNUM += sum(txTracker)
                    ALL_CANCELEDNUM += LastCancelNum
                    ALL_FAILEDTXNUM += LastFailNum
                    fw_trax.close()

                '''
                We collect data of 10 loops, i.e., 10 times of experiment. 
                Then, we average this data and save the final results in "Figures/Classic" folder's specific files.
                '''
                avg_All_TXNUM = All_TXNUM / float(len(mySeeds))
                avg_ALL_CANCELEDNUM = ALL_CANCELEDNUM / float(len(mySeeds))
                avg_All_FAILEDNUM = ALL_FAILEDTXNUM / float(len(mySeeds))
                Canceled_TX_Ratio = avg_ALL_CANCELEDNUM / avg_All_TXNUM
                Failed_TX_Ratio = avg_All_FAILEDNUM / avg_All_TXNUM

                fw_statistic = open('Figures/Classic/TE/TE-'+str(TE)+
                        'BG-'+str(R)+'CN-'+str(N)+'Sig-'+str(sig)+'.txt','w')
                fw_statistic.write(str(avg_All_TXNUM)+'\t'+str(avg_ALL_CANCELEDNUM)+'\t'+str(avg_All_FAILEDNUM)
                    +'\t'+str(Canceled_TX_Ratio)+'\t'+str(Failed_TX_Ratio))
                fw_statistic.close()




