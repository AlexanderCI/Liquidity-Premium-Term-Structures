# Student project in liquidity premium term structures

Hello! This project contains a basic data analysis framework for yield curve metrics and cost of carry principles in a liquidity context. The model essentially parses historical market data to isolate hidden liquidity premiums from total funding spreads across distinct maturity tenors (1M, 3M, 6M, 12M).

### Important notes:
* The model imports multi-currency historical government yields and wholesale tracking baselines
* It also isolates credit risk components from total spreads using transaction volume liquidity friction proxies
* It then generates an aggregated structural term report tracking how the liquidity premium scales across longer-dated cash lockup windows.
