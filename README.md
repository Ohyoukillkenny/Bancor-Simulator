# Bancor-Simulator

![Bancor icon](https://cdn-images-1.medium.com/max/600/1*0u59V1q5pcP5f1fArOkF1g.jpeg)

### We build a simulator of Bancor, which helps to explain the difference between Bancor market and real-world market.

## Configuration

Python 2.7 + Anaconda 2.7

## How to run
### Here we give three ways to view how Bancor protocol works.

1. *Recommended*, run **Bancor-Simulator.ipynb** in ipython notebook, then follow the comments.
2. Run **main-Bancor.py** and **main-Classical.py** in python. The **customers.py** presents the python class for customer simulating. The **smartToken.py** is the python class for smartToken in Bancor market, which includes the Bancor protocol. And the **market.py** is the python class for Bancor Market and Classical Market simulating.

## Other documents

1. **Figures** file contains temporary figures generated by **main-Bancor.py** and **main-Classical.py**.
2. **Result** file contains text results generated by **main-Bancor.py** and **main-Classical.py**.
3. **Result-July14th** contains all figures and text results of several setting parameters. And I draw analysis column graph in **Results-Bar.numbers** file. Since I use the *np.random.seed()* function call, you can reproduce these results just by running code downloaded from my github account.
4. **regular-patterns-Bancor.pdf** presents some naive analysis of difference between Bancor Market and Classical Market.