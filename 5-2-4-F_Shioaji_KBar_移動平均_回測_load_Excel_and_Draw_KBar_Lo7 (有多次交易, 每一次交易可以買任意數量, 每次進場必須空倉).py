# 載入必要模組
#import haohaninfo
from order_Lo8 import Record
import numpy as np
from talib.abstract import SMA,EMA, WMA
#import sys
#import indicator_f_Lo2,datetime
import datetime
import pandas as pd
print(pd.__version__)

#df = pd.read_excel("kbars_台積電_1100701_1100708_2.xlsx")

df = pd.read_excel('kbars_1d_TXF_2020-03-23_To_2021-12-31.xlsx')  ## 'kbars_1d_2330_2020-01-02_To_2025-03-04.xlsx','kbars_1d_TXF_2020-03-23_To_2021-12-31.xlsx', "kbars_2330_2022-07-01-2022-07-31.xlsx", 'kbars_1d_MXF_2020-01-02_To_2025-03-04.xlsx'
product = df['product'][0]
#df.columns  ## Index(['Unnamed: 0', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'], dtype='object')
#df = df.drop('Unnamed: 0',axis=1)
df.columns  ## Index(['time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'], dtype='object')
#df['time']
#type(df['time'])  ## pandas.core.series.Series
#df['time'][11]
df.head()

## 畫 KBar 圖
# df.columns = [ i[0].upper()+i[1:] for i in df.columns ]
# df.set_index( "Time" , inplace=True)
# import mplfinance as mpf
# mpf.plot(df,volume=True,addplot=[],type='candle',style='charles')
df.set_index( "time" , inplace=True)
import mplfinance as mpf
mpf.plot(df,volume=True,addplot=[],type='candle',style='charles')

## 將索引 (time) 轉為普通欄位
df = df.reset_index()
#df['open']
# df['time'] = df.index

### 轉化為字典以利使用talib計算技術指標:
# KBar_dic = df.to_dict()
# #type(KBar_dic)
# #KBar_dic.keys()  ## dict_keys(['time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'])
# #KBar_dic['open']
# #type(KBar_dic['open'])  ## dict
# #KBar_dic['open'].values()
# #type(KBar_dic['open'].values())  ## dict_values
# KBar_open_list = list(KBar_dic['open'].values())
# KBar_dic['open']=np.array(KBar_open_list).astype(np.float64)
# #type(KBar_dic['open'])  ## numpy.ndarray
# #KBar_dic['open'].shape  ## (1596,)
# #KBar_dic['open'].size   ##  1596

# KBar_dic['product'] = np.repeat(product, KBar_dic['open'].size)
# #KBar_dic['product'].size   ## 1596
# #KBar_dic['product'][0]      ## 'tsmc'

# KBar_time_list = list(KBar_dic['time'].values())
# KBar_time_list = [i.to_pydatetime() for i in KBar_time_list] ## Timestamp to datetime
# KBar_dic['time']=np.array(KBar_time_list)

# # KBar_time_list[0]        ## Timestamp('2022-07-01 09:01:00')
# # type(KBar_time_list[0])  ## pandas._libs.tslibs.timestamps.Timestamp
# #KBar_time_list[0].to_pydatetime() ## datetime.datetime(2022, 7, 1, 9, 1)
# #KBar_time_list[0].to_numpy()      ## numpy.datetime64('2022-07-01T09:01:00.000000000')
# #KBar_dic['time']=np.array(KBar_time_list)
# #KBar_dic['time'][80]   ## Timestamp('2022-09-01 23:02:00')

# KBar_low_list = list(KBar_dic['low'].values())
# KBar_dic['low']=np.array(KBar_low_list).astype(np.float64)

# KBar_high_list = list(KBar_dic['high'].values())
# KBar_dic['high']=np.array(KBar_high_list).astype(np.float64)

# KBar_close_list = list(KBar_dic['close'].values())
# KBar_dic['close']=np.array(KBar_close_list).astype(np.float64)

