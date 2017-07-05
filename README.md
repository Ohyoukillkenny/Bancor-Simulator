# Bancor-Simulator

![Bancor icon](https://cdn-images-1.medium.com/max/600/1*0u59V1q5pcP5f1fArOkF1g.jpeg)

### We build a simulator of Bancor, which helps to explain the difference between Bancor market and real-world market.

## Configuration

1. Python 2.7 + Anaconda 2.7.
2. PyQT4 and Linux Operating System required for running the GUI


## How to run
### Here we give three ways to view how Bancor protocol works.

1. *Recommended*, run *Bancor-Simulating.ipynb* in ipython notebook, then follow the comments.
2. *For Results*, run *BancorGUI.py* in file *QT*, by inputting value to GUI.
3. Run *marketsimulator.py* in python. The customers.py presents the python class for customer simulating, the smartToken.py is the python class for smartToken in Bancor market, which includes the Bancor protocol.

## Other documents

1. *Failure* file contains figures about failure rate of transaction.
2. *Price* file contains figures about the shifting price of the Smarttoken with the time.
3. *Transaction-Record.txt* records the information of smarkToken during transactions.
4. *gaussian.py* and *gaussian-price.ipynb* are just codes for gaussian function testing. Please ignore them.
5. *QT* file contains GUI codes for Bancor simulator as well as figures and txt file which tracks information in simulating.