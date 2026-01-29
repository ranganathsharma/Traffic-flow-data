import os
import pandas as pd

# Setting the path where the data will be downloaded

path = '...data\\Counter' 

#Enter the dates
#Date range should not be more than seven days
start_date='2019-12-01'
End_date='2019-12-07'

#Enter the counter Id
location=1506 
#***********************************************

#Enter the direction of traffic as South bound or North boun or West bound or East bound
direction='South bound' 
#***********************************************

#Enter the speedlimit 
vf=120 #kmph

# import pandas as pd
# import datetime

def url(t):
    format2=t.strftime("%Y-%m-%d")
    format1=t.strftime("%Y/%m/%d")
    filename='https://data.tii.ie/Datasets/TrafficCountData/'+ format1 + '/per-vehicle-records-' + format2 +'.csv'
    return filename

#download selected days data and write to csv
def download(start_date, End_date):
    temp1=pd.date_range(start_date,End_date, freq='D') 
    filelist = filelist=os.listdir(path)
    for i in range(0,temp1.size):
        data = pd.read_csv(url(temp1[i]))
        tempname=temp1[i].strftime("%Y-%m-%d")+ '.csv'
        if tempname not in filelist:
            data.to_csv(f'{path}\\{tempname}') 
        else:
            pass
        print('Download completed')

# clearing temporary variables
def clear(variables):
    for var in variables:
        del var

#removing unwanted columns and formatting datetime       
def process(data):
    data['Datetime']=data.year.astype(str)+ '-' +data.month.astype(str)+'-'+data.day.astype(str)+ ' ' + data.hour.astype(str)+ ':' + data.minute.astype(str) + ':' + data.second.astype(str)
    data['Datetime']=pd.to_datetime(data['Datetime'].astype(str), format='%Y-%m-%d %H:%M:%S')
    data1 = data[['Datetime', 'cosit' ,'classname', 'lanename', 'speed', 'headway']].copy()
    # data1['lanename'] = data1['lanename'].str.replace('\d+', '')
    data1.set_index('Datetime', inplace=True)
    return data1

#splitting directions of traffic
def direction(data3):
    if 'Southbound 2' in data3['lanename'].unique():
        searchfor_s=['Southbound ' + str(i + 1) for i in range(0,4)]
    elif 'Southbound' in data3['lanename'].unique():
        searchfor_s = ['Southbound']
    elif 'Westbound 2' in data3['lanename'].unique():
        searchfor_s=['Westbound ' + str(i + 1) for i in range(0,4)]
    elif 'Westbound' in data3['lanename'].unique():
        searchfor_s = ['Westbound']
    else:
        searchfor_s=[]
    return searchfor_s

#Dowload the counter data 
# download(start_date, End_date) # Activate to download the data
filelist=os.listdir(path)

# filelist

def processing():
    #Data processing block 1
    print('Data is getting prepared')
    dfseries=[]
    result=pd.DataFrame()
    data=pd.DataFrame()
    for file in filelist:
        data =pd.read_csv(f'{path}\\{file}') #reading a csv
        data2=process(data) #removing unwanted columns and formatting datetime
        data3=data2[(data2['cosit']==location)]
        searchfor=direction(data3)
        data4=data3[data3['lanename'].str.contains('|'.join(searchfor))]
        dfseries.append(data4)
        clear(['data', 'data2', 'data3', 'data4'])
        result= pd.concat(dfseries)
        clear(['dfseries'])
    print('Data preparation completed')

    #Data processing block 2
    #Estimation of aggregated flow and speed
    data=result
    flow=[]
    speed=[]


    flow.append(data['classname'].resample('15T').count()) #Change aggregation using H - hourly, T- mins, D - days
    speed.append(data['speed'].resample('15T').mean())
    merged_flow = pd.concat(flow)
    merged_speed = pd.concat(speed)

    #database preparation
    merged=pd.concat([merged_flow, merged_speed], axis=1)
    merged.columns =['HourlyFlow','meanspeed']

    merged.to_csv('Output.csv')
    print('Data Processing completed')
    print('Results are saved into the Processedfiles directory')
    pass

processing()