import os
import pytest

from selenium.webdriver.support import expected_conditions as EC

from src.config.config import EMAIL, PW
from src.utils.helpers import get_file_path
from src.pages.upload_page import UploadPage
from src.pages.login_page import LoginPage

# [DOC_MDL_TC_001] 빈 문서가 정상 업로드되는지 확인
def test_001_document_upload_empty_file_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 빈 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_empty.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 문서 파일 업로드 확인
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert is_uploaded, f"'{file_name}'파일이 업로드되지 않았습니다."
    print(f"'{file_name}' 파일 업로드 완료")
    
# [DOC_MDL_TC_002] 암호화 문서 업로드 시 에러 메시지가 표시되는지 확인 
def test_002_document_upload_encrypted_file_shows_error(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver) 
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 암호화 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_encrypted.docx'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert not is_uploaded, \
        f"암호화된 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 5. 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("암호화")
    assert has_error_message, f"'{file_name}' 암호화 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")

#[DOC_MDL_TC_003] 지원 확장자 문서가 정상 업로드되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_normal.pdf",
        "test_normal.docx",
    ]
)
def test_003_document_upload_valid_extension_pdf(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 파일 경로: {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)

    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 문서 파일 업로드 확인
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert is_uploaded, f"'{file_name}'파일이 업로드되지 않았습니다."
    print(f"{file_name} 파일 업로드 완료")

# [DOC_MDL_TC_004] 미지원 확장자 문서 업로드 시 에러 메시지가 표시되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_fail.zip",
        "test_fail.exe",
        "test_fail.mp4",
    ]
)
def test_004_document_invalid_extensions_shows_error(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 문서 파일 경로 {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert not is_uploaded, \
        f"미지원 확장자 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("지원","확장자")
    assert has_error_message, f"'{file_name}' 확장자 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")
   
# [DOC_MDL_TC_005] 허용 용량 초과 문서 업로드 시 에러 메시지가 표시되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_50.1mb.pdf",
        "test_51mb.pdf",
        "test_60mb.pdf",
    ]
)
def test_005_document_upload_exceeds_max_size_shows_error(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 문서 파일 경로: {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert not is_uploaded, \
        f"허용 용량 초과 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("크기", "용량")
    assert has_error_message, f"'{file_name}' 용량 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")
   
# [DOC_MDL_TC_006] 경계값 용량 문서 업로드 시 정상 업로드되는지 확인 (49MB) / (49.9MB)
@pytest.mark.parametrize(
    "file_name",
    [
        "test_49mb.pdf",
        "test_49.9mb.docx",
    ]
)
def test_006_document_upload_boundary_size_succeeds(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 문서 파일 경로: {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 문서 파일 업로드 확인
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert is_uploaded, f"'{file_name}' 파일이 업로드되지 않았습니다."
    print(f"'{file_name}' 파일 업로드 완료")

# [DOC_MDL_TC_007] 여러 문서 동시 업로드 시 정상 업로드되는지 확인
MULTI_DOC_FILES = [
        'test_multi_1.pdf',
        'test_multi_2.docx'
    ]
def test_007_document_upload_multiple_files_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 파일 경로 준비
    file_paths_list = []
    
    for file_name in MULTI_DOC_FILES:
        relative_path = f'../../src/resources/asserts/files/{file_name}'
        file_path = get_file_path(relative_path)
        file_paths_list.append(file_path)
        print(f"  - {file_name}: 경로 확인 완료")

    # 3. 다중 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_multiple_files(file_paths_list)
    print(f"{len(MULTI_DOC_FILES)}개 파일 업로드 요청 완료")
    
    # 4. 다중 파일 업로드 확인
    for file_name in MULTI_DOC_FILES:
        is_uploaded = upload_page.is_file_uploaded(file_name)
        assert is_uploaded, f"'{file_name}' 파일이 업로드되지 않았습니다."
        print(f"'{file_name}' 파일 카드 확인 완료")
    print(f"{len(MULTI_DOC_FILES)}개 파일 업로드 완료")

# [DOC_MDL_TC_008] 특수문자가 포함된 문서 파일명 업로드 시 정상 업로드 확인
def test_008_document_upload_filename_with_special_characters_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 특수문자 포함된 파일명 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_한글@#$.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)

    # 4. 문서 파일 업로드 확인
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert is_uploaded, f"'{file_name}'파일이 업로드되지 않았습니다."
    print(f"{file_name} 파일 업로드 완료")

# [DOC_MDL_TC_009] 헤더가 손상된 문서 업로드 시 에러 메시지가 표시되는지 확인 
def test_009_document_upload_corrupted_header_shows_error(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 손상된 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_corrupted_invalid_header.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 파일 카드가 나타나지 않아야 함
    is_uploaded = upload_page.is_file_uploaded(file_name)
    assert not is_uploaded, \
        f"손상된 파일 '{file_name}'의 파일 카드가 표시되면 안 됩니다."
    print("파일 카드가 나타나지 않음 (정상)")
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    has_error_message = upload_page.verify_alert_contains("손상","잘못된 형식")
    assert has_error_message, f"'{file_name}' 손상 관련 오류 메시지가 표시되지 않음"
    print(f"'{file_name}' 파일 업로드 오류 메시지 확인 완료")










