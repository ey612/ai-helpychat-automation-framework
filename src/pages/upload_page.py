from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class UploadPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open_file_upload_dialog(self):
        """"[+] 버튼 클릭 -> [파일 업로드] 버튼 클릭 ( 파일 선택 UI 나오게 하는 것 )"""
        plus_icon = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="plusIcon"]'))
        )
        plus_icon.click()
        
        upload_file_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='파일 업로드']"))
        )
        upload_file_btn.click()

    def upload_file(self, file_path):
        """"파일 선택 + [열기] 버튼 클릭"""
        file_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(file_path)   
    
    def upload_multiple_files(self, file_paths: list[str]):
        """
        여러 파일을 동시에 업로드
        Selenium 규칙상 '\\n'으로 경로를 이어서 전달
        """
        files_to_send = '\n'.join(file_paths)

        file_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(files_to_send)
        
    def is_file_uploaded(self, file_name):
        """문서 파일이 업로드되었는지 확인"""
        try:
            file_card = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
             )
            print("파일 카드가 나타남")
            return file_card.is_displayed()
        except TimeoutException:
            print(f"'{file_name}' 파일 카드를 찾을 수 없음")
            return False        
        
    def is_image_uploaded(self, file_name):
        """이미지 파일이 업로드되었는지 확인"""
        try :
            image_card = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
            print("파일 카드가 나타남")
            return image_card.is_displayed()
        except TimeoutException:
            print(f"'{file_name}' 이미지 파일 카드를 찾을 수 없음")
            return False
                   
    def verify_alert_contains(self, *expected_texts):
        """Alert 메시지에 특정 텍스트들중 하나라도 포함되어 있는지 확인"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Alert 메시지: {alert_text}")
            
            found_texts = []
            
            for text in expected_texts:
                if text in alert_text:
                    found_texts.append(text)
                    
            if found_texts:
                print(f"Alert에 '{expected_texts}' 포함됨")
                alert.acccept()
                return True
            else :
                print(f"Alert에 '{expected_texts}' 없음")
                alert.accept()
                return False
        
        except TimeoutException:
            print("Alert이 나타나지 않음")
            return False