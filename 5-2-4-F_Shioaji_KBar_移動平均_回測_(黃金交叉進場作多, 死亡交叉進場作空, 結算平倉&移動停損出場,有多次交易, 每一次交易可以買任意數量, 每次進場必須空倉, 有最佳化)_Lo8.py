#%%
############################################
##### 載入必要模組
############################################

#import haohaninfo
from order_Lo13 import *
import numpy as np
from talib.abstract import SMA,EMA, WMA
#import sys
import indicator_f_Lo2,datetime
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm


#%%
############################################
##### 讀入資料
############################################

df = pd.read_excel("kbars_1d_2330_2020-01-02_To_2025-03-04.xlsx", index_col=0)
#df = pd.read_excel('kbars_1d_TXF_2020-03-23_To_2025-03-14.xlsx', index_col=0)  ## 'kbars_1d_2330_2020-01-02_To_2025-03-04.xlsx','kbars_1d_TXF_2020-03-23_To_2025-03-14.xlsx', "kbars_2330_2022-07-01-2022-07-31.xlsx", 'kbars_1d_MXF_2020-01-02_To_2025-03-04.xlsx'
# product = df['product'][0]
#df.columns  ## Index(['Unnamed: 0', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'], dtype='object')
#df = df.drop('Unnamed: 0',axis=1)
df.columns  ## Index(['time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'], dtype='object')
#df['time']
#type(df['time'])  ## pandas.core.series.Series
#df['time'][11]
df.head()



#%%
############################################
##### 定義相關函數
############################################

#### 轉化為字典以利使用talib計算技術指標
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
    
    KBar_dic['product'] = np.repeat(df['product'][0], KBar_dic['open'].size)
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


#### 定義回測函數
### 訂購數量 Order_Quantity 的單位是口(期貨) or 股(股票)
def back_test(OrderRecord, KBar_dic, LongMAPeriod=10, ShortMAPeriod=2, MoveStopLoss=10, Order_Quantity=1,StopLossPoint=0):
    
    # 回測取報價物件
    KBar_dic['MA_long']=SMA(KBar_dic,timeperiod=int(LongMAPeriod))
    KBar_dic['MA_short']=SMA(KBar_dic,timeperiod=int(ShortMAPeriod))
    
    # 開始回測
    for n in range(0,len(KBar_dic['time'])-1):
        # 先判斷long MA的上一筆值是否為空值 再接續判斷策略內容
        if not np.isnan( KBar_dic['MA_long'][n-1] ) :
            ## 進場: 如果無未平倉部位
            #Order_Quantity=1
            if GetOpenInterest(OrderRecord.OpenInterestQty)==0 :
                #Order_Quantity=1
                # 多單進場: 黃金交叉: short MA 向上突破 long MA
                if KBar_dic['MA_short'][n-1] <= KBar_dic['MA_long'][n-1] and KBar_dic['MA_short'][n] > KBar_dic['MA_long'][n] :
                    #rder_Quantity=1
                    OrderRecord.Order('Buy', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],Order_Quantity)
                    OrderPrice = KBar_dic['open'][n+1]  ## 單位: 大盤點數(大小台指) or TWD(股票 或 股票期貨)
                    StopLossPoint = OrderPrice - MoveStopLoss
                    continue
                # 空單進場:死亡交叉: short MA 向下突破 long MA
                if KBar_dic['MA_short'][n-1] >= KBar_dic['MA_long'][n-1] and KBar_dic['MA_short'][n] < KBar_dic['MA_long'][n] :
                    #Order_Quantity=1
                    OrderRecord.Order('Sell', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],Order_Quantity)
                    OrderPrice = KBar_dic['open'][n+1]  ## 單位: 大盤點數(大小台指) or TWD(股票 或 股票期貨)
                    StopLossPoint = OrderPrice + MoveStopLoss
                    continue
            ## 出場:
                
            ## 多單出場: 如果有多單部位   
            elif GetOpenInterest(OrderRecord.OpenInterestQty)>0:
                ## 結算平倉(期貨才使用, 股票除非是下市櫃)
                if KBar_dic['product'][n+1] != KBar_dic['product'][n] :
                    OrderRecord.Cover('Sell', KBar_dic['product'][n],KBar_dic['time'][n],KBar_dic['close'][n], GetOpenInterest(OrderRecord.OpenInterestQty))
                    continue
                # 更新停損價位 (移動停損點)
                if KBar_dic['close'][n] - MoveStopLoss > StopLossPoint :
                    StopLossPoint = KBar_dic['close'][n] - MoveStopLoss
                # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
                elif KBar_dic['close'][n] < StopLossPoint :
                    OrderRecord.Cover('Sell', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1], GetOpenInterest(OrderRecord.OpenInterestQty))
                    continue
            # 空單出場: 如果有空單部位
            elif GetOpenInterest(OrderRecord.OpenInterestQty)<0:
                ## 結算平倉(期貨才使用, 股票除非是下市櫃)
                if KBar_dic['product'][n+1] != KBar_dic['product'][n] :
               
                    OrderRecord.Cover('Buy', KBar_dic['product'][n],KBar_dic['time'][n],KBar_dic['close'][n],-GetOpenInterest(OrderRecord.OpenInterestQty))
                    continue
                # 更新停損價位 (移動停損)
                if KBar_dic['close'][n] + MoveStopLoss < StopLossPoint :
                    StopLossPoint = KBar_dic['close'][n] + MoveStopLoss
                # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
                elif KBar_dic['close'][n] > StopLossPoint :
                    OrderRecord.Cover('Buy', KBar_dic['product'][n+1],KBar_dic['time'][n+1],KBar_dic['open'][n+1],-GetOpenInterest(OrderRecord.OpenInterestQty))
                    continue
    CumulativeCapitalRate_series, final_return = GetCumulativeCapitalRate_finalReturn(OrderRecord.Capital_rate)
    return CumulativeCapitalRate_series, final_return 


