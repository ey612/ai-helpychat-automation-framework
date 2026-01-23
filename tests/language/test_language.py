
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.login_page import LoginPage
from src.pages.main_page import GnbComponent, LanguageSetting
from src.config.config import PW


# [LANG_TC_001] 프로필 메뉴에서 언어 설정 클릭 시 지원 언어 목록이 표시되는지 확인
def test_001_language_menu_shows_supported_languages(logged_in_korean):

    driver = logged_in_korean

    # 1. 언어 설정 메뉴 열기
    gnb = GnbComponent(driver)
    gnb.click_person_icon()
    gnb.click_language_setting()

    # 2. 지원 언어 표시 되는지 확인
    language_setting = LanguageSetting(driver)
    test_passed = language_setting.verify_all_languages_displayed()
    
    # 3. 검증
    assert test_passed, "모든 언어 항목이 드롭다운에 표시되지 않았습니다."

# [LANG_TC_002] 언어 변경 후 재로그인 시 선택한 언어 설정이 유지되는지 확인
def test_002_language_setting_persists_after_relogin(logged_in_korean):
    
    driver = logged_in_korean
    wait = WebDriverWait(driver, 10)

    # 1. 사용자 아이콘 -> 언어 설정 클릭
    gnd_component = GnbComponent(driver)

    try:
        
        gnd_component.click_person_icon()
        gnd_component.click_language_setting()
        
        # 2. 언어 설정 변경 ( 한국어 -> 영어 )
        language_setting = LanguageSetting(driver)
        language_setting.select_language("American English")

        # 3. 언어 변경 확인 (검증)
        is_displayed = gnd_component.is_account_management_displayed()
        assert is_displayed, "언어 변경 확인 실패: Account Management가 표시되지 않았습니다."
        print("언어 변경 확인 성공!")

        # 4. 새로 고침
        driver.refresh()
        print("페이지를 새로고침했습니다.")

        
        # 드롭다운이 보이지 않을 때까지 대기
        wait.until(
            EC.invisibility_of_element_located(gnd_component.locators["account_management"])
        )
        
        # 5.로그아웃
        login_btn = gnd_component.logout()
        assert login_btn.is_displayed(), "로그아웃 실패: 로그인 버튼이 표시되지 않았습니다"
        
        # 6. 재로그인
        login_page = LoginPage(driver)
        login_page.login(PW)
        
        # 로그인 완료 대기
        wait.until(
            EC.invisibility_of_element_located(login_page.locators["login_button"])
        )
        print("재로그인 완료")

        # 메인 페이지 로드 대기
        wait.until(
        EC.element_to_be_clickable(gnd_component.locators["person_icon"])
        ) 
        
        # 7. 언어 유지 확인
        gnd_component.click_person_icon()
        is_displayed_second = gnd_component.is_account_management_displayed()
        assert is_displayed_second, "재로그인 후 언어 설정이 유지되지 않았습니다."
        print("재로그인 후 언어 유지 확인 성공!")
        
        driver.refresh()
        print("페이지를 새로고침했습니다.")
        
    except Exception as e:
        assert False, f"사용자 아이콘 클릭 실패: {e}"