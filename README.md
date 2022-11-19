# Norn-Finance-Backtesting

# Troubleshooting

- ImportError cannot import name 'warnings' from 'matplotlib.dates'
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

