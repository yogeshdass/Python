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
hist  -f > seriesdemo.py
hist  -f seriesdemo.py
import numpy
a1=numpy.arange(1,17).resphape(4,4)
a1=numpy.arange(1,17).reshape(4,4)
a1
Df1=DataFrame(a1)
df1
Df1
a1
df1=DataFrame(a1,index='r1 r2 r3 r4'.split(), columns='c1 c2 c3 c4'.split())
df1
df1['c1']
df1['r1':'r2']
df1[0:1]
df1
df1.loc['r1']
df1.loc['r1']
df1.loc[['r1']]
df1.loc['r1','c1']
df1.loc[['r1'],['c1']]
df1.iloc[:,0:3]
hist -f dataframe.py