# KBar_volume_list = list(KBar_dic['volume'].values())
# KBar_dic['volume']=np.array(KBar_volume_list)

# KBar_amount_list = list(KBar_dic['amount'].values())
# KBar_dic['amount']=np.array(KBar_amount_list)

    
    
    
    
def toDictionary(df):
    KBar_dic = df.to_dict()
    #type(KBar_dic)
    #KBar_dic.keys()  ## dict_keys(['time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'])
    #KBar_dic['open']
    #type(KBar_dic['open'])  ## dict
    #KBar_dic['open'].values()
    #type(KBar_dic['open'].values())  ## dict_values
    KBar_open_list = list(KBar_dic['open'].values())
    KBar_dic['open']=np.array(KBar_open_list).astype(np.float64)
    #type(KBar_dic['open'])  ## numpy.ndarray
    #KBar_dic['open'].shape  ## (1596,)
    #KBar_dic['open'].size   ##  1596
    
    KBar_dic['product'] = np.repeat(product, KBar_dic['open'].size)
    #KBar_dic['product'].size   ## 1596
    #KBar_dic['product'][0]      ## 'tsmc'
    
    KBar_time_list = list(KBar_dic['time'].values())
    KBar_time_list = [i.to_pydatetime() for i in KBar_time_list] ## Timestamp to datetime
    KBar_dic['time']=np.array(KBar_time_list)
    
    # KBar_time_list[0]        ## Timestamp('2022-07-01 09:01:00')
    # type(KBar_time_list[0])  ## pandas._libs.tslibs.timestamps.Timestamp
    #KBar_time_list[0].to_pydatetime() ## datetime.datetime(2022, 7, 1, 9, 1)
    #KBar_time_list[0].to_numpy()      ## numpy.datetime64('2022-07-01T09:01:00.000000000')
    #KBar_dic['time']=np.array(KBar_time_list)
    #KBar_dic['time'][80]   ## Timestamp('2022-09-01 23:02:00')
    
    KBar_low_list = list(KBar_dic['low'].values())
    KBar_dic['low']=np.array(KBar_low_list).astype(np.float64)
    
    KBar_high_list = list(KBar_dic['high'].values())
    KBar_dic['high']=np.array(KBar_high_list).astype(np.float64)
    
    KBar_close_list = list(KBar_dic['close'].values())
    KBar_dic['close']=np.array(KBar_close_list).astype(np.float64)
    
    KBar_volume_list = list(KBar_dic['volume'].values())
    KBar_dic['volume']=np.array(KBar_volume_list)
    
    KBar_amount_list = list(KBar_dic['amount'].values())
    KBar_dic['amount']=np.array(KBar_amount_list)

    return KBar_dic


KBar_dic = toDictionary(df)


# 建立部位管理物件
OrderRecord=Record() 
# 取得回測參數、移動停損點數
# StartDate=sys.argv[1]
# EndDate=sys.argv[2]
# LongMAPeriod=int(sys.argv[3])
# ShortMAPeriod=int(sys.argv[4])
# MoveStopLoss=float(sys.argv[5])

#StartDate='20170330'
#EndDate='20170331'
LongMAPeriod=10
ShortMAPeriod=2
MoveStopLoss=10  ##  如果是大小台指期貨, 代表大盤點數, 非TWD

# 回測取報價物件
KBar_dic['MA_long']=SMA(KBar_dic,timeperiod=LongMAPeriod)
KBar_dic['MA_short']=SMA(KBar_dic,timeperiod=ShortMAPeriod)
Order_Quantity=1  

