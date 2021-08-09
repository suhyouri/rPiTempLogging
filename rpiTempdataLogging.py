import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import time

# def measure_temp():
#         temp = os.popen("vcgencmd measure_temp").readline()
#         return (temp.replace("temp=",""))

# while True:
#         print(measure_temp())
#         time.sleep(1)

# mytemp = measure_temp()

mymy = 1

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'mydata.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xy6EwLOis4-JMA5bPR4M3sqJQYWuEQLt-joOUwSkWVs/edit#gid=0'

# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('sheet1')

# 행에 데이터 추가하기(맨 마지막행에 자동추가)
worksheet.append_row([mymy, 'new2'])

# # 특정(4번) 행에 데이터 추가하기(사전에 이미 추가하고자 하는 행이 생성되어있어야함)
# worksheet.insert_row(['new1', 'new2', 'new3', 'new4'], 4)

# # 특정(4번) 열에 데이터 추가하기(사전에 이미 추가하고자 하는 행이 생성되어있어야함)
# worksheet.insert_col(['new1', 'new2', 'new3', 'new4'], 2)

# # 시트크기 조정하기
# worksheet.resize(10,4)
