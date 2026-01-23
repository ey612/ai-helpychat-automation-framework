import os
from datetime import datetime

def save_screenshot(driver, folder_name, file_name):
    """
    Selenium 스크린샷 저장 유틸
    """

    # 프로젝트 루트 기준 screenshots 폴더
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "screenshots")
    )

    target_dir = os.path.join(base_dir, folder_name)
    os.makedirs(target_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(
        target_dir, f"{timestamp}_{file_name}.png"
    )

    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

    return screenshot_path