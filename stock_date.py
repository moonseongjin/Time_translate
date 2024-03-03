from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import re
from datetime import datetime, timedelta
import pandas as pd
import requests

userid = '이메일@naver.com'  # 네이버 아이디(이메일)를 설정합니다.
userpw = '비밀번호'  # 네이버 비밀번호를 설정합니다. 

driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('https://nid.naver.com/nidlogin.login')

driver.find_element(By.NAME, 'id').click()
pyperclip.copy(userid)
driver.find_element(By.NAME, 'id').send_keys(Keys.CONTROL, 'v')

driver.find_element(By.NAME, 'pw').click()
pyperclip.copy(userpw)
driver.find_element(By.NAME, 'pw').send_keys(Keys.CONTROL, 'v')
driver.find_element(By.CSS_SELECTOR, '#log\.login').click()
driver.get('https://mail.naver.com/v2/folders/0')

linka = driver.find_element(By.PARTIAL_LINK_TEXT, 'Most Anticipated Releases')
linka.click()

# 한글 번역 버튼 클릭
linkb = driver.find_element(By.XPATH, '//*[@id="mail_read_scroll_view"]/div/div[2]/div[1]/button')
linkb.click()

driver.implicitly_wait(5)

# HTML 멘트 가져옴
elements = driver.find_elements(By.CLASS_NAME, 'papago-parent')

# 이미지 가져오기
img_element = driver.find_element(By.CSS_SELECTOR, 'tbody > tr > td > a > img')

# 이미지 결과 출력
img_src = img_element.get_attribute('src')
if img_src:  # 이미지 소스가 있다면
    current_time = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(img_src)
    with open(f'{current_time}.jpg', 'wb') as f:
        f.write(response.content)
        print("이미지 저장 성공!")
    
    
# 한국어 -> 영어로 (이 작업을 하는 이유는 %A %p가 한국어 인식 못함)
def translate_day(day_name):
    days = {
        "월요일": "Monday",
        "화요일": "Tuesday",
        "수요일": "Wednesday",
        "목요일": "Thursday",
        "금요일": "Friday",
        "토요일": "Saturday",
        "일요일": "Sunday"
    }
    return days.get(day_name, "Invalid day")

def translate_ampm(ampm):
    ampm_translation = {
        "오전" : "AM",
        "오후" : "PM"
    }
    return ampm_translation.get(ampm.upper(), "올바르지 않은 입력입니다.")

# 영어 -> 한국어
def rtranslate_day(rday_name):
    rdays = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }
    return rdays.get(rday_name, "Invalid")

def rtranslate_ampm(rampm):
    rampm_translation = {
        "AM" : "오전",
        "PM" : "오후"
    }
    return rampm_translation.get(rampm.upper(), "올바르지 않은 입력입니다.")


# 미국 동부 표준시 문자열을 datetime 객체로 변환하여 14시간을 더하고 다시 문자열로 변환하는 함수
def add_14_hours(est_time_str):
    # 문자열을 datetime 객체로 변환
    est_t = datetime.strptime(est_time_str, '%Y년 %m월 %d일 %A %p %I시 %M분')
    # 14시간 추가
    est_t += timedelta(hours=14)
    # 변환된 시간을 문자열로 반환
    return est_t.strftime('%Y년 %m월 %d일 %A %p %I시 %M분')


# 출력되는 텍스트 중에서 "(동부 표준시)"를 포함하는 문장만 출력
output_texts = ""
for element in elements:
    sentences = element.text.split('.')  # 문장 단위로 나누기
    for sentence in sentences:
        if "(동부 표준시)" in sentence:
            # "경" 단어 제거
            sentence_without_timezone = sentence.replace("경", "").split("(동부 표준시)")[0].strip()
            if "분" not in sentence_without_timezone:
                sentence_without_timezone += " 00분"  # "00분" 추가
            translated_sentence = ""
            for word in sentence_without_timezone.split():
                if word in ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]:
                    translated_sentence += translate_day(word) + " "
                elif word in ["오전", "오후"]:
                    translated_sentence += translate_ampm(word) + " "
                else:
                    translated_sentence += word + " "
            
            output_texts += translated_sentence.strip() + '\n'
            
# 출력 문자를 리스트 형식으로 변환
est_time_list = output_texts.strip().split('\n')

ticker_list = []
est_list = []

for item in est_time_list:
    split_item = re.split(r'는|은', item)  # "는" 또는 "은"으로 분할
    # print(split_item)
    if len(split_item) > 1:
        ticker_list.append(split_item[0].strip())
        est_list.append(split_item[1].strip())
        
#print("기업 명:", ticker_list)
#print("미국 동부 표준:", est_list)

# 문자열로 변환
est_time = '\n'.join(est_list)
#print("미국 동부 표준:")
#print(est)

korea_list = []

# 기업 명과 미국 동부 표준시 출력
for est_time_str in est_list:
    korea_list.append(add_14_hours(est_time_str))

#print(korea_list)

korean_time = ""
for est_time_str in korea_list:
    split_time = est_time_str.split()
    for word in split_time:
        if word in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            korean_time += rtranslate_day(word) + " "
        elif word in ["AM", "PM"]:
            korean_time += rtranslate_ampm(word) + " "
        else:
            korean_time += word + " "
    korean_time += "\n"

#print(est_time)
#print(korean_time)

korean_time_list = korean_time.strip().split('\n')

data = { '기업명' : ticker_list,
        '한국 시간' : korean_time_list

}
# 데이터프레임 생성
df = pd.DataFrame(data)

# '한국 시간' 열을 기준으로 오름차순 정렬
df = df.sort_values(by='한국 시간', ascending=True)

# 엑셀 파일로 저장
df.to_excel('한국 시간.xlsx', index=False)

print("엑셀 파일 저장!")

# WebDriver 종료
driver.quit()