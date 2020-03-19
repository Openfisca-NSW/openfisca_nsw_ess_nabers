# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:46:36 2020

@author: mccannl
"""

import pandas as pd
dates = [('2019-01-06','2019-02-06'),('2019-02-06','2019-03-06')]

from pandas import DateOffset, Timestamp
from pandas.tseries.offsets import MonthBegin

class LegislativeMonth(DateOffset):
    def __init__(self, n=1, normalize=False, months=1):
        # restricted to months
        kwds = {'months':months}
        super().__init__(n=1, normalize=False, **kwds)
    def apply(self,other):
        end_date = super().apply(other)
        if end_date.day < other.day:
            # truncated to month end
            end_date = end_date + MonthBegin(1)
        return end_date

for a,b in dates:
   earlier,later = sorted(map(Timestamp, (a,b)))
   delta_months = later.month - earlier.month
   delta_months += (later.year - earlier.year) * 12
   end_of_period = earlier + LegislativeMonth(months=delta_months)
   if end_of_period > later:
       delta_months -= 1
   print(f'{earlier.date()} - {later.date()} --> {delta_months}')