#### 畫圖相關函數:
### 將K線轉為DataFrame
def KbarToDf(KBar_dic):
    # 將K線 Dictionary 轉換成 Dataframe
    Kbar_df=pd.DataFrame(KBar_dic)
    # 將 Dataframe 欄位名稱轉換(首字母大寫)
    Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
    # 將 Time 欄位設為索引
    Kbar_df.set_index( "Time" , inplace=True)
    # 回傳
    return Kbar_df

### 繪製K線圖
def ChartKBar(title, KBar_dic,addp=[],volume_enable=True):
    ## 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar_dic)
    
    ## 指定你電腦上中文字型的路徑（例如微軟雅黑）
    font_path = "C:/Windows/Fonts/msyh.ttc"  # Microsoft YaHei
    font_prop = fm.FontProperties(fname=font_path)
    
    ## 開始繪圖
    fig, axlist = mpf.plot(Kbar_df,volume=volume_enable,addplot=addp,type='candle',style='charles', returnfig=True, title=title)
    fig.suptitle(title, fontproperties=font_prop, fontsize=16)
    plt.show()

### 繪製K線圖以及下單紀錄
def ChartOrder(title, KBar_dic,TR,addp=[],volume_enable=True):
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
    ChartKBar(title, KBar_dic,addp,volume_enable)  ## 多單進場: red向上 進, blue向下 出; 空單進場:green 向下進, pink 向上出

### 繪製K線圖加上MA以及下單紀錄
def ChartOrder_MA(title, KBar_dic,TR):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar_dic)
    # 定義指標副圖
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['MA_long'],color='red'))
    addp.append(mpf.make_addplot(Kbar_df['MA_short'],color='yellow'))
    # 繪製指標、下單圖
    ChartOrder(title, KBar_dic,TR,addp)


#### 定義最佳化函數
def optimizeMA(OrderRecord,KBar_dic,period_range_Long, period_range_Short, MoveStopLoss=10, Order_Quantity=1, isFuture='False', G_commission=0.001425):

    openPrice=KBar_dic['open']
    closePrice=KBar_dic['close']  
    bestcapital=-1000000
    bestcapital_series=[]
    bestperiodLong=0
    bestperiodShort=0
    for periodLong in period_range_Long:
        for periodShort in period_range_Short:
            if(periodLong<=periodShort):
                continue

            ##
            ### 重新建立部位管理物件 
            if isFuture=='True' or isFuture=='true':   ## 期貨商品
                OrderRecord=Record(G_spread=3.628e-4, G_tax=0.00002, G_commission=G_commission, isFuture=True)  ## G_commission 單位是TWD   ##(不要)G_commission在各別期貨商品要重新計算=手續費價格(TW)/期貨商品價值(TW)
            else: ## 股票商品:
                OrderRecord=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=0.001425, isFuture=False)


            ##對訊號進行回測
            CumulativeCapitalRate_series, final_return = back_test(OrderRecord, KBar_dic, periodLong, periodShort, MoveStopLoss, Order_Quantity)
            #CumulativeCapitalRate_series, final_return = GetCumulativeCapitalRate_finalReturn(OrderRecord.Capital_rate)
            #如果結果比之前更好,就記錄下來
            if(bestcapital<(final_return+1)):
                #print(f'old capital:{bestcapital}, new capital:{final_return+1}')
                bestcapital = final_return+1
                bestCumulativeCapitalRate_series = CumulativeCapitalRate_series
                bestperiodLong=periodLong
                bestperiodShort=periodShort
    return bestcapital,bestCumulativeCapitalRate_series,(bestperiodLong,bestperiodShort)


