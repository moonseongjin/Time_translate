from datetime import datetime, timedelta
import locale

# 주어진 날짜와 시간 문자열
input_date_string = "2024년 1월 30일 화요일 오후 4시 5분"

# "분"이 포함되어 있는지 체크
if "분" in input_date_string:
    # "분"이 포함되어 있으면 분을 포함한 포맷 문자열 사용
    format_str = "%Y년 %m월 %d일 %A %p %I시 %M분"
else:
    # "분"이 포함되어 있지 않으면 분을 뺀 포맷 문자열 사용
    format_str = "%Y년 %m월 %d일 %A %p %I시"

# 로케일을 한국어로 설정
locale.setlocale(locale.LC_TIME, 'ko_KR')

# 사용자 정의 포맷으로 문자열을 datetime 객체로 변환
input_date = datetime.strptime(input_date_string, format_str)

# 14시간을 더함
korea_time = input_date + timedelta(hours=14)

# 출력 형식 지정
output_format = "%Y년 %m월 %d일 %A %p %I시 %M분" if "분" in input_date_string else "%Y년 %m월 %d일 %A %p %I시"

# 결과 출력
print("미국 동부 표준시:", input_date.strftime(output_format))
print("대한민국 시간:", korea_time.strftime(output_format))