# 開始回測
for n in range(0,len(KBar_dic['time'])-1):
    # 先判斷long MA的上一筆值是否為空值 再接續判斷策略內容
    if not np.isnan( KBar_dic['MA_long'][n-1] ) :
        ## 進場: 如果無未平倉部位
        #Order_Quantity=1
        if OrderRecord.GetOpenInterest()==0 :
            #Order_Quantity=1
            # 多單進場: 黃金交叉: short MA 向上突破 long MA
            if KBar_dic['MA_short'][n-1] <= KBar_dic['MA_long'][n-1] and KBar_dic['MA_short'][n] > KBar_dic['MA_long'][n] :
                #rder_Quantity=1
                OrderRecord.Order('Buy', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],Order_Quantity)
                OrderPrice = KBar_dic['open'][n+1]  ## 大盤點數, 非TWD
                StopLossPoint = OrderPrice - MoveStopLoss
                continue
            # 空單進場:死亡交叉: short MA 向下突破 long MA
            if KBar_dic['MA_short'][n-1] >= KBar_dic['MA_long'][n-1] and KBar_dic['MA_short'][n] < KBar_dic['MA_long'][n] :
                #Order_Quantity=1
                OrderRecord.Order('Sell', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],Order_Quantity)
                OrderPrice = KBar_dic['open'][n+1]  ## 大盤點數, 非TWD
                StopLossPoint = OrderPrice + MoveStopLoss
                continue
        ## 出場:
            
        ## 多單出場: 如果有多單部位   
        elif OrderRecord.GetOpenInterest()>0:
            ## 結算平倉(期貨才使用, 股票除非是下市櫃)
            if KBar_dic['product'][n+1] != KBar_dic['product'][n] :
                OrderRecord.Cover('Sell', KBar_dic['product'][n],KBar_dic['time'][n],KBar_dic['close'][n],OrderRecord.GetOpenInterest())
                continue
            # 更新停損價位 (移動停損點)
            if KBar_dic['close'][n] - MoveStopLoss > StopLossPoint :
                StopLossPoint = KBar_dic['close'][n] - MoveStopLoss
            # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
            elif KBar_dic['close'][n] < StopLossPoint :
                OrderRecord.Cover('Sell', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],OrderRecord.GetOpenInterest())
                continue
        # 空單出場: 如果有空單部位
        elif OrderRecord.GetOpenInterest()<0:
            ## 結算平倉(期貨才使用, 股票除非是下市櫃)
            if KBar_dic['product'][n+1] != KBar_dic['product'][n] :
           
                OrderRecord.Cover('Buy', KBar_dic['product'][n],KBar_dic['time'][n],KBar_dic['close'][n],-OrderRecord.GetOpenInterest())
                continue
            # 更新停損價位 (移動停損)
            if KBar_dic['close'][n] + MoveStopLoss < StopLossPoint :
                StopLossPoint = KBar_dic['close'][n] + MoveStopLoss
            # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
            elif KBar_dic['close'][n] > StopLossPoint :
                OrderRecord.Cover('Buy', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],-OrderRecord.GetOpenInterest())
                continue
                


### 繪製: 長短移動平均線, KBar, 進場出場點位 (多空皆有)

## 將K線轉為DataFrame
def KbarToDf(KBar_dic):
    # 將K線 Dictionary 轉換成 Dataframe
    Kbar_df=pd.DataFrame(KBar_dic)
    # 將 Dataframe 欄位名稱轉換
    Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
    # 將 Time 欄位設為索引
    Kbar_df.set_index( "Time" , inplace=True)
    # 回傳
    return Kbar_df

## 繪製K線圖
def ChartKBar(KBar_dic,addp=[],volume_enable=True):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar_dic)
    # 開始繪圖
    mpf.plot(Kbar_df,volume=volume_enable,addplot=addp,type='candle',style='charles')