#%%
############################################
##### 畫 KBar 圖
############################################

# df.columns = [ i[0].upper()+i[1:] for i in df.columns ]
# df.set_index( "Time" , inplace=True)
# import mplfinance as mpf
# mpf.plot(df,volume=True,addplot=[],type='candle',style='charles')

#### 將 'time' column設定為index
df.set_index( "time" , inplace=True)

#### 畫圖
### 指定你電腦上中文字型的路徑（例如微軟雅黑）
font_path = "C:/Windows/Fonts/msyh.ttc"  # Microsoft YaHei
font_prop = fm.FontProperties(fname=font_path)
### 畫圖
# mpf.plot(df,volume=True,addplot=[],type='candle',style='charles', title='股票K線圖標題')
fig, axlist = mpf.plot(df,volume=True,addplot=[],type='candle',style='charles', returnfig=True)
fig.suptitle('K線圖', fontproperties=font_prop, fontsize=16)
plt.show()

#### 將索引 (time) 轉為普通欄位
df = df.reset_index()
#df['open']
# df['time'] = df.index



#%%
############################################
##### 轉化為字典以利使用talib計算技術指標:
############################################
KBar_dic = toDictionary(df)
#KBar_dic.keys()  ## dict_keys(['time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product', 'MA_long', 'MA_short'])



#%%
############################################
##### 進行回測
############################################

#### 建立部位管理物件
### Record類別的建構子__init__() 參數有下列期貨商品預設值, 視需要調整: G_spread=3.628e-4, G_tax=0.00002, G_commission=4.411e-5, isFuture=True    
### 例如買股票時: OrderRecord=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=0.001425, isFuture=False)

### 選擇 期貨還是股票:
isFuture = input("是否為期貨商品 ? 是: 輸入'True' 或 'true'; 否: 輸入'False' ") 
# isFuture=True   ## 如果是股票 isFuture=False   
### 輸入期貨商品手續費(如果是期貨) & 建立部位管理物件 
if isFuture=='True' or isFuture=='true':   ## 期貨商品
    G_commission = float(input("請輸入你的期貨商品的手續費用(TW)(TXF:20,MXF:12.5,FXF:20)(查詢 https://reurl.cc/RYy7Vn) "))   ## 期貨暨選擇權商品相關費用表 https://www.taifex.com.tw/cht/4/feeSchedules
    OrderRecord=Record(G_spread=3.628e-4, G_tax=0.00002, G_commission=G_commission, isFuture=True)  ##  G_commission在各別期貨商品要重新計算=手續費價格(TW)/期貨商品價值(TW)
else: ## 股票商品:
    OrderRecord=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=0.001425, isFuture=False)


#### 實際進行回測: LongMAPeriod=10, ShortMAPeriod=2
LongMAPeriod = input("請輸入MA 長週期: ") 
ShortMAPeriod = input("請輸入MA 短週期: ")
CumulativeCapitalRate_series, final_return = back_test(OrderRecord, KBar_dic, LongMAPeriod=LongMAPeriod, ShortMAPeriod=ShortMAPeriod, MoveStopLoss=10, Order_Quantity=1)

#### 繪製回測相關圖: 長短移動平均線, KBar, 進場出場點位 (多空皆有)
### 畫圖: K棒, 長短移動平均線, 進出場點
#from chart import ChartOrder_MA
ChartOrder_MA('K棒,長短移動平均線,進出場點', KBar_dic, GetTradeRecord(OrderRecord.TradeRecord))

#### 計算績效:
###
GetTradeRecord(OrderRecord.TradeRecord)  ## 交易紀錄清單
#len(GetTradeRecord(OrderRecord.TradeRecord))  ## 189
GetProfit(OrderRecord.Profit)       ## 利潤清單
print('淨利: ', GetTotalProfit(OrderRecord.Profit))  ## 淨利
print('勝率: ', GetWinRate(OrderRecord.Profit))      ## 勝率
print('最大連續虧損: ', GetAccLoss(OrderRecord.Profit))      ## 最大連續虧損

