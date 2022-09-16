from tkinter import *
from tkinter.ttk import Combobox
import urllib.request as request
import re
import requests as reqs
import json


#當選取城市時顯示城市的天氣資訊
def showWeather(event):

    # 抓取城市天氣資訊
    weatherUrl = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-FDBBB16D-6A36-4072-8388-8A663EEF6F9D'
    req = reqs.get(weatherUrl)
    weatherJson = json.loads(req.text)

    for location in weatherJson['records']['location']:
        if location['locationName'] == cityMenu.get():
            Wx='天氣狀況 : ' + location['weatherElement'][0]['time'][0]['parameter']['parameterName']
            PoP='降雨機率 : ' + location['weatherElement'][1]['time'][0]['parameter']['parameterName'] + '%'
            CI='體感狀況 : ' + location['weatherElement'][3]['time'][0]['parameter']['parameterName']
            Temp='氣溫 : ' + location['weatherElement'][2]['time'][0]['parameter']['parameterName'] + '°C ~ ' + location['weatherElement'][4]['time'][0]['parameter']['parameterName'] + '°C'
            Info='{}\n\n{}\n\n{}\n\n{}'.format(Wx,PoP,CI,Temp)
            weatherInfo.config(text=Info)

    if '雷' in Wx:
        weatherWx.config(image=image01)
    elif '雨' in Wx:
        weatherWx.config(image=image02)
    elif '雲' and '晴' in Wx:
        weatherWx.config(image=image03)
    elif '雲' in Wx:
        weatherWx.config(image=image04)
    else:
        weatherWx.config(image=image05)


#獲取當前IP位置天氣資訊
def CurrentIPweather():
    ip = reqs.get('https://api.ipify.org/').text #本機IP

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48'}
    url = "https://whatismyipaddress.com/ip/{}".format(ip)
    requests = request.Request(url, headers=headers)
    with request.urlopen(requests) as response:
        data = response.read().decode("utf-8")
    Latitude = re.search('<span>Latitude:</span> <span>(.*?)</span>', data).group(1).split('&')[0]   #緯度
    Longitude = re.search('<span>Longitude:</span> <span>(.*?)</span>', data).group(1).split('&')[0] #經度

    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,daily,alerts&lang=zh_tw&units=metric&appid=8c1ce97757b096dd52eb61d855d75db9'.format(Latitude, Longitude)
    req = reqs.get(url)
    weatherJson = json.loads(req.text)

    Wx = '天氣狀況 : ' + weatherJson['hourly'][0]['weather'][0]['description']
    PoP = '降雨機率 : ' + str(round(weatherJson['hourly'][0]['pop'] * 100)) + '%'

    url = 'http://api.openweathermap.org/data/2.5/weather?lat=22&lon=120&units=metric&lang=zh_tw&appid=8c1ce97757b096dd52eb61d855d75db9'
    req = reqs.get(url)
    weatherJson = json.loads(req.text)

    Temp = '氣溫 : ' + str(round(weatherJson['main']['temp_min'])) + '°C ~ ' + str(round(weatherJson['main']['temp_max'])) + '°C'

    Info = '本機IP : {}\n\n{}\n\n{}\n\n{}'.format(ip,Wx,PoP,Temp)
    weatherInfo.config(text=Info)

    if '雷' in Wx:
        weatherWx.config(image=image01)
    elif '雨' in Wx:
        weatherWx.config(image=image02)
    elif '雲' and '晴' in Wx:
        weatherWx.config(image=image03)
    elif '雲' in Wx:
        weatherWx.config(image=image04)
    else:
        weatherWx.config(image=image05)


root=Tk()
root.title("City Weather")
root.geometry("500x300")
root.iconbitmap('sources/weather_icon.ico')
root.resizable(0,0)

#取得城市資料
cityFile=open('sources/Cities.txt','r',encoding='UTF-8')
cityRead=cityFile.readline()
cities=tuple(cityRead.split(','))
cityVar=StringVar(root,cities[0])

operate=Frame(root)
menuLabel=Label(operate,text='選擇城市:',font=('Arial', 12))
cityMenu=Combobox(operate,textvariable=cityVar,value=cities,font=('Arial', 12),width=10)
locateBtn=Button(operate,text="取得本機IP地點資訊",width=20,height=2,font=('Arial', 12),command=CurrentIPweather)

menuLabel.pack(side=LEFT)
cityMenu.pack(side=LEFT,padx=10,pady=20)
locateBtn.pack(side=LEFT,padx=20,pady=20)
operate.pack(side=TOP)

cityMenu.bind('<<ComboboxSelected>>', showWeather)

weatherFrame=LabelFrame(root,text="⛅天氣資訊",width=500,height=500,font=('Arial', 12))
weatherFrame.pack(padx=20,pady=20)
weatherFrame.propagate(0)

weatherInfo=Label(weatherFrame,text='',font=('Arial', 12),justify=LEFT)
weatherInfo.pack(side=LEFT)

 #天氣圖案
image01 = PhotoImage(file='sources/雷雨.png')
image02 = PhotoImage(file='sources/雨.png')
image03 = PhotoImage(file='sources/晴雲.png')
image04 = PhotoImage(file='sources/雲.png')
image05 = PhotoImage(file='sources/晴.png')

weatherWx=Label(weatherFrame)
weatherWx.pack(side=RIGHT,padx=20,pady=10)

root.mainloop()