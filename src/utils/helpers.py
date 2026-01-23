import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# 브라우저 여는 함수

WAIT_TIMEOUT = 5
URL = "https://qaproject.elice.io/ai-helpy-chat"

def setup_driver(EMAIL, PW):
    '''브라우저를 열고 기본 설정을 한 뒤 로그인까지 완료하는 헬퍼 함수'''
    
    # 크롬 옵션 정의
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    
    # 드라이버 생성 및 설정 로직
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(WAIT_TIMEOUT)
    driver.get(URL)
    
    # 로그인 함수 호출
    login(driver, EMAIL, PW)
    
    return driver

# 파일 업로드 함수

def get_file_path(relative_path):
    
    
    # current_dir = 현재 위치
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 파일 경로 합치기
    combined_path = os.path.join(current_dir, relative_path)
    
    # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
    file_path = os.path.abspath(combined_path)
    print(f"계산된 파일 경로: {file_path}")
    
    file_name = os.path.basename(file_path)
    print(f"파일명: {file_name}")
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")
    
    return file_path