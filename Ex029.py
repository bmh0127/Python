import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# API URL 및 키 설정
api_key = "0252926988"
url = f"https://data.ex.co.kr/openapi/specialAnal/trafficFlowByTime?key={api_key}&type=xml&iStdYear=2023"

# API 요청 보내기
response = requests.get(url)

# 응답 상태 코드 확인
if response.status_code == 200:
    # BeautifulSoup을 사용하여 XML 데이터 파싱
    soup = BeautifulSoup(response.content, 'xml')  # 'xml' 파서 사용

    # 데이터를 저장할 리스트 초기화
    traffic_data = []

    # XML 데이터에서 필요한 정보 추출
    for item in soup.find_all('trafficFlowByTimeLists'):
        sphlDfttCode = int(item.find('sphlDfttCode').text)  # 정수형 변환
        sphlDfttNm = item.find('sphlDfttNm').text
        sphlDfttScopTypeCode = int(item.find('sphlDfttScopTypeCode').text)
        sphlDfttScopTypeNm = item.find('sphlDfttScopTypeNm').text
        stdHour = int(item.find('stdHour').text)
        stdYear = item.find('stdYear').text
        trfl = int(item.find('trfl').text)

        # 추출한 데이터를 리스트에 저장  ( 특수일 코드, 특수일 이름, 특수일 범위 코드, 특수일 범위 이름, 기준 시간, 기준 연도, 교통량 )
        traffic_data.append({
            'sphlDfttCode': sphlDfttCode,
            'sphlDfttNm': sphlDfttNm,
            'sphlDfttScopTypeCode': sphlDfttScopTypeCode,
            'sphlDfttScopTypeNm': sphlDfttScopTypeNm,
            'stdHour': stdHour,
            'stdYear': stdYear,
            'trfl': trfl
        })

    # 특수일 코드(sphlDfttCode) 기준으로 데이터 정렬
    sorted_data = sorted(traffic_data, key=lambda x: x['sphlDfttCode'])

    # 정렬된 결과 출력
    for data in sorted_data:
        print(f"특수일 코드: {data['sphlDfttCode']}")
        print(f"특수일 이름: {data['sphlDfttNm']}")
        print(f"특수일 범위 코드: {data['sphlDfttScopTypeCode']}")
        print(f"특수일 범위 이름: {data['sphlDfttScopTypeNm']}")
        print(f"기준 시간: {data['stdHour']}시")
        print(f"기준 연도: {data['stdYear']}")
        print(f"교통량: {data['trfl']}")
        print("-" * 40)
else:
    print(f"API 요청 실패: 상태 코드 {response.status_code}")

filtered_data = []
# 그래프 그리기

def zz(j:int, h:int):
    result = []
    for data in sorted_data:
        if data['sphlDfttCode'] == j and data['sphlDfttScopTypeCode'] == h:
            result.append(data)  # 조건을 만족하는 데이터를 filtered_data에 추가
    return result

for i in range(1,8):
    filtered_data.append(zz(1,i))

print(filtered_data[0])

x = []
y = []
# 필터링된 데이터 출력
for data in filtered_data[4]:
    x.append(data['stdHour'])
    y.append(data['trfl'])

# 시간에 따라 교통량 변동 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', color='y', label=data['sphlDfttScopTypeNm'])
plt.title('Change in Traffic')
plt.xlabel('Reference Time (Hour)')
plt.ylabel('Traffic')

plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

plt.show()

# 데이터프레임 생성
traffic_data_tbl = pd.DataFrame(sorted_data)

# CSV 파일로 저장 (Windows 호환성을 위한 cp949 인코딩)
traffic_data_tbl.to_csv("./traffic_data_tbl_EXCEL.csv", encoding='cp949', mode='w', index=True)

# CSV 파일로 저장 (UTF-8 인코딩, 다른 운영체제와의 호환성)
traffic_data_tbl.to_csv("./traffic_data_tbl.csv", encoding='utf-8-sig', mode='w', index=True)











