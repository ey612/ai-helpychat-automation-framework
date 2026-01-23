import os
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from src.pages.upload_page import UploadPage
from src.pages.login_page import LoginPage
from src.config.config import EMAIL, PW
from src.utils.helpers import get_file_path
from src.utils.screenshot import save_screenshot

# [IMG_MDL_TC_001] 지원 확장자 이미지가 정상 업로드되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_normal.jpg",
        "test_normal.png",
    ]
)
def test_001_image_upload_valid_extension(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 설정
    print(f"업로드 할 이미지 파일 경로{file_name}")
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 이미지 파일 업로드 확인
    is_uploaded = upload_page.is_image_uploaded(file_name)
    assert is_uploaded, f"'{file_name}'파일이 업로드되지 않았습니다."
    print(f"'{file_name}' 파일 업로드 완료")

# [IMG_MDL_TC_002] 미지원 확장자 이미지 업로드 시 에러 메시지가 표시되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_fail.svg",
        "test_fail.ico",
        
    ]
)
def test_002_image_invalid_extensions_shows_error(driver, file_name):
    
     # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    print(f"업로드 할 이미지 파일 경로{file_name}")
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_image_uploaded(file_name)
    assert not is_uploaded, \
        f"미지원 확장자 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("지원","확장자")
    assert has_error_message, f"'{file_name}' 확장자 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")

# [IMG_MDL_TC_003] 허용 용량 초과 이미지 업로드 시 에러 메시지가 표시되는지 확인    
@pytest.mark.parametrize(
    "file_name",
    [
        "test_50.1mb.jpg",
        "test_51mb.jpg",
        "test_60mb.jpg",
    ]
)
def test_003_image_upload_exceeds_max_size_shows_error(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    print(f"업로드 할 {file_name} 이미지 파일 경로")
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
     # 3. 이미지 파일 업로드
    print(f"{file_name} 이미지 파일 업로드 중")
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_image_uploaded(file_name)
    assert not is_uploaded, \
        f"허용 용량 초과 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("크기", "용량")
    assert has_error_message, f"'{file_name}' 용량 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")

# [IMG_MDL_TC_004] 경계값 용량 이미지 업로드 시 정상 업로드되는지 확인 (49MB) / (49.9MB)
@pytest.mark.parametrize(
    "file_name",
    [
        "test_49mb.jpg",
        "test_49.9mb.jpg",
    ]
)
def test_004_image_upload_boundary_size_succeeds(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 이미지 파일 업로드 확인
    is_uploaded = upload_page.is_image_uploaded(file_name)
    assert is_uploaded, f"'{file_name}' 파일이 업로드되지 않았습니다."
    print(f"'{file_name}' 파일 업로드 완료")
    
# [IMG_MDL_TC_005] 여러 이미지 동시 업로드 시 정상 업로드되는지 확인
MULTI_IMAGE_FILES = [
    
    'test_multi_1.jpg',
    'test_multi_2.png'
]
def test_005_image_upload_multiple_files(driver) :
    
     # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 파일 경로 준비
    file_paths_list = []
    
    for file_name in MULTI_IMAGE_FILES:
        relative_path = f'../../src/resources/asserts/images/{file_name}'
        file_path = get_file_path(relative_path)
        file_paths_list.append(file_path)
        print(f"  - {file_name}: 경로 확인 완료")
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_multiple_files(file_paths_list)
    print(f"{len(MULTI_IMAGE_FILES)}개 파일 업로드 요청 완료")
    
    # 4. 이미지 파일 업로드 확인
    for file_name in MULTI_IMAGE_FILES:
        is_uploaded = upload_page.is_image_uploaded(file_name)
        assert is_uploaded, f"'{file_name}' 파일이 업로드되지 않았습니다."
        print(f"'{file_name}' 파일 카드 확인 완료")
    print(f"{len(MULTI_IMAGE_FILES)}개 파일 업로드 완료")

# [IMG_MDL_TC_006] 특수문자가 포함된 이미지 파일명 업로드 시 정상 업로드 확인
def test_006_image_upload_filename_with_special_characters_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 특수문자 포함된 파일명 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_한글@#$.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    # 4. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 이미지 파일 업로드 확인
    is_uploaded = upload_page.is_image_uploaded(file_name)
    assert is_uploaded, f"'{file_name}'파일이 업로드되지 않았습니다."
    print(f"'{file_name}' 파일 업로드 완료")

# [IMG_MDL_TC_007] 헤더가 손상된 이미지 업로드 시 에러 메시지가 표시되는지 확인
def test_007_image_upload_corrupted_header_shows_error(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    print("업로드 할 손상된 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_corrupted_invalid_header.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_image_uploaded(file_name)
    assert not is_uploaded, \
        f"손상된 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("손상","잘못된 형식")
    assert has_error_message, f"'{file_name}' 손상 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")
    
    
    