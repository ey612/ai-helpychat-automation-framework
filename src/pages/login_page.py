from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    
    locators = {
        "email_input": (By.CSS_SELECTOR, '[name="loginId"]'),
        "password_input": (By.CSS_SELECTOR, '[name="password"]'),
        "login_button": (By.XPATH, '//button[text()="Login"]'),
        "logout_button": (By.CSS_SELECTOR, 'button[type="button"]'),
        "error_message": (By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'message')]")
    }
    
    
    def __init__(self,driver):
        
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login (self, PW, user_id=None):
        """"
        - user_id가 있으면 이메일 + 비밀번호 입력
        - user_id가 없으면 비밀번호만 입력
        """
        print("로그인 시도")

        if user_id:
            print(f"이메일 입력: {user_id}")
            email_el = self.wait.until(EC.presence_of_element_located(self.locators["email_input"]))
            email_el.clear()
            email_el.send_keys(user_id)
        
        print("비밀번호 입력")
        pw_el = self.wait.until(EC.presence_of_element_located(self.locators["password_input"]))
        pw_el.clear()
        pw_el.send_keys(PW)

        print("로그인 버튼 클릭")
        self.wait.until(EC.element_to_be_clickable(self.locators["login_button"])).click()
        print('로그인 버튼 클릭 완료')
        
    def is_logout_button_displayed(self):
        """로그인 성공 여부를 확인하기 위한 메서드"""
        try:
            return self.wait.until(
                EC.presence_of_element_located(self.locators["logout_button"])
            ).is_displayed()
        except:
            return False
        
    def get_error_text(self):
            """에러 메시지 텍스트가 화면에 나타날 때까지 기다린 후 반환합니다."""
            # 특정 에러 메시지가 포함된 요소를 텍스트 기반으로 찾음
            element = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'match') or contains(text(), 'format') or contains(text(), 'incorrectly')]"))
            )
            return element.text