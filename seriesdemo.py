from pandas import Series
from pandas import DataFrame
l1=[10,20,30,40]
s1=Series(l1)
s1
s1.values
s1.index
s1.index=list('abcde')
s1.index=list('abcd')
s1
s1[0:3]
s1['a':'d']
hist  -f seriesdemo.py
