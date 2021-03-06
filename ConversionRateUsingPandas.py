import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta

conv_data = pd.read_excel('Desktop/Conv_list.xlsx',
                         header=0)
conv_data['indate'] = conv_data['indate'].astype('datetime64') #엑셀의 object type을 datetime64 type로 변환
conv_data['conv_indate'] = conv_data['conv_indate'].astype('datetime64')
conv_data['conv_outdate'] = conv_data['conv_outdate'].astype('datetime64')
#가입일과 전환일 사이의 경과일을 계산하고 30으로 나눔 (month method 를 써도됨)
conv_data['diff']= (conv_data['conv_indate'] - conv_data['indate']).dt.days / 30 + 1  
conv_data['diff']= conv_data['diff'].astype(int)  
#tabulate 를 위해 월 범주 데이터를 만듦 
conv_data['in_month'] = conv_data['indate'].dt.month
#특정 날짜 이후의 가입자를 추출
condition = conv_data['indate'] > '20200101'
conv_data1 = conv_data[condition]
conv_data1.head()

conv = pd.pivot_table(conv_data1,                # 피벗할 데이터프레임
                     index = 'diff',    # 행 위치에 들어갈 열
                     columns = 'in_month',    # 열 위치에 들어갈 열
                     values = 'paramount',     # 데이터로 사용할 열
                     aggfunc = ['count'] ) # 데이터 집계함수
print(conv)
conv.to_excel('Desktop/conv.xlsx')

#특정 가입일 이후 가입자 중 null data (정상사용자) 를 삭제 
condition = ( conv_data['indate'] > '20200101' ) & ( conv_data['conv_outdate'].notnull() == True ) 
conv_data1 = conv_data[condition]

conv_data1['outdiff']= (conv_data1['conv_outdate'] - conv_data1['conv_indate']).dt.days / 30 + 1
conv_data1['outdiff']= conv_data1['outdiff'].astype(int)
conv_data1['conv_inmonth'] = conv_data1['conv_indate'].dt.month


conv_data1.head()

conv = pd.pivot_table(conv_data1,                # 피벗할 데이터프레임
                     index = 'outdiff',    # 행 위치에 들어갈 열
                     columns = 'conv_inmonth',    # 열 위치에 들어갈 열
                     values = 'paramount',     # 데이터로 사용할 열
                     aggfunc = ['count'] ) # 데이터 집계함수
print(conv)

conv.to_excel('Desktop/churn.xlsx')


#전환율에 영향을 주는 변수들에 대한 산점도와 추세선 그리기


from matplotlib import pyplot
plotdata = pd.read_excel('Desktop/Activation.xlsx',
                         header=1)
plotdata.head(5)

y =  plotdata['1개월내 전환율']
x =  plotdata['Activation 율']

# 추세선을 위한 계산 - 1차원의 polynomial(다항식)을 계산하기 위한 코드.
z = np.polyfit(y, x, 1)   # (X,Y,차원) 정의
f = np.poly1d(z)          # 1차원 다항식에 대한 연산을 캡슐화

plotdata.plot.scatter(x='1개월내 전환율', y='Activation 율', color='#ff6600', marker='o')
pyplot.grid()
pyplot.title("Activation rate vs Conversion rate in 1 month")
pyplot.xlabel('Conversion rate in 1 month')              # y축 라벨
pyplot.ylabel('Activation rate')              # x축 라벨
pyplot.plot(y,f(y),'#ff0000')         # 추세선
#pyplot.show()
pyplot.savefig('Desktop/act vs con.png')

y =  plotdata['Activation 대비 1개월내 전환율']
x =  plotdata['Activation 율']

# 추세선을 위한 계산 - 1차원의 polynomial(다항식)을 계산하기 위한 코드.
z = np.polyfit(y, x, 1)   # (X,Y,차원) 정의
f = np.poly1d(z)          # 1차원 다항식에 대한 연산을 캡슐화

plotdata.plot.scatter(x='Activation 대비 1개월내 전환율', y='Activation 율', color='#ff6600', marker='o')
pyplot.grid()
pyplot.title("Activation rate vs Conversion rate in 1 month")
pyplot.xlabel('Conversion rate of activated user')              # y축 라벨
pyplot.ylabel('Activation rate')              # x축 라벨
pyplot.plot(y,f(y),'#ff0000')         # 추세선
#pyplot.show()
pyplot.savefig('Desktop/act vs con_of_activateuser.png')

