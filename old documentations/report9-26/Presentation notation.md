Presentation notation:

*Page 1*

Today I want to briefly present the result of the market analysis about Bancor Protocol.

I will quickly review the Bancor protocol and then briefly illustrate unfinished details of simulating design. After that, I will thoroughly show my experiment results as well as my analysis based on these results.

*Page 2*

First of all, I present the final conclusion I draw from my simulation. And you can also view these conclusions as the summary of all my whole experiment results. In all of my later slides, what I want to do is to explain how these conclusions being summarised.

So here maybe you can just quickly scan these conclusions, and have a preliminary understanding of them.

*Page 3*

Since it has been a long time for us talked about Bancor protocol. So here I use one slide to quickly review the Bancor protocol.

What it wants to do is to use the price fluctuation of smart tokens to ensure the stability of reserve balance.

For instance, imagine there is a market with initial reserve balance, when people buy smart tokens, the price of them will increase, which makes people more willing to sell. Therefore, price of smart tokens will decrease and the balance will be kept.

*Page 4*

However, the design of Bancor protocol is flawed.

First of all, the frequent price fluctuation might lead bad influence to market. And many transactions might be failed due to it.

Second, the Bancor protocol disregards the potential aberrant market issues such as market craze. The robustness of Bancor awaits substantiation.

Third, the Double Coincidence Bancor aims to resolve might not exist. Even assuming it exists, Bancor shows no evidence about its superiority by experiment results.

Therefore, we try to use the simulation to analyse the Bancor protocol's protential problem.

*Page 5*

This is the overview of our simulating model. Since we have already talked about it, here I will quickly go through it. And there is one thing that we should notice. That is the synchronize step in every time slot. In synchronisation, simulator will tell all customers the price of smart token in the current time step. And then customers can give their valuation and launch orders.

*Page 6*

This is the trading rule implemented in classic market. Here I want to introduce it in order to make sure the correctness of my understanding.

In original state, we assume there are some orders in market. When new order comes, it will look at the existed orders one by one. Edward for instance, he always wants to buy by fewer money. So he first buys Stan's product, then Bob's and finally Amy's.

One thing that we should notice is in the final state, there are five orders remaining in the market, which in the next time slot will be canceled. But there is a difference between these five orders. As Joe, Kyle and Kenny's orders are completely ignored, these orders are totally failed; while Amy and Cartman's orders are partly failed.

And to divide these two situation, we call the first situation — red one as failed orders. And all these five orders as cancelled orders.

*Page 7*

And then we start our simulation. I set three stipulations for simulating.

The first is one time one order, which means one customer at one time can only launch one order.

The second is our old-friend, that is the Gaussian distributed number of customers.

The third is quite new and important. It calls all-in and half-in. They are two policies to determine the transaction value of orders. 

The reason why we implement these two policies I will show you later in experiment’s section. Results show that these two policies actually could lead really different results in classic market.

*Page 8*

Here is an example of the Gaussian distribution. In figure (a), the length of blue bar represents customers' number, and the x-axis such as 1.5, 1.4 represents the valuation of customers.

Figure (b) presents an example of how to use Gaussian distribution to simulate market craze. 

The black curve represents the original state. The blue curve represents the normal cases of price fluctuation. And the new mu of Gaussian distribution is set as the new price of smart token in next time slot. However, if we want to simulate the market craze, the new mu needs to bounce. Just as red line curve shown, we bounce the mu to in a random range and then according to this parameter, customers generate their valuation as a new gaussian distribution. I mean, the medium value of gaussian function needs to be changed significantly.

*Page 9*

Now, we are very close to our experiment. But before we do experiment, we need to specify the parameters we simulate.

Here, we observe four parameters which are listed on the slide.

And in Gaussian distribution, the sigma's chosen directly influences the steepness of the Gaussian curve, just as the figure presented.

*Page10*

So, it is time to make experiment.

Here we define several indexes for measuring market's performance.

These indicators are listed on the slide. And since only in Bancor market, the price of currency will fluctuate, the Price Slipping Ratio is designed for Bancor market only.

