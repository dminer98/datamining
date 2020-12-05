import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta

pro_data = pd.read_excel('Desktop/Pro_list.xlsx',
                         header=0)
pro_data['indate'] = pro_data['indate'].astype('datetime64') #엑셀의 object type을 datetime64 type로 변환
pro_data['pro_indate'] = pro_data['pro_indate'].astype('datetime64')
pro_data['pro_outdate'] = pro_data['pro_outdate'].astype('datetime64')
#가입일과 전환일 사이의 경과일을 계산하고 30으로 나눔 (month method 를 써도됨)
pro_data['diff']= (pro_data['pro_indate'] - pro_data['indate']).dt.days / 30 + 1  
pro_data['diff']= pro_data['diff'].astype(int)  
#tabulate 를 위해 월 범주 데이터를 만듦 
pro_data['in_month'] = pro_data['indate'].dt.month
#특정 날짜 이후의 가입자를 추출
condition = pro_data['indate'] > '20200101'
pro_data1 = pro_data[condition]
pro_data1.head()

pro = pd.pivot_table(pro_data1,                # 피벗할 데이터프레임
                     index = 'diff',    # 행 위치에 들어갈 열
                     columns = 'in_month',    # 열 위치에 들어갈 열
                     values = 'paramount',     # 데이터로 사용할 열
                     aggfunc = ['count'] ) # 데이터 집계함수
print(pro)

pro.to_excel('Desktop/프로가입전환.xlsx')
condition = ( pro_data['indate'] > '20200101' ) & ( pro_data['pro_outdate'].notnull() == True ) 
pro_data1 = pro_data[condition]

pro_data1['outdiff']= (pro_data1['pro_outdate'] - pro_data1['pro_indate']).dt.days / 30 + 1
pro_data1['outdiff']= pro_data1['outdiff'].astype(int)
pro_data1['pro_inmonth'] = pro_data1['pro_indate'].dt.month


pro_data1.head()

pro = pd.pivot_table(pro_data1,                # 피벗할 데이터프레임
                     index = 'outdiff',    # 행 위치에 들어갈 열
                     columns = 'pro_inmonth',    # 열 위치에 들어갈 열
                     values = 'paramount',     # 데이터로 사용할 열
                     aggfunc = ['count'] ) # 데이터 집계함수
print(pro)

pro.to_excel('Desktop/프로해지.xlsx')
