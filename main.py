import csv

# 타입 번호와 이름 매핑 (페어리 타입 삭제)
TYPE_MAP = {
    1: "불꽃",
    2: "물",
    3: "풀",
    4: "전기",
    5: "독",
    6: "에스퍼",
    7: "비행",
    8: "땅",
    9: "노말",
    10: "격투",
    11: "벌레",
    12: "바위",
    13: "고스트",
    14: "얼음",
    15: "드래곤",
}

# 포켓몬 형태 매핑
FORM_MAP = {
    1: "머리만 있는 포켓몬",
    2: "몸이 길쭉한 포켓몬",
    3: "지느러미가 있는 포켓몬",
    4: "머리와 팔만 있는 포켓몬",
    5: "머리와 바닥이 있는 포켓몬",
    6: "두 다리와 꼬리가 있는 포켓몬",
    7: "머리와 다리만 있는 포켓몬",
    8: "다리가 넷인 포켓몬",
    9: "날개가 둘인 포켓몬",
    10: "몸이 여러갈래인 포켓몬",
    11: "여러 몸이 합쳐진 포켓몬",
    12: "두 다리에 꼬리가 없는 포켓몬",
    13: "날개가 여러쌍인 포켓몬",
    14: "곤충형 포켓몬",
}

class Pokemon:
    def __init__(self, number, name, type1, type2, form, category, red_green_desc, blue_desc, yellow_desc):
        self.number = number
        self.name = name
        self.p_type = [TYPE_MAP[type1]]  # 타입1 변환
        if type2:
            self.p_type.append(TYPE_MAP[type2])  # 타입2 변환
        self.form = FORM_MAP[form]  # 형태 정보 (번호로 저장, 문자로 변환)
        self.category = category  # 분류 정보
        self.red_green_desc = red_green_desc  # 적/녹 버전 도감 설명
        self.blue_desc = blue_desc
        self.yellow_desc = yellow_desc

    def __str__(self):
        return (f"#{self.number} {self.name}\n"
                f"타입: {', '.join(self.p_type)}\n"
                f"형태: {self.form}\n"
                f"분류: {self.category}\n"
                f"적/녹 버전: {self.red_green_desc}\n"
                f"청 버전: {self.blue_desc}\n"
                f"피카츄 버전: {self.yellow_desc}")

# CSV 파일로부터 포켓몬 데이터 로드
def load_pokedex_from_csv(file_path):
    pokedex = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            number = int(row["number"])
            name = row["name"]
            type1 = int(row["type1"])
            type2 = int(row["type2"]) if row["type2"] else None
            form = int(row["form"])
            category = row["category"]
            red_green_desc = row["red_green_desc"]
            blue_desc = row["blue_desc"]
            yellow_desc = row["yellow_desc"]
            pokedex.append(Pokemon(number, name, type1, type2, form, category, red_green_desc, blue_desc, yellow_desc))
    return pokedex

# 포켓몬의 번호로 모든 정보를 출력하는 기능 추가
def show_pokemon_details(pokedex, number):
    for pokemon in pokedex:
        if pokemon.number == number:
            print(pokemon)
            return
    print("해당 번호의 포켓몬을 찾을 수 없습니다.")

# 포켓몬 번호와 이름만 출력하는 함수
def search_by_number(pokedex, number):
    for pokemon in pokedex:
        if pokemon.number == number:
            return f"#{pokemon.number} {pokemon.name}"
    return "해당 번호의 포켓몬을 찾을 수 없습니다."

# 14가지 형태 출력 및 검색
def print_form_options():
    print("\n포켓몬 형태:")
    for key, value in FORM_MAP.items():
        print(f"{key}. {value}")

# 검색 기능: 형태로 포켓몬 검색
def search_by_form(pokedex, form_input):
    results = []
    for pokemon in pokedex:
        if pokemon.form == FORM_MAP[form_input]:
            results.append(f"#{pokemon.number} {pokemon.name}")
    return results if results else "해당 형태에 맞는 포켓몬을 찾을 수 없습니다."

# 포켓몬 도감 메뉴
def menu():
    pokedex = load_pokedex_from_csv("pokedex_data.csv")

    while True:
        print("\n포켓몬 도감")
        print("1. 번호로 검색")
        print("2. 형태로 검색")
        print("3. 종료")
        
        choice = input("선택: ")
        
        if choice == '1':
            try:
                number = int(input("포켓몬 번호 입력: "))
                result = search_by_number(pokedex, number)
                print(result)

                # 추가 기능: 포켓몬의 번호로 모든 정보 출력
                show_number = input("해당 포켓몬의 번호를 입력하면 모든 정보를 출력합니다 (0을 입력하면 메뉴로 돌아갑니다): ")
                if show_number == '0':
                    print("메뉴로 돌아갑니다.")
                    continue
                elif show_number.isdigit():
                    show_pokemon_details(pokedex, int(show_number))
            except ValueError:
                print("잘못된 번호입니다.")
        
        elif choice == '2':
            print_form_options()
            try:
                form_input = int(input("검색할 형태 번호를 입력하세요: "))
                results = search_by_form(pokedex, form_input)
                if isinstance(results, list):
                    for pokemon in results:
                        print(pokemon)
                else:
                    print(results)

                # 추가 기능: 포켓몬의 번호로 모든 정보 출력
                show_number = input("해당 포켓몬의 번호를 입력하면 모든 정보를 출력합니다 (0을 입력하면 메뉴로 돌아갑니다): ")
                if show_number == '0':
                    print("메뉴로 돌아갑니다.")
                    continue
                elif show_number.isdigit():
                    show_pokemon_details(pokedex, int(show_number))
            except ValueError:
                print("잘못된 입력입니다.")
        
        elif choice == '3':
            break
        
        else:
            print("잘못된 입력입니다.")

# 프로그램 실행
menu()
