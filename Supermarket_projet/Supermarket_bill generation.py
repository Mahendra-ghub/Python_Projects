from datetime import datetime

name =(input("Enter your name:"))

Lists='''
Rice  Rs 100/kg
Sugar Rs 30/kg
Dal   Rs 120/kg
Oil   Rs 200/Kg
Soap  Rs 20/each
Paneer Rs 40/Each
Coffe Rs 200/kg
'''
print(Lists)
#declaration
price = 0
pricelist=[]
totalprice = 0
finalprice = 0
ilist = []
qlist = []
plist = []

#rates for items
items = {'Rice':100,'Sugar':30,'Panner':40, 'Coffe':200,'Soap':20,'Oil':200,'Dal':120}
option = int(input("for list of items enter 1:"))
if option == 1:
    print(Lists)
for i in range(len(items)):
  inp1=int(input("if you want to buy press 1 or 2 for exit:"))
  if inp1 == 2:
     break
  if inp1== 1:
     item = input("Enter item name:")
     quantity = int(input("Enter your quantity:"))
     if item in items.keys():
      price = items[item] * quantity
      print(price)
      pricelist.append((item,quantity,items,price))
      totalprice += price
      ilist.append(item)
      qlist.append(quantity)
      plist.append(price)
      gst = totalprice*5/100
      finalamount = totalprice + gst
     else:
       print("this item isnot available.")
  else:
     print("enetered wrong number.")
  inp = input("Can i bill the item:")
  if inp == 'yes':
   pass
   if finalamount != 0:
     for i in range(len(pricelist)):
       print(i,ilist[i],qlist[i],pricelist[i])
  

     