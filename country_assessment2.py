
import datetime
def determine_lang(c_name,details):
    for key,value in details.items():
        if c_name==key:
            print("Language:",value[3])
def currency_val(c_name,amount,details):
    for ke,val in details.items():
        if c_name==ke:
            rate=amount/float(val[4])
            print("currency value : ",val[4])
            print("EQUIVALENT CURRENCY VALUE FOR", amount,"INR :",rate," ", val[2])
def cuuent_time (c_name,details,h,m):
    for keys,values in details.items():
        if c_name==keys:
            actual_hour=h+values[5]
            actual_minute=m+values[6]
            if actual_hour<0:
                actual_hour=24+actual_hour
            print("current Time=", actual_hour,":",actual_minute,values[0])

country=['UK','USA','INDIA','MEXICO','AUSTRALIA']
time_zone=["gmt","est","ist","cst","adet"]
time=["gmt-5.5","est-10.5","ist+0.0","cst-11.5","adet+5.5"]
currency=['pound','usd','inr','usd','aud']
language=['english','english','hindi','spaanish','english']
currency_rate=['92.72','71.32','1','71.32','47.73']

x=datetime.datetime.now()
print(x)
h= int(x.strftime("%H"))
m = int(x.strftime("%M"))
l=[]
minutes=[]
hour=[]
for j in time:
    s=j.split('t')
    l.append(float(s[1]))
print(l)
for k in l:
    a=k*60
    hour.append(int(k))
    minutes.append(a%60)
print(hour)
print(minutes)
d=list(zip(time_zone,time,currency,language,currency_rate,hour,minutes))
details=dict(zip(country,d))
print(details)
c_name=input("Enter country")
amount=float(input("Amount:"))
cuuent_time (c_name,details,h,m)
determine_lang(c_name,details)
currency_val(c_name,amount,details)
