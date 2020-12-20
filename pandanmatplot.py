import pandas as pd
from matplotlib import pyplot as plt

itemframe = pd.read_csv('items.csv')
print(itemframe)

salesframe = pd.read_excel('sales.xlsx')
print(salesframe)

#print total sales for the item
#display item name |total sales quantity

print(itemframe.columns)

itemsalesdataframe = pd.merge(itemframe,salesframe) # merge is based on id column, for different clumns in frames, we can user left_on or right_on on columns
print(itemsalesdataframe)

print(itemsalesdataframe.groupby('name').sum().salesquantity)
totalsalesbyname = itemsalesdataframe.groupby('name').sum().salesquantity.reset_index() # to create a new index use reset_index()
print(totalsalesbyname) 

plt.plot(totalsalesbyname.index,totalsalesbyname.salesquantity)
plt.xticks(ticks=totalsalesbyname.index,labels=totalsalesbyname.name)
plt.show()

plt.bar(totalsalesbyname.index,totalsalesbyname.salesquantity)
plt.xticks(ticks=totalsalesbyname.index,labels=totalsalesbyname.name)
plt.show()

plt.pie(totalsalesbyname.salesquantity,labels=totalsalesbyname.name)
plt.show()

plt.pie(totalsalesbyname.salesquantity,labels=totalsalesbyname.name,explode=[.1,0,0,0,0],autopct='%.2f%%')
plt.show()