### 歷次交易累計本利和清單(以1為初始資金) & 最後總報酬率: 買Order_Quantity "口(for期貨)" or "股(for股票,不是張)". 
## 累計本利和清單(以1為初始資金): 至第i次交易(完成入出場)時,將所有1至i次所有完成入場與出場的交易的本利和相乘
## 最後總報酬率即為:所有完成入場與出場的交易的本利和相乘-1=累計本利和清單最後一個值-1. <說明>計算績效期間(不一定是第一個入場至最後一個出場期間),每根K棒期間的本利和複利計算=前一根K棒週期所得的本利和再度投入下一根K棒週期中計算本利和, 故為複利. 如果是出場期間, 此根K棒本利和=1+0, 如果是入場期間, 此根K棒本利和=1+每根K棒期間投資報酬率.
CumulativeCapitalRate_series, final_return = GetCumulativeCapitalRate_finalReturn(OrderRecord.Capital_rate)
print('總報酬率(複利型): ', final_return)  ## 參考 order_Lo9.py

### MDD:
GetMDD_Profit(OrderRecord.Profit)               ## 最大 "歷次交易累計盈虧(TWD,點數)" 回落: 畫圖時: y軸是 "盈虧(Profit)", x軸是歷次交易的編號
GetMDD_Profit_rate(OrderRecord.Profit_rate)          ## 最大 "歷次交易累計投資報酬率" 回落: 畫圖時: y軸是 "投資報酬率(Profit_rate)", x軸是歷次交易的編號
print('最大的 "累計本利和(以1為初始本金)" 回落: ', GetMDD_CapitalRate1(CumulativeCapitalRate_series))         ## 最大的 "累計本利和(以1為初始本金)" 回落: 畫圖時: y軸是 "累計本利和(以1為初始本金)", x軸是歷次交易的編號
GetMDD_CapitalRate2(CumulativeCapitalRate_series)         ## 最大的 "減少的累計本利和/最大累計本利和": 畫圖時: y軸是 "減少的累計本利和/最大累計本利和(浮動)", x軸是歷次交易的編號

### 產出累計盈虧(TWD,點數)交易績效圖(畫出 "累計盈虧(TWD,點數)清單")
GeneratorProfitChart(OrderRecord.Profit, StrategyName='MA Strategy')

### 產出累計本利和(複利,(以1為初始資金))交易績效圖(畫出 "累計本利和清單(以1為初始資金)")
GeneratorCapitalRateChart(CumulativeCapitalRate_series, StrategyName='MA Strategy')




#%%
############################################
##### 最佳化模型參數
############################################

#### 建立部位管理物件
### Record類別的建構子__init__() 參數有下列期貨商品預設值, 視需要調整: G_spread=3.628e-4, G_tax=0.00002, G_commission=4.411e-5, isFuture=True    
### 例如買股票時: OrderRecord=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=0.001425, isFuture=False)

### 選擇 期貨還是股票:
isFuture = input("是否為期貨商品 ? 是: 輸入'True'; 否: 輸入'False' ") 
# isFuture=True   ## 如果是股票 isFuture=False   
### 輸入期貨商品手續費(如果是期貨) & 建立部位管理物件 
if isFuture=='True' or isFuture=='true':   ## 期貨商品
    G_commission = float(input("請輸入你的期貨商品的手續費用(TW)(TXF:20,MXF:12.5,FXF:20)(查詢 https://reurl.cc/RYy7Vn) "))   ## 期貨暨選擇權商品相關費用表 https://www.taifex.com.tw/cht/4/feeSchedules
    OrderRecord=Record(G_spread=3.628e-4, G_tax=0.00002, G_commission=G_commission, isFuture=True)  ##  G_commission在各別期貨商品要重新計算=手續費價格(TW)/期貨商品價值(TW)
else: ## 股票商品:
    G_commission=0.001425
    OrderRecord=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=G_commission, isFuture=False)


