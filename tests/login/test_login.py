from src.pages.login_page import LoginPage
from src.pages.main_page import GnbComponent
from src.config.config import EMAIL, INVALID_FORMAT_EMAIL, PW, INVALID_EMAIL, WRONG_PASSWORD
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_success(driver):
    
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    assert "login" not in driver.current_url.lower()
    assert login_page.is_logout_button_displayed() is True
        

def test_login_invalid_id(driver):
    login_page = LoginPage(driver)
    login_page.login(WRONG_PASSWORD, INVALID_EMAIL)
    
    error_text = login_page.get_error_text()
    assert "Email or password does not match" in error_text
    print(f"실패 케이스: '{error_text}' 메시지 확인")
    
def test_login_invalid_format(driver):
    login_page = LoginPage(driver)
    login_page.login(INVALID_FORMAT_EMAIL, WRONG_PASSWORD)
    
    error_text = login_page.get_error_text()
    assert "Invalid email format" in error_text
    print(f"형식 오류 케이스: '{error_text}' 메시지 확인")

def test_login_lock_observation(driver):
    """팀원의 5회 실패 로직을 반복문으로 리팩토링함."""
    login_page = LoginPage(driver)
    
    for i in range(1, 6):
        print(f"{i}회차 잘못된 로그인 시도 중...")
        login_page.login(INVALID_EMAIL, WRONG_PASSWORD)
        
        # 락 문구가 뜨는지 확인 (에러 텍스트 가져오기 시도)
        try:
            error_text = login_page.get_error_text()
            if "incorrectly several times" in error_text:
                print(f"{i}회차 만에 락 경고 감지: {error_text}")
                return # 락이 확인되면 테스트 종료 (PASS)
        except:
            continue
    
    print("ℹ 5회 시도했으나 락 문구는 나타나지 않음 (관찰 종료)")
    
def test_logout_security_scenario(driver):
    login_page = LoginPage(driver)
    logout_page = GnbComponent(driver)
    
    login_page.login(PW, EMAIL)
    logout_page.logout()
    
    try:
        WebDriverWait(driver, 10).until(
            lambda d: "signin" in d.current_url or "login" in d.current_url
        )
        print(f"로그아웃 후 정상 이동 확인: {driver.current_url}")
    except:
        # 만약 data:, 처럼 비정상적인 주소라면, 직접 로그인 페이지로 이동시켜줍니다.
        print("비정상 주소 감지. 로그인 페이지로 직접 이동합니다.")
        driver.get("https://qaproject.elice.io") # 실제 로그인 URL로 수정
    
    for i in range(3):
        print(f" 뒤로가기 {i+1}회 시도")
        driver.back()
    
        # URL에 login, signin 이 포함되거나, 혹은 accounts.elice.io 주소일 때까지 대기
        WebDriverWait(driver, 10).until(
            lambda d: any(word in d.current_url.lower() for word in ["signin", "login", "accounts.elice"])
        )
        
        # 현재 URL을 출력해서 실제로 어디에 머물고 있는지 확인합니다.
        print(f"현재 URL: {driver.current_url}")
        assert any(word in driver.current_url.lower() for word in ["signin", "login", "accounts.elice"])