#https://www.amazon.in/ASUS-15-6-inch-i5-10300H-Graphics-FX566LI-HN272T/dp/B098P62W63
from bs4 import BeautifulSoup
import requests,time,datetime
import PySimpleGUI as sg
from urllib.request import urlopen
from threading import Thread
stop=False
def checker():
    global name
    if stop==True:
        try:
            if name!=None:
                sg.SystemTray.notify(name,"Product Not Available")
            else:
                sg.SystemTray.notify("Error","Product Not Available")
        except:
            sg.SystemTray.notify("Error","Product Not Available")
        exit()
    def net_connection():
        try:
            urlopen('https://www.google.com',timeout=2)
            return True
        except:
            sg.SystemTray.notify('No Internet Connection',"Check Your Connection")
    try:
        file=open("Link.txt","r")
        net_connection()
        url = file.read()
        k=url.split("/")
        url="/".join(k[:6])
        print(url)
        file.close()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        prices = soup.find('span', id ='priceblock_ourprice')
        name=soup.find('span',id="productTitle")
        name=str(name.text).strip()
        if prices is None:
            prices = soup.find('span', id ='priceblock_dealprice')
            if prices is None:
                prices=soup.find('span',id='kindle-price')
        price=str(prices.text)
        t=datetime.datetime.now()
        f=open("Price_Data/Saved_Prices.txt","a")
        f.write(str(t.day)+"/"+str(t.month)+"/"+str(t.year)+" # "+name+" : "+str(price))
        f.write("\n\n")
        f.close()
        sg.SystemTray.notify(name,"Current Price : "+str(price))
        exit()
    except AttributeError:
        exec(open("/home/user/Desktop/Python Projects/Amazon Price Updater/Amazon Price Updater.py").read())
    except:
        print("An Error had occured in the execution of the Program")
    
c=Thread(target = checker)
c.start()
time.sleep(60)
stop=True
