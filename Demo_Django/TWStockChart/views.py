from re import I
from django.shortcuts import render
from django.http import HttpResponse

import datetime
import twstock as ts
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 
tz=datetime.datetime.now()+datetime.timedelta(hours=8)#設定時區
# Create your viewtos here.


def index(request):#回傳首頁HTML
    return render(request, 'index_new.html')
def searching(request):#回傳快速搜尋頁面HTML
    return render(request,'searching.html')

def result(request):#回傳快速搜尋結果頁面HTML
    try:#利用股票代碼查詢資料,若格式有錯誤則利用股票名稱
        code = request.GET["code"]#抓取輸入的資料
        stock=ts.realtime.get(str(code))#抓取股票即時資料並回傳給HTML
        stock_name=stock['info']['name']
        stock_full_name=stock['info']['fullname']
        best_bid_price=stock['realtime']['best_bid_price']
        best_bid_volume=stock['realtime']['best_bid_volume']
        best_ask_price=stock['realtime']['best_ask_price']
        best_ask_volume=stock['realtime']['best_ask_volume']
        open=stock['realtime']['open']
        high=stock['realtime']['high']
        low=stock['realtime']['low']
        time=datetime.datetime.now()
        return render(request,'result_new.html',locals())
    except:
        try:#若名稱有錯誤,則回傳ERROR頁面
            code = request.GET["code"]
            for i in ts.codes:#確認輸入的股票名稱是否存在
                if code==list(ts.codes[i])[2]:
                    stock=ts.realtime.get(i)
                    code=i
                    break
            stock_name=stock['info']['name']
            stock_full_name=stock['info']['fullname']
            time=datetime.datetime.now()
            best_bid_price=stock['realtime']['best_bid_price']
            best_bid_volume=stock['realtime']['best_bid_volume']
            best_ask_price=stock['realtime']['best_ask_price']
            best_ask_volume=stock['realtime']['best_ask_volume']
            open=stock['realtime']['open']
            high=stock['realtime']['high']
            low=stock['realtime']['low']   
            return render(request,'result_new.html',locals())
        except:
            text ="未搜尋到符合 {} 的項目，請重新輸入。".format(request.GET["code"])#回傳錯誤代碼給HTML
            return render(request,'error.html',locals())#回傳錯誤頁面HTML

def make_image(request):#回傳圖表製作網頁
        return render(request,'make_image_new.html')

def get_image(request):#回傳製作圖表結果頁面
    try:#利用股票名稱來抓取資料並繪製圖表，若股票名稱格式不符合，則用股票代碼
        code=request.GET["code"]#抓取輸入的資料
        month=request.GET["month"]#抓取輸入的資料
        time=month.split('-')#將資料轉為需要的格式
        if our_database(code,time[0],time[1])==1:#判定股票是否在我們的資料庫中
            return render(request,'get_image_new.html')
        else:
            for i in ts.codes:#檢查股票名稱是否存在
                if code==list(ts.codes[i])[2]:
                    stock=ts.realtime.get(i)
                    code=i
                    break
            stock_name=ts.realtime.get(code)#抓取資料並將資料轉換為製圖所需格式
            stock = ts.Stock(code)
            stock_month = stock.fetch(int(time[0]),int(time[1]))
            stock_pd = pd.DataFrame(stock_month)
            c=0
            for i in stock_pd.date:#轉換日期格式
                t=str(i).split('-')
                a=t[1]+'-'+t[2].split(' ')[0]
                stock_pd.date[c]=a
                c+=1
            stock_pd = stock_pd.set_index('date')#將date設為主值
            plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC'] 
            plt.rcParams['axes.unicode_minus'] = False
            fig = plt.figure(figsize=(21, 12))
            plt.plot(stock_pd.close, '-' , label="收盤價")
            plt.plot(stock_pd.open, '-' , label="開盤價")
            plt.title('{}{} 開盤/收盤價曲線'.format(stock_name['info']['name'],time[0]),loc='left',fontsize=30)
            plt.xlabel('日期',fontsize=25)
            plt.ylabel('金額',fontsize=25)
            plt.xticks(fontsize=18,rotation=-30)#Ｘ軸項目設定
            plt.yticks(fontsize=18)
            plt.grid(True, axis='y')
            plt.legend(fontsize=30)
            fig.savefig('D:/Demo_Django/static/images/image.png')
            fig.show()
            return render(request,'get_image_new.html')
    except:#利用股票代碼來抓取資料並繪製圖表，若股票代碼格式不符合，則回傳ERROR頁面
        try:
            code=request.GET["code"]
            month=request.GET["month"]
            time=month.split('-')
            stock_name=ts.realtime.get(code)
            stock = ts.Stock(code)
            stock_month = stock.fetch(int(time[0]),int(time[1]))
            stock_pd = pd.DataFrame(stock_month)
            c=0
            for i in stock_pd.date:
                t=str(i).split('-')
                a=t[1]+'-'+t[2].split(' ')[0]
                stock_pd.date[c]=a
                c+=1
            stock_pd = stock_pd.set_index('date')
            plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta'] 
            plt.rcParams['axes.unicode_minus'] = False
            fig = plt.figure(figsize=(21, 12))
            plt.plot(stock_pd.close, '-' , label="收盤價")
            plt.plot(stock_pd.open, '-' , label="開盤價")
            plt.title('{}{} 開盤/收盤價曲線'.format(stock_name['info']['name'],time[0]),loc='left',fontsize=30)
            plt.xlabel('日期',fontsize=25)
            plt.ylabel('金額',fontsize=25)
            plt.xticks(fontsize=18,rotation=-30)
            plt.yticks(fontsize=18)
            plt.grid(True, axis='y')
            plt.legend(fontsize=30)
            fig.savefig('D:/Demo_Django/static/images/image.png')
            return render(request,'get_image_new.html',locals())
        except:
            text = "輸入的資料有誤，請重新輸入"
            return render(request,'error.html',locals())


