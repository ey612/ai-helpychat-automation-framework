from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ChatPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)
            
        self.locators = {
            TEXTAREA = (By.CSS_SELECTOR, "textarea"),
            SEND_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="보내기"]'),
            COPY_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="복사"]'),
            AI_COMPLETE = (By.CSS_SELECTOR, ".ai-response-complete"),
            }
    
    def _to_bmp_only(self, text: str) -> str:
        """
        비-BMP 문자(이모지 등) 제거
        
        개념:
        - 언더스코어(_)로 시작: '내부 전용' 메서드 (외부에서 직접 호출 X)
        - ord(c): 문자를 유니코드 번호로 변환
        - 리스트 컴프리헨션: [x for x in ... if 조건]
        
        예시: "안녕😊" → "안녕" (😊는 0xFFFF보다 큼)
        """
        return "".join(c for c in text if ord(c) <= 0xFFFF)
    
    def _wait_for_element(self, locator, condition="clickable"):
        """
        요소가 특정 상태가 될 때까지 대기
        
        개념:
        - expected_conditions (EC): 요소의 '예상 상태'를 확인
        - clickable: 클릭 가능 상태
        - presence: 페이지에 존재하는 상태
        
        매개변수:
        - locator: 요소 위치 정보 (By.CSS_SELECTOR, "...")
        - condition: 대기 조건 ("clickable" 또는 "presence")
        """
        if condition == "clickable":
            return self.wait.until(
                EC.element_to_be_clickable(locator)
            )
        elif condition == "presence":
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )
    
    # ============ 4. 공개 메서드 (Public Methods) ============
    
    def send_message(self, message: str):
        """
        채팅 메시지 전송
        
        동작 순서:
        1. 필요시 이모지 제거
        2. 입력창 찾아서 클릭
        3. 기존 텍스트 지우기
        4. 메시지 입력
        5. 보내기 버튼 클릭
        6. AI 응답 완료 대기
        
        매개변수:
        - message (str): 보낼 메시지 텍스트
        
        예외 처리:
        - TimeoutException: 요소를 찾지 못하거나 시간 초과
        """
        # 1. 이모지 제거 (필요시)
        safe_message = (
            self._to_bmp_only(message) 
            if self.CHROMEDRIVER_BMP_ONLY 
            else message
        )
        
        # 2. 입력창 찾기 및 클릭
        textarea = self._wait_for_element(self.TEXTAREA, "clickable")
        textarea.click()
        
        # 3. 기존 내용 지우고 새 메시지 입력
        textarea.clear()
        textarea.send_keys(safe_message)
        
        # 4. 보내기 버튼 클릭
        send_btn = self._wait_for_element(self.SEND_BUTTON, "clickable")
        send_btn.click()
        
        # 5. AI 응답 완료 대기
        try:
            self._wait_for_element(self.AI_COMPLETE, "presence")
            print(f"✅ 메시지 전송 완료: {message[:30]}...")
        except TimeoutException:
            print("⚠️ AI 응답 대기 시간 초과")
            raise
    
    
    def copy_last_message_and_resend(self):
        """
        마지막 메시지 복사 후 재전송
        
        동작 순서:
        1. 모든 복사 버튼 찾기
        2. 마지막 복사 버튼만 선택
        3. 클릭하여 클립보드에 복사
        4. 입력창에 붙여넣기 (Ctrl+V)
        5. 보내기 버튼 클릭
        6. AI 응답 대기
        
        개념:
        - presence_of_all_elements_located: 조건에 맞는 '모든' 요소 찾기
        - [-1]: 파이썬 리스트에서 마지막 요소 선택
        - Keys.CONTROL + "v": Ctrl+V 키보드 입력
        """
        # 1. 모든 복사 버튼 찾기
        copy_buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.COPY_BUTTON)
        )
        
        # 2. 마지막 버튼만 선택 및 클릭
        last_copy_btn = copy_buttons[-1]
        last_copy_btn.click()
        print("✅ 마지막 메시지 복사 완료")
        
        # 3. 입력창에 포커스
        textarea = self._wait_for_element(self.TEXTAREA, "clickable")
        textarea.click()
        
        # 4. Ctrl+V로 붙여넣기
        textarea.send_keys(Keys.CONTROL, "v")
        
        # 5. 보내기 버튼 클릭
        send_btn = self._wait_for_element(self.SEND_BUTTON, "clickable")
        send_btn.click()
        
        # 6. AI 응답 완료 대기
        try:
            self._wait_for_element(self.AI_COMPLETE, "presence")
            print("✅ 복사한 메시지 재전송 완료")
        except TimeoutException:
            print("⚠️ 재전송 후 AI 응답 대기 시간 초과")
            raise
    
    
    def get_all_messages(self):
        """
        화면의 모든 메시지 텍스트 가져오기
        
        개념:
        - find_elements: 여러 개의 요소를 리스트로 반환
        - .text: 요소의 텍스트 내용
        - 리스트 컴프리헨션: [x.text for x in list]
        
        반환값:
        - list: 모든 메시지 텍스트의 리스트
        
        사용 예:
        messages = chat_page.get_all_messages()
        print(messages[-1])  # 마지막 메시지 출력
        """
        # 실제 메시지 요소의 CSS 선택자는 확인 필요!
        message_elements = self.driver.find_elements(
            By.CSS_SELECTOR, 
            ".chat-message-text"  # 실제 선택자로 수정 필요
        )
        return [elem.text for elem in message_elements]
    
    
    def verify_last_two_messages_identical(self):
        """
        마지막 두 메시지가 동일한지 검증
        
        개념:
        - 테스트 검증용 메서드
        - assert: 조건이 False면 에러 발생
        
        반환값:
        - bool: 동일하면 True, 아니면 False
        """
        messages = self.get_all_messages()
        
        if len(messages) < 2:
            print("⚠️ 메시지가 2개 미만입니다")
            return False
        
        last_two = messages[-2:]
        is_identical = last_two[0] == last_two[1]
        
        if is_identical:
            print(f"✅ 마지막 두 메시지 동일: {last_two[0][:30]}...")
        else:
            print(f"❌ 마지막 두 메시지 불일치")
            print(f"   첫 번째: {last_two[0][:30]}...")
            print(f"   두 번째: {last_two[1][:30]}...")
        
        return is_identical