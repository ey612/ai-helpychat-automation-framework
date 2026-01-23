
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class GnbComponent:
    """상단 네비게이션 바 컴포넌트"""
    
    locators = {
        "account_management": (By.XPATH, "//span[text()='계정 관리' or text()='Account Management']"),
        "person_icon": (By.CSS_SELECTOR, '[data-testid="PersonIcon"]'),
        "password_input": (By.CSS_SELECTOR, '[name="password"]'),
        "login_button": (By.XPATH, '//button[text()="Login"]'),
        "logout_button": (By.XPATH, '//p[text()="Logout" or text()="로그아웃"]'),
        "language_setting": (By.XPATH, "//span[text()='언어 설정' or text()='Language Settings']"),
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def logout(self):
        """로그아웃 시도"""
    
        # 1. 사용자 아이콘 클릭
        icon = self.wait.until(EC.element_to_be_clickable(self.locators["person_icon"]))
        icon.click()
        
        # 드롭다운이 보일 때까지 기다림
        self.wait.until(EC.visibility_of_element_located(self.locators["logout_button"]))
        
        try:
            self.wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "[data-elice-user-profile-content='true']")
            ))
        except:
            pass
        
        # 2. 로그아웃 버튼 클릭
        logout_btn = self.wait.until(EC.element_to_be_clickable(self.locators["logout_button"]))
        logout_btn.click()

        # 3. 로그아웃 후 Login 버튼 표시 확인
        login_btn = self.wait.until(
            EC.visibility_of_element_located(self.locators["login_button"])
        )
        return login_btn

    def click_person_icon(self):
        """사용자 아이콘 클릭해서 프로필 드롭다운 열기"""
        
        personl_icon = self.wait.until(
            EC.element_to_be_clickable(self.locators["person_icon"])
        )
        personl_icon.click()
        return personl_icon

    def click_language_setting(self):
        """프로필 드롭다운에서 언어 설정 메뉴를 클릭한다."""
        print("== 언어 설정 클릭 중 ==")
        self.wait.until(
        EC.invisibility_of_element_located(
        (By.CSS_SELECTOR, "span.MuiTypography-root.MuiTypography-body"))
        )
        language_setting = self.wait.until(
            EC.element_to_be_clickable(self.locators["language_setting"])
        )
        language_setting.click()
        print("✔️ 언어 설정 클릭 완료")       
        return language_setting
    
    def is_account_management_displayed(self):
        """Account Management 텍스트가 표시되는지 확인"""
        try:
            
            account_mgmt_element = self.wait.until(
                EC.visibility_of_element_located(self.locators["account_management"])
            )
            return account_mgmt_element.is_displayed()
        except TimeoutException:
            return False
        
        
class LanguageSetting:
    """언어 설정 드롭다운 메뉴 관련 기능"""
    
    #지원 언어 목록
    SUPPORTED_LANGUAGES = [
        "American English",
        "한국어(대한민국)",
        "ไทย (ไทย)",
        "日本語 (日本)",
    ]
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    
    def _get_language_locator(self, language_name):
        """특정 언어의 locator를 생성한다."""
        return (By.XPATH, f"//p[text()='{language_name}']")
    
    def verify_all_languages_displayed(self):
        """지원 언어가 드롭다운에 표시되는지 확인"""

        test_passed = True
        
        for language in self.SUPPORTED_LANGUAGES:
            current_locator = self._get_language_locator(language)

            try:
                self.wait.until(
                    EC.visibility_of_element_located(current_locator)
                )
                print(f" [성공] '{language}' 항목이 확인 되었습니다.")
            except TimeoutException:
                print(f" [실패] '{language}' 항목을 찾을 수 없습니다.")
                test_passed = False
                
        return test_passed
    
    def select_language(self, language_name):
        """언어 선택"""
        locator = self._get_language_locator(language_name)
        language_option = self.wait.until(EC.element_to_be_clickable(locator))
        language_option.click()
        print(f"'{language_name}' 선택 완료")
    
    def is_korean(self):
        """현재 언어가 한국어인지 확인"""
        korean_indicators = ["새 대화", "검색", "도구", "에이전트 탐색"]
        
        for text in korean_indicators:
            try:
                self.driver.find_element(By.XPATH, f"//*[text()='{text}']")
                return True
            except:
                continue
        
        return False
    
    def get_current_language(self):
        """사이드바 텍스트로 현재 언어 확인"""
    
        # 한국어 확인만 하면 됨!
        korean_indicators = ["새 대화", "검색", "도구", "에이전트 탐색"]
        
        for text in korean_indicators:
            try:
                self.driver.find_element(By.XPATH, f"//*[text()='{text}']")
            
                return "한국어(대한민국)"
            except:
                continue
        
        # 한국어가 아니면 "not korean"
        return "not korean"
