Summary. RasberryPi CPU Temp Data Logging to Google Spread Sheet(라즈베리파이 CPU온도 데이터 구글 스프레드시트에 기록하기)
===

# 1. Get RasberryPi CPU Temp data라즈베리파이 온도 데이터 받기
---
- `$ vcgencmd measure_temp` Measure CPU Temperature of Rpi라즈베리파이 CPU온도측정
in Linux of Rpi 라즈베리파이 리눅스에서 작동
- `$ vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'` Extract only the temperature data숫자값만 추출

### 1-1. Get the data by shell script → Save the data to csv.file 쉘스크립트를 이용해 csv에 데이터 저장

1. `$ nano print_temp.sh` Create new shell script(name:print_temp)새 쉘 스크립트 만들기 

    ```bash
    //print_temp.sh 
    #!/bin/bash

    printf "%-15s%5s\n" "TIMESTAMP" "TEMP(degC)"
    printf "%20s\n" "........."

    while true
    do
            temp=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')
            timestamp=$(date '+%D-%T')
            printf "%-15s%5s\n" "$timestamp" "$temp"
    				echo "$timestamp," "$temp" >> test.csv
            sleep 1
    done
    ```

    - echo = print
        - `$ echo “hello world” > test.txt`  console X, txt_file에 저장 O `>` : redirection symbol
        - `$ echo “hello world” | tee test.txt`  console O, txt_file에 저장 O  `tee`
        - `$ echo "hello world" >> test.txt` 파일 뒤에 계속 내용을 이어서 기록하려면? `>>` 를 사용
        - `$ echo ”hello world” | tee -a test.txt` 동시에 파일과 화면에 보이는 걸 계속 이어서 기록
    - sleep = delay(second)
2. `$ chmod +x print_temp.sh` print_temp.sh를 실행파일로 만들기
3. `$ ./print_temp.sh` 실행하기 

### 1-2. 라즈베리파이 CPU온도 아두이노에 보내서 그래프 만들기?

- 라즈베리 파이에서 아두이노 찾기 `$ ls /dev/tty*` 로 비교해보기

    → 찾음 `/dev/ttyACM0` 

- 아두이노 Idle 라즈베리파이에 설치하기

    `$ sudo apt-get install arduino`

    **`$ sudo usermod -a -G tty pi`**

    **`$ sudo usermod -a -G dialout pi`**

- (주의🚨)serial 통신은 rx-tx가 교차되어 둘다 연결되어야 한다.
- 통신코드 `echo "AT" >> /dev/ttyACM0`
- 최종코드

    ```bash
    #!/bin/bash

    printf "%-15s%5s\n" "TIMESTAMP" "TEMP(degC)"
    printf "%20s\n" "........."

    while true
    do
            temp=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')
            timestamp=$(date '+%D-%T')
            printf "%-15s%5s\n" "$timestamp" "$temp"
    				echo "$timestamp," "$temp" >> test.csv
            echo "$timestamp," "$temp" >> /dev/ttyACM0
            sleep 1
    done
    ```

    → 시리얼 통신은 가능 

# 2. Send RasberryPi CPU Temp data to Google SpreadSheet Using Python받은 라즈베리파이 온도 데이터 구글 스프레드 시트로 보내기(파이썬사용)

### 2-1. 맥에서 기본 셋팅(pip, **oauth2client, gspread)**

- 참고URL-1 : [http://hleecaster.com/python-google-drive-spreadsheet-api/](http://hleecaster.com/python-google-drive-spreadsheet-api/)
- **pip** 설치 [https://dora-guide.com/pip-install/](https://dora-guide.com/pip-install/) [https://blog.nachal.com/1530](https://blog.nachal.com/1530)
    - `$ curl [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py) -o [get-pip.py](http://get-pip.py/)`
    - `$ sudo easy_install pip` in Mac
    - `$ sudo apt-get install python3-pip` in Linux
- **oauth2client** 설치
    - `$ pip install pygsheets oauth2client`
- **gspread** 설치
    - `$ pip install gspread`
- **구글 개발자 콘솔**에 접속 - [https://console.developers.google.com](https://console.developers.google.com/)
    - 새 프로젝트 만들기 > 사용자 인증정보 > 서비스 계정 만들기 > json 키 파일 다운로드
        - 받은 json파일이름은 쓰기 쉽게 짧게 고쳐준다
    - json 파일에서 'client_email' 체크 및 복사해두기
    - 'client_email'을 수정할 구글 스프레드 시트에 공유자로 추가
    - 데이터를 추가 할 구글 스프레드 url 복사해두기

### 2-2. 파이썬과 구글스프레드 시트에 데이터 받고, 쓰는 연습

- Get the data from Google Spread Sheet구글 스프레드 시트 데이터 값을 파이썬으로 받아오기 `.acell('')` `row_values(num)` `col_values(num)`
- Write the data to Google Spread Sheet구글 스프레드 시트 데이터 값을 파이썬으로 쓰기 `.update_acell` `.append_row` `.insert_row`
- Create new spreadsheet 스프레드 시트생성 및 권한 공유하기 `.create()` `.add_worksheet()`

# 3. 파이썬에서 온도 저장 및 날짜 방법

- 참고URL : [https://chem.libretexts.org/Courses/Intercollegiate_Courses/Internet_of_Science_Things_(2020)/1%3A_IOST_Modules/1.6%3A_Writing_to_Google_Sheets](https://chem.libretexts.org/Courses/Intercollegiate_Courses/Internet_of_Science_Things_(2020)/1%3A_IOST_Modules/1.6%3A_Writing_to_Google_Sheets)
- 파이썬 실행: `$ python py.py`

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
from datetime import datetime 

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'mydata.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1MmtNLwfFsHORLU49uZcLHT1X9YsquwbZGzeruhsS8Bc/edit#gid=0'

# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('sheet1')

# 날짜와 온도 보내기
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(time)
data = os.popen("vcgencmd measure_temp").readline()
values =[time,data]
worksheet.append_row(values)
```

- 에러메세지(Invalid JWT) 해결

    ```c
    //에러메세지 
    google.auth.exceptions.RefreshError: 
    ('invalid_grant: Invalid JWT: Token must be a short-lived token (60 minutes) 
    and in a reasonable timeframe. 
    Check your iat and exp values in the JWT claim.',
     {'error': 'invalid_grant', 'error_description': 'Invalid JWT: Token must be a short-lived token (60 minutes) and in a reasonable timeframe. 
    Check your iat and exp values in the JWT claim.'})

    -> 시스템 시간 동기화 필요
    $ date 
    시스템 시간 확인 
    ```

    → **시스템 시간 동기화 필요**

    - `$ date`  : 라즈베리파이 시스템 시간 확인 : 현재 시간이랑 라즈베리 파이 시간이 같은지 확인
    - `$ sudo apt-get install rdate`
    - `$ sudo /usr/bin/rdate -s [time.bora.net](http://time.bora.net/)`
    - `$ date` : 다시 동기화 됐는지 체크