## 繪製K線圖以及下單紀錄
def ChartOrder(KBar_dic,TR,addp=[],volume_enable=True):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar_dic)
    ### 造 addp list
    # 買(多)方下單點位紀錄
    BTR = [ i for i in TR if i[0]=='Buy' or i[0]=='B' ]
    BuyOrderPoint = [] 
    BuyCoverPoint = []
    for date,value in Kbar_df['Close'].items():
        # 買方進場
        if date in [ i[2] for i in BTR ]:
            BuyOrderPoint.append( Kbar_df['Low'][date] * 0.999 )
        else:
            BuyOrderPoint.append(np.nan)
        # 買方出場
        if date in [ i[4] for i in BTR ]:
            BuyCoverPoint.append( Kbar_df['High'][date] * 1.001 )
        else:
            BuyCoverPoint.append(np.nan)
    # 將下單點位加入副圖物件
    if [ i for i in BuyOrderPoint if not np.isnan(i) ] !=[]:
        addp.append(mpf.make_addplot(BuyOrderPoint,scatter=True,markersize=50,marker='^',color='red'))  ## 200
        addp.append(mpf.make_addplot(BuyCoverPoint,scatter=True,markersize=50,marker='v',color='blue')) ## 200
    # 賣(空)方下單點位紀錄
    STR = [ i for i in TR if i[0]=='Sell' or i[0]=='S' ]
    SellOrderPoint = [] 
    SellCoverPoint = []
    for date,value in Kbar_df['Close'].items():
        # 賣方進場
        if date in [ i[2] for i in STR ]:
            SellOrderPoint.append( Kbar_df['High'][date] * 1.001 )
        else:
            SellOrderPoint.append(np.nan)
        # 賣方出場
        if date in [ i[4] for i in STR ]:
            SellCoverPoint.append( Kbar_df['Low'][date] * 0.999 )
        else:
            SellCoverPoint.append(np.nan)
    # 將下單點位加入副圖物件
    if [ i for i in SellOrderPoint if not np.isnan(i) ] !=[]:
        addp.append(mpf.make_addplot(SellOrderPoint,scatter=True,markersize=50,marker='v',color='green'))  ## 200
        addp.append(mpf.make_addplot(SellCoverPoint,scatter=True,markersize=50,marker='^',color='pink'))   ## 200
    # 開始繪圖 (將以上造的addp帶入以下)
    ChartKBar(KBar_dic,addp,volume_enable)  ## 多單進場: red向上 進, blue向下 出; 空單進場:green 向下進, pink 向上出

## 繪製K線圖加上MA以及下單紀錄
def ChartOrder_MA(KBar_dic,TR):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar_dic)
    # 定義指標副圖
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['MA_long'],color='red'))
    addp.append(mpf.make_addplot(Kbar_df['MA_short'],color='yellow'))
    # 繪製指標、下單圖
    ChartOrder(KBar_dic,TR,addp)


#from chart import ChartOrder_MA
ChartOrder_MA(KBar_dic,OrderRecord.GetTradeRecord())

KBar_dic.keys()



## 計算績效:
OrderRecord.GetTradeRecord()  ## 交易紀錄清單
len(OrderRecord.GetTradeRecord())  ## 189
OrderRecord.GetProfit()       ## 利潤清單
OrderRecord.GetTotalProfit()  ## 淨利
OrderRecord.GetWinRate()      ## 勝率
OrderRecord.GetAccLoss()      ## 最大連續虧損
OrderRecord.GetMDD()          ## 最大資金回落(MDD)=最大 "累計盈虧(TWD,點數)" 回落(MDD)




# KBar_dic['product'][n+1]  ## 'tsmc'
# len(KBar_dic['product'])  ## 1596
# type(KBar_dic)  ##dict
# type(OrderRecord.GetTradeRecord())  ## list
# len(OrderRecord.GetTradeRecord()) ##1


### Pandas DataFrame iteritems() Method:
import pandas as pd
data = {
  "firstname": ["Sally", "Mary", "John"],
  "age": [50, 40, 30]
}
df = pd.DataFrame(data)
df.head()

for x, y in df["firstname"].iteritems():
  print(x)
  print(y)
  
for x, y in df["age"].iteritems():
  print(x)
  print(y)