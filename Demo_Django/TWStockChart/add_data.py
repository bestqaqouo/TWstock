from django.test import TestCase
import sqlite3
import pandas as pd

# Create your tests here.

stocknumber = ["0050","2330","2884","1101","1102","2002","2412","2823","5880","2892"]
for k in stocknumber:
    conn = sqlite3.connect('stock'+k+'.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE stock%s(Date, Capacity, Turnover, Open, High, Low, Close, Change, Transcation)'%k)
    conn.commit()

    for i in range(6,13):
        df = pd.read_csv('D:/csv/0050/0050 2021 '+str(i)+'月'+'.csv', index_col=[0])

        df.tosql('stock'+k, conn, if_exists='append', index=False)
    for j in range(1,7):
        df = pd.read_csv('D:/csv')