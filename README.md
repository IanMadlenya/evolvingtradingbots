# evolvingtradingbots
Evolving Trading Bots

## Data
The /data folder contains historical data organized by the bar size.  

# Notes from email exchanges
It does look like one typical trading algorithm is to use a basic 'mean reversion' model. 

x_{t+1} = x_t + k(\mu - x_t) + \epsilon

k -  an adjustment speed coefficient (so how quickly we expect a return to the mean)
epsilon - Simple error (figure a normal or similar) w/ mu = 0, sigma as a parameter
mu - Calculated mean over some time period (Parameter can be how large of a window we use).

So this gives us a set of 3 parameters - k, sigma_epsilon, mu

Suggested measuring using Sharpe's Ratio.  That has been around for quite some time, and was modified in 1994.  As of now, it looks like the following:

S = (E[R_a - R_b]) / (var[R_a - R_b]**0.5)

Basically, it seems that the ratio is the expected rate of return for your asset vs. the rate of return for the 'benchmark' asset.  In our case the 'benchmark' asset may be the individual commodity we're trading in.  So our benchmark would be if we invested at the start of our cycle, and simply left the money sitting in the commodity throughout.  Our actual asset return will (of course) be the ROI for the algorithm we're using (SA or GA).

Interesting paper here: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1153505

In reading more, I am thinking that we should continue to use the basic model for mean reversion w/ some potential additional factors.  Each additional factor would be modeled in a similar method to the above -  k(\mu - x_t).  We can consider adding two additional factors:

1. A factor for similar commodities (oil, corn?)
2. A factor w/ a different time window (so that we can have two time windows represented).

This would give us a total set of parameters that look like the following:
T_1, K_1 -- First time window duration (multiple of 6 hours), & assoc. weighting factor
T_2, K_2 -- Second time window duration (multiple of 6 hours), & assoc. weighting factor
T_3, K_3 -- Time window for related commodities & weighting factor for related commodities
sigma_epsilon - Std deviation of our error

These 7 parameters would allow us to easily explore the problem space w/ a small amount of additional complexity.  I'll throw together a demo this evening (hopefully!)

Ideally we would also factor volume of trades into this model.  This small blog post here: http://traderfeed.blogspot.com/2006/08/trading-by-mean-reversion.html indicates that low volume in the beginning of a trading day can be indicative of a higher likelihood of mean reversion in a given day


# Notes from 4/16/2016 discussion w/ Richard
  - Need to increase project complexity. 
  - Add comparison to Simulated Annealing
    - Potentially look @ parallel simulated annealing
  - Richard may be able to provide alternative data source


# Notes from 3/20/2016 chat 

## Deliverables for project
  - code
  - write up
  - poster 
  - what experiments we did
 
## Due Dates
  - Proposal 4/7
  - Note that data should not be distributed widely due to concerns over EULA violation

  
 