#### 實際進行最佳化參數尋找 
bestcapital,bestCumulativeCapitalRate_series,bestperiod=optimizeMA(OrderRecord, KBar_dic, np.arange(2,100,1,dtype=int), np.arange(2,100,1,dtype=int), MoveStopLoss=10, Order_Quantity=1, isFuture=isFuture, G_commission=G_commission)
#### 呈現最佳化的結果
MDD =GetMDD_CapitalRate1(bestCumulativeCapitalRate_series) 
print('最佳化的報酬率(以1為初始本金):', bestcapital-1)
print('最佳報酬率時的 MDD:', MDD)
print('最佳報酬率時的 MA長週期:', bestperiod[0])  ## 14
print('最佳報酬率時的 MA短週期:', bestperiod[1])  ## 10
#### 畫圖        
#plt.plot(np.log10(bestCumulativeCapitalRate_series),color='green')
plt.plot(bestCumulativeCapitalRate_series,color='green')
#plt.title('Cumulative Capital Rate Series after optimizing(log)')
plt.title('Cumulative Capital Rate Series after optimizing')
plt.show()


#%%
###########################################
##### 計算兩檔商品做成投資組合的報酬率(尚未進行兩組商品以上投資組合的最佳化 !)
############################################

#### 讀入資料
#df = pd.read_excel("kbars_台積電_1100701_1100708_2.xlsx")
df_TXF = pd.read_excel('kbars_1d_TXF_2020-03-23_To_2021-12-31.xlsx')  ## 'kbars_1d_2330_2020-01-02_To_2025-03-04.xlsx','kbars_1d_TXF_2020-03-23_To_2021-12-31.xlsx', "kbars_2330_2022-07-01-2022-07-31.xlsx", 'kbars_1d_MXF_2020-01-02_To_2025-03-04.xlsx'
#product_1 = df_TXF['product'][0]
df_TXF.head()

df_2330 = pd.read_excel('kbars_1d_2330_2020-01-02_To_2025-03-04.xlsx')  ## 'kbars_1d_2330_2020-01-02_To_2025-03-04.xlsx','kbars_1d_TXF_2020-03-23_To_2021-12-31.xlsx', "kbars_2330_2022-07-01-2022-07-31.xlsx", 'kbars_1d_MXF_2020-01-02_To_2025-03-04.xlsx'
#product_2 = df_2330['product'][0]
df_2330 = df_2330.drop('Unnamed: 0',axis=1)
#df_2330.columns
df_2330.head()

#### 選取時間範圍重複的資料
###
df_TXF.set_index( "time" , inplace=True)
df_2330.set_index( "time" , inplace=True)

begin_time = max(df_TXF.index[0],df_2330.index[0])  ## 原來 min
begin_time_s = str(begin_time)
df_TXF = df_TXF[begin_time_s:]
df_2330 = df_2330[begin_time_s:]

df_TXF.reset_index(inplace=True)
df_2330.reset_index(inplace=True)


#### 轉化為字典以利使用talib計算技術指標:
KBar_dic_TXF = toDictionary(df_TXF)
KBar_dic_2330 = toDictionary(df_2330)


#### 進行回測
# ### 建立部位管理物件
# OrderRecord_1=Record(G_tax=0.00002, G_commission=4.411e-5, isFuture=True)
# OrderRecord_2=Record(G_tax=0.003 , G_commission=0.001425, isFuture=False)

### 建立部位管理物件
## 選擇 期貨還是股票:
isFuture_1 = input("商品1是否為期貨商品 ? 是: 輸入'True'; 否: 輸入'False' ") 
## 輸入期貨商品手續費(如果是期貨) & 建立部位管理物件 
if isFuture_1=='True':   ## 期貨商品
    G_commission = float(input("請輸入商品1的期貨商品的手續費用(TW)(TXF:20,MXF:12.5,FXF:20)(查詢 https://reurl.cc/RYy7Vn) "))   ## 期貨暨選擇權商品相關費用表 https://www.taifex.com.tw/cht/4/feeSchedules
    OrderRecord_1=Record(G_spread=3.628e-4, G_tax=0.00002, G_commission=G_commission, isFuture=True)  ##  G_commission在各別期貨商品要重新計算=手續費價格(TW)/期貨商品價值(TW)
else: ## 股票商品:
    OrderRecord_1=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=0.001425, isFuture=False)

## 選擇 期貨還是股票:    
isFuture_2 = input("商品2是否為期貨商品 ? 是: 輸入'True'; 否: 輸入'False' ") 
 ## 輸入期貨商品手續費(如果是期貨) & 建立部位管理物件 
if isFuture_2=='True':   ## 期貨商品
    G_commission = float(input("請輸入商品2的期貨商品的手續費用(TW)(TXF:20,MXF:12.5,FXF:20)(查詢 https://reurl.cc/RYy7Vn) "))   ## 期貨暨選擇權商品相關費用表 https://www.taifex.com.tw/cht/4/feeSchedules
    OrderRecord_2=Record(G_spread=3.628e-4, G_tax=0.00002, G_commission=G_commission, isFuture=True)  ##  G_commission在各別期貨商品要重新計算=手續費價格(TW)/期貨商品價值(TW)
