# Student project in Liquidity Premium Term Structures

Hello! This project contains quite a comprehensive data analysis framework to apply yield curve metrics and cost of carry principles. The model essentially parses historical market data to isolate hidden liquidity premiums from total funding spreads across distinct maturity tenors (1M, 3M, 6M, 12M).

### Methodology notes:
* Imports multi-currency historical government yields and wholesale tracking baselines
* Isolates credit risk components from total spreads using transaction volume liquidity friction proxies
* Generates an aggregated structural term report tracking how the liquidity premium scales across longer-dated cash lockup windows.