def our_database(n,y,m):#如果股票資料存在於我們的資料庫，就用此函數製圖
    if int(y)==2020 and int(m)<6:#判定資料的年月是否符合資料庫
        return 0
    if int(y)==2021 and int(m)>6:
        return 0
    if int(y)!=2020 and int(y)!=2021:
        return 0
    import sqlite3
    what_we_have=['1201','2353','2330','2498','2380','2412','2427','2603','4904','3045']#儲存股票代碼的list
    name=['味全','宏碁','台積電','宏達電','虹光','中華電','三商電','長榮','遠傳','台灣大']#儲存股票名稱的list
    count=0#判定目前是第幾個股票
    for i in what_we_have:#走訪每個股票代碼
        if n==i:#如果存在就抓取資料
            conn=sqlite3.connect('D:/Demo_Django/db.sqlite3')#連接資料庫
            cursor=conn.cursor()
            cursor.execute("SELECT open, close,date FROM trips_post where company_name=='{}'".format(name[count]+i))#抓取資料
            rows=cursor.fetchall()
            open,close,date=[],[],[]#儲存繪圖用的資料
            for j in rows:#走訪股票的每筆資料
                l=list(j)
                t=l[2].split("-")#轉換為需要的格式
                if t[0]==y and t[1]==m:#查看資料日期是否符合
                    l[0],l[1]=float(l[0]),float(l[1])#轉換格式並儲存
                    l[2]=t[1]+'-'+t[2]
                    open.append(l[0])
                    close.append(l[1])
                    date.append(l[2])
            plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta'] #字體
            plt.rcParams['axes.unicode_minus'] = False
            fig = plt.figure(figsize=(21, 12))#圖大小
            plt.plot(date,open, '-' , label="收盤價")#open的折線圖
            plt.plot(date,close, '-' , label="開盤價")#close的折線圖
            plt.title('{}{} 開盤/收盤價曲線'.format(name[count],y),loc='left',fontsize=30)#標題
            plt.xlabel('日期',fontsize=25)#Ｘ軸標題
            plt.ylabel('金額',fontsize=25)#Ｙ軸標題
            plt.xticks(fontsize=18,rotation=-30)#Ｘ軸項目設定
            plt.yticks(fontsize=18)#Ｙ軸項目設定
            plt.grid(True, axis='y')#輔助線設定
            plt.legend(fontsize=30)#圖例設定
            fig.savefig('D:/Demo_Django/static/images/image.png')#儲存圖片
            return 1
        count+=1
    count=0
    for i in name:#走訪每個股票名稱
        if n==i:
            conn=sqlite3.connect('D:/Demo_Django/db.sqlite3')
            cursor=conn.cursor()
            cursor.execute("SELECT open, close,date FROM trips_post where company_name=='{}'".format(i+what_we_have[count]))
            rows=cursor.fetchall()
            open,close,date=[],[],[]
            for j in rows:
                l=list(j)
                t=l[2].split("-")
                if t[0]==y and t[1]==m:
                    l[0],l[1]=float(l[0]),float(l[1])
                    l[2]=t[1]+'-'+t[2]
                    open.append(l[0])
                    close.append(l[1])
                    date.append(l[2])
            plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta'] 
            plt.rcParams['axes.unicode_minus'] = False
            fig = plt.figure(figsize=(21, 12))
            plt.plot(date,open, '-' , label="收盤價")
            plt.plot(date,close, '-' , label="開盤價")
            plt.xlabel('日期',fontsize=25)
            plt.title('{}{} 開盤/收盤價曲線'.format(i,y),loc='left',fontsize=30)
            plt.ylabel('金額',fontsize=25)
            plt.xticks(fontsize=18,rotation=-30)
            plt.yticks(fontsize=18)
            plt.grid(True, axis='y')
            plt.legend(fontsize=30)
            fig.savefig('D:/Demo_Django/static/images/image.png')
            return 1
        count+=1
    return 0
