# Norn-Finance-Backtesting
![Build Badge](https://github.com/zmcx16/Norn-Finance-Backtesting/workflows/build/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/91acc0c5dfaf47ea8907c076190ba8f9)](https://app.codacy.com/gh/zmcx16/Norn-Finance-Backtesting?utm_source=github.com&utm_medium=referral&utm_content=zmcx16/Norn-Finance-Backtesting&utm_campaign=Badge_Grade_Settings)
[![codecov](https://codecov.io/gh/zmcx16/Norn-Finance-Backtesting/branch/master/graph/badge.svg?token=tvxcZ3NgZ0)](https://codecov.io/gh/zmcx16/Norn-Finance-Backtesting)

The backtesting tool base on backtrader framework.

# How to use
### Download historical data
#### Command usage
```
python download_data.py -s "SPY" -o "./datas"
```

#### Parameters
```
-s          (default = "SPY")                    stock / index symbol
-o          (default = "./datas")                output folder path
-l          (default = "DEBUG")                  log level
```

### Run backtesting tool for Martingale / Anti-Martingale strategy
#### Command usage
```
python main_martingale.py
```

#### Parameters
```
-d          (default = "./datas/SPY.csv")        test data path
-o          (default = "./result.json")          output data path
-from       (default = "1999-01-01")             backtesting data start date
-to         (default = "2021-12-31")             backtesting data end date
-plot       (default = "1")                      plot the backtesting grpah ("1": enable; other: disable)
-t          (default = "1")                      strategy type ("1": Martingale; "-1": Anti-Martingale)
-p          (default = "252")                    the period of highest / lowest for strategy threshold
-s          (default = "0.05")                   position size per trade
-e          (default = "0.05")                   position error for stragtegy threshold (sensitivity)
-mpl        (default = {built-in})               martingale strategy threshold line list ({threshold},{position},{color};  e.g. "0,0.2,#29b6f6;0.05,0.4,#03a9f4")
-l          (default = "INFO")                   log level
```

# Backtesting Report
### Martingale vs AntiMartingale (2000-2021)
| Symbol-Strategy | Cumulative Return | Draw Down | Sharp Ratio
| :----- | -----: |-----: |-----: |
| SPY-All-In | 395.28% | 54.73% | 0.455
| SPY-Martingale | 125.86% | 48.81% | 0.290
| SPY-AntiMartingale | 343.10% | 37.79% | 0.475
| | | | 
| QQQ-All-In | 318.64% | 82.17% | 0.344
| QQQ-Martingale | 49.53% | 79.59% | 0.153 
| QQQ-AntiMartingale | 312.82% | 73.30% | 0.346
| | | | 
| INTC-All-In | 87.74% | 81.54% | 0.206
| INTC-Martingale | 130.36% | 74.90% | 0.233
| INTC-AntiMartingale | 3.79% | 81.76% | 0.111
| | | | 
| C-All-In | -75.55% | 97.90% | 0.009
| C-Martingale | -67.67% | 97.49% | 0.005
| C-AntiMartingale | -64.99% | 95.15% | 0.005

# Demo
![image](https://github.com/zmcx16/Norn-Finance-Backtesting/blob/master/demo/martingale-SPY.png)

![image](https://github.com/zmcx16/Norn-Finance-Backtesting/blob/master/demo/anti-martingale-SPY.png)

# Troubleshooting

### ImportError cannot import name 'warnings' from 'matplotlib.dates'
  1. go to /Lib/site-packages/backtrader/plot/locator.py
  2. replace code as follows
      ``` 
     from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
                              MONTHS_PER_YEAR, DAYS_PER_WEEK,
                              SEC_PER_HOUR, SEC_PER_DAY,
                              num2date, rrulewrapper, YearLocator,
                              MicrosecondLocator, warnings)
      ``` 
     to
      ``` 
     from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
                              MONTHS_PER_YEAR, DAYS_PER_WEEK,
                              SEC_PER_HOUR, SEC_PER_DAY,
                              num2date, rrulewrapper, YearLocator,
                              MicrosecondLocator)
     import warnings
      ```

# License
This project is licensed under the terms of the MIT license.