The first is price oriented index, in which, price slipping ratio means the possibility of price fluctuation in Bancor market.

….. ppt …..

*Page 11*

First of all, let us view some pictures about the price fluatuation graph under several parameter settings. Though here I only present 9 cases. It can be found that though market craze happens which makes the price of smart token changes fiercely, the Bancor market actually is able to adjust the price to a relatively stable state. And by comparing these figures, with the decrease of σ and the increase of Nc, the price of smart token could be more stable.

*Page 12*

However, since these figures only plot curves by single experiment's data, with the pseudo-random seed 0, which is unrepresentative to reflect the uniform results.

And only observing the price fluctuation of smart token by figures is not accurate enough. Therefore, we quantify the price fluctuating degree by slipping ratio and analyze it by averaging data from 10 times experiments with same parameter settings.

In Figure (a), we can find that with the growth of R, the price splitting ratio slightly increases. And Figure (b) shows when T decrease, the splitting ratio can be largely improved. And in Figure (c), it can be viewed that the splitting ratio drops when customers’ number decreases. And combining all these Figures, we can see with the increase of σ, the price splitting ratio is improved with different degree.

In summary, we can find that when market craze emerges frequently, and the market owns a large size, the price slipping ratio can be very high in Bancor market.

Thus, we can draw our conclusion. … ppt ...

*Page 13*

Then, we study the market's performance of dealing with transactions.

This is the transaction analysis graph for Bancor market under all-in policy.

*Page 14*

In analysis, we learn that with the small customer number, and the closer valuation between customers, the failure rate of transaction orders can exceed more than 10% in Bancor market, which is actually intolerable in real world.

*Page 15*

This is the transaction analysis graph for Classic Market under all-in policy.

In fact, as you can see, the performance of Classic Market is terrible as some cancel ratio is close to 80%. 

*Page 16*

But before we analyse why the performance of Classic Market is so bad. We have another quite interesting finding, that is 

Lower the sigma is, higher the canceled transaction ratio in Bancor Market, while lower ratio in Classic Market.

This phenomenon can be well explained by Figure 10.

In Bancor Market, when price of smart token fluctuates slightly, when σ0 is small, for instance, σ0 = 0.01, the number of influenced customers is larger than case when σ0 is large, for instance, σ0 = 0.1 that is red shadowed area is larger than blue shadowed area. Hence, much more transaction might be failed when σ0 is smaller in Bancor market. 

Similarly in classic market, when a buy order comes, the number of customers who are qualified to satisfy this order is smaller when σ0 = 0.01, as red dash shadowed area is smaller than blue shadowed area. Thus, the cancel or failed rate will be raised when σ0 is small.

*Page 17*

Let us go back to the Classic Market's case under all-in policy.

We find the totally transaction number is decreasing significantly. After print every customers' smart tokens and reserve tokens by python. I find the final reason for the terrible performance in Classic market.

It is because under all-in policy, in classic market, some customers quickly run out their assets as they generate low valuation to sell and generate high valuation to buy with all their money.

And then, Double coincidence of wants does happen as new orders cannot be satisfied due to the paucity of matched orders.

*Page 18*

Therefore, we can find that under all-in policy, the "Double coincidence of wants" problem does exist and largely harms market's efficiency. And Bancor market can alleviate this problem to some extent.

But how about situation under half-in policies? In that case, customers exhaust their money more seldomly.

*Page 19*

This is the situation of half-in policy in Classic Market.

*Page 20*

We actually find under half-in policy, “Double Coincidence of Wants” might no longer be a problem. Since the total transaction number is stable now, and the cancel rate of transaction orders is significantly decreased.

*Page 21*

By comparing the transaction-oriented performance between Bancor market and classic market, we conclude several properties as below:

… ppt ...

*Page 22*

And this picture vividly shows the comparison between Bancor and classic market under All-in policy and half-in policy.

*Page 23*

In summary, we can say that Bancor is flawed.

And this argument is based on solid experiment results.

