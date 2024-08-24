import requests
from bs4 import BeautifulSoup
import csv
import time

# 1세대 포켓몬 이름 리스트
pokemon_names = [
    "이상해씨", "이상해풀", "이상해꽃", "파이리", "리자드", "리자몽", "꼬부기", "어니부기", "거북왕", "캐터피", 
    "단데기", "버터플", "뿔충이", "딱충이", "독침붕", "구구", "피죤", "피죤투", "꼬렛", "레트라",
    "깨비참", "깨비드릴조", "아보", "아보크", "피카츄", "라이츄", "모래두지", "고지", "니드런♀", "니드리나",
    "니드퀸", "니드런♂", "니드리노", "니드킹", "삐삐", "픽시", "식스테일", "나인테일", "푸린", "푸크린",
    "주뱃", "골뱃", "뚜벅초", "냄새꼬", "라플레시아", "파라스", "파라섹트", "콘팡", "도나리", "디그다", 
    "닥트리오", "나옹", "페르시온", "고라파덕", "골덕", "망키", "성원숭", "가디", "윈디", "발챙이", 
    "슈륙챙이", "강챙이", "캐이시", "윤겔라", "후딘", "알통몬", "근육몬", "괴력몬", "모다피", "우츠동", 
    "우츠보트", "왕눈해", "독파리", "꼬마돌", "데구리", "딱구리", "포니타", "날쌩마", "야돈", "야도란", 
    "코일", "레어코일", "파오리", "두두", "두트리오", "쥬쥬", "쥬레곤", "질퍽이", "질뻐기", "셀러", 
    "파르셀", "고오스", "고우스트", "팬텀", "롱스톤", "슬리프", "슬리퍼", "크랩", "킹크랩", "찌리리공", 
    "붐볼", "아라리", "나시", "탕구리", "텅구리", "시라소몬", "홍수몬", "내루미", "또가스", "또도가스", 
    "뿔카노", "코뿌리", "럭키", "덩쿠리", "캥카", "쏘드라", "시드라", "콘치", "왕콘치", "별가사리", 
    "아쿠스타", "마임맨", "스라크", "루주라", "에레브", "마그마", "쁘사이저", "켄타로스", "잉어킹", "갸라도스", 
    "라프라스", "메타몽", "이브이", "샤미드", "쥬피썬더", "부스터", "폴리곤", "암나이트", "암스타", "투구", 
    "투구푸스", "프테라", "잠만보", "프리져", "썬더", "파이어", "미뇽", "신뇽", "망나뇽", "뮤츠", "뮤"
]

# Fandom 포켓몬 URL을 생성
base_url = "https://pokemon.fandom.com/ko/wiki/"
pokemon_urls = [base_url + name for name in pokemon_names]

# 크롤링 함수
def get_pokemon_data(pokemon_url):
    response = requests.get(pokemon_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 포켓몬 이름 수집
    name = soup.find('h1', class_='page-header__title').text.strip()

    # 도감 설명 (여러 버전) 수집
    descriptions = soup.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color')
    red_desc = green_desc = blue_desc = yellow_desc = "N/A"

    for desc in descriptions:
        if "적" in desc.text:
            red_desc = desc.find('div', class_='pi-data-value pi-font').text.strip()
        elif "녹" in desc.text:
            green_desc = desc.find('div', class_='pi-data-value pi-font').text.strip()
        elif "청" in desc.text:
            blue_desc = desc.find('div', class_='pi-data-value pi-font').text.strip()
        elif "피카츄" in desc.text:
            yellow_desc = desc.find('div', class_='pi-data-value pi-font').text.strip()

    # 형식에 맞춘 데이터 반환
    return {
        'name': name,
        'red_desc': red_desc,
        'green_desc': green_desc,
        'blue_desc': blue_desc,
        'yellow_desc': yellow_desc,
    }

# CSV 파일 작성
with open('pokedex_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'red_desc', 'green_desc', 'blue_desc', 'yellow_desc'])

    # 각 포켓몬 URL에서 데이터를 수집하여 CSV 파일에 저장
    for url in pokemon_urls:
        try:
            pokemon_data = get_pokemon_data(url)
            writer.writerow([pokemon_data['name'], pokemon_data['red_desc'], pokemon_data['green_desc'], pokemon_data['blue_desc'], pokemon_data['yellow_desc']])
            print(f"{pokemon_data['name']} 정보 저장 완료")
            time.sleep(1)  # 사이트에 부담을 줄이기 위해 1초간 딜레이를 추가
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")