else: ## 股票商品:
    OrderRecord_2=Record(G_spread=3.628e-4, G_tax=0.003, G_commission=0.001425, isFuture=False)




### 各別進行回測: Order_Quantity 必須為整數
CumulativeCapitalRate_series_1, final_return_1 = back_test(OrderRecord_1, KBar_dic_TXF, LongMAPeriod=10, ShortMAPeriod=2, MoveStopLoss=10, Order_Quantity=1)
CumulativeCapitalRate_series_2, final_return_2 = back_test(OrderRecord_1, KBar_dic_TXF, LongMAPeriod=10, ShortMAPeriod=2, MoveStopLoss=10, Order_Quantity=1)

#### 投資組合之平均績效
### 平均總報酬率(複利型)
final_return_MIX = (final_return_1 + final_return_2)*0.5 
CumulativeCapitalRate_series_MIX = CumulativeCapitalRate_series_1+ CumulativeCapitalRate_series_2
print('平均總報酬率(複利型): ', final_return_MIX) 

###
TradeRecord_MIX = GetTradeRecord(OrderRecord_1.TradeRecord)+GetTradeRecord(OrderRecord_2.TradeRecord)  ## 合併之交易紀錄清單
#len(TradeRecord_MIX)  ## 126
#len(GetTradeRecord(OrderRecord_1.TradeRecord))  ## 126
#len(GetTradeRecord(OrderRecord_2.TradeRecord))  ## 0

Profit_list_MIX = GetProfit(OrderRecord_1.Profit) + GetProfit(OrderRecord_2.Profit)      ## 合併之利潤清單
print('平均淨利: ', GetTotalProfit(Profit_list_MIX)*0.5)  ## 平均淨利
if OrderRecord_1.Profit !=[] and OrderRecord_2.Profit !=[]:
    print('平均勝率: ', (GetWinRate(OrderRecord_1.Profit)+GetWinRate(OrderRecord_2.Profit))*0.5)      ## 平均勝率
print('最大連續虧損: ', max(GetAccLoss(OrderRecord_1.Profit),GetAccLoss(OrderRecord_2.Profit)))      ## 最大連續虧損

### MDD:
max(GetMDD_Profit(OrderRecord_1.Profit),GetMDD_Profit(OrderRecord_2.Profit))               ## 投資組合的最大 "歷次交易累計盈虧(TWD,點數)" 回落: 畫圖時: y軸是 "盈虧(Profit)", x軸是歷次交易的編號
max(GetMDD_Profit_rate(OrderRecord_1.Profit_rate),GetMDD_Profit_rate(OrderRecord_2.Profit_rate))          ## 投資組合的最大 "歷次交易累計投資報酬率" 回落: 畫圖時: y軸是 "投資報酬率(Profit_rate)", x軸是歷次交易的編號
print('最大的 "累計本利和(以1為初始本金)" 回落: ', max(GetMDD_CapitalRate1(CumulativeCapitalRate_series_1),GetMDD_CapitalRate1(CumulativeCapitalRate_series_2)))         ## 投資組合的最大的 "累計本利和(以1為初始本金)" 回落: 畫圖時: y軸是 "累計本利和(以1為初始本金)", x軸是歷次交易的編號
max(GetMDD_CapitalRate2(CumulativeCapitalRate_series_1),GetMDD_CapitalRate2(CumulativeCapitalRate_series_2))         ## 投資組合的最大的 "減少的累計本利和/最大累計本利和": 畫圖時: y軸是 "減少的累計本利和/最大累計本利和(浮動)", x軸是歷次交易的編號

### 產出投資組合的平均累計盈虧(TWD,點數)交易績效圖(畫出投資組合的平均 "累計盈虧(TWD,點數)清單")
GeneratorProfitChart([x * 0.5 for x in Profit_list_MIX], StrategyName='MA Strategy')

### 產出投資組合的平均累計本利和(複利,(以1為初始資金))交易績效圖(畫出投資組合的平均 "累計本利和清單(以1為初始資金)")
GeneratorCapitalRateChart([x * 0.5 for x in CumulativeCapitalRate_series_1]+ [x * 0.5 for x in CumulativeCapitalRate_series_2], StrategyName='MA Strategy')

































