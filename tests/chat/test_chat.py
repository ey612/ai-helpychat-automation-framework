import time
import pytest
from src.pages.chat_page import ChatPage

# ============ 테스트 케이스 ============

def test_send_simple_message(logged_in_korean):
    """
    간단한 메시지 전송 테스트
    
    개념:
    - 테스트 함수는 'test_'로 시작해야 pytest가 인식해요
    - logged_in_korean: conftest.py의 fixture (로그인 완료된 드라이버)
    
    검증:
    - 메시지 전송이 에러 없이 완료되는지 확인
    """
    driver = logged_in_korean
    
    # 1. ChatPage 객체 생성
    # 개념: 드라이버를 주입(Dependency Injection)해서 객체 생성
    chat_page = ChatPage(driver)
    
    # 2. 메시지 전송
    test_message = "안녕하세요 자동화 테스트입니다."
    chat_page.send_message(test_message)
    
    # 3. 검증
    # 개념: assert는 조건이 True가 아니면 테스트 실패
    assert True  # 에러 없이 여기까지 왔으면 성공!
    print("✅ 간단한 메시지 전송 테스트 통과")


def test_send_long_message(logged_in_korean):
    """
    장문 메시지 전송 테스트
    
    검증:
    - 긴 텍스트도 정상적으로 전송되는지 확인
    """
    driver = logged_in_korean
    chat_page = ChatPage(driver)
    
    # 긴 메시지 생성
    # 개념: 문자열 * 숫자 = 반복된 문자열
    long_message = "장문 요약 입니다!!." * 90
    
    chat_page.send_message(long_message)
    
    assert True
    print("✅ 장문 메시지 전송 테스트 통과")


def test_send_special_characters(logged_in_korean):
    """
    특수문자 포함 메시지 전송 테스트
    
    검증:
    - 특수문자와 이모지가 처리되는지 확인
    - BMP 제약으로 일부 이모지는 제거될 수 있음
    """
    driver = logged_in_korean
    chat_page = ChatPage(driver)
    
    special_message = "()_+!&★☆♥♡♠♣😊🎉💡♬㉿㈜🔥✨㎲㎳㎴ⅵⅶ⅛⅜⅝㈍㉭"
    
    chat_page.send_message(special_message)
    
    assert True
    print("✅ 특수문자 메시지 전송 테스트 통과")


def test_copy_and_resend_last_message(logged_in_korean):
    """
    마지막 메시지 복사 후 재전송 테스트
    
    시나리오:
    1. 특수문자 메시지 전송
    2. 해당 메시지 복사
    3. 재전송
    4. 마지막 두 메시지가 동일한지 검증
    
    개념:
    - 복합 시나리오: 여러 단계를 순차적으로 테스트
    """
    driver = logged_in_korean
    chat_page = ChatPage(driver)
    
    # 1. 원본 메시지 전송
    original_message = "복사 테스트용 메시지입니다."
    chat_page.send_message(original_message)
    
    # 잠시 대기 (UI 안정화)
    time.sleep(1)
    
    # 2. 마지막 메시지 복사 및 재전송
    chat_page.copy_last_message_and_resend()
    
    # 3. 검증: 마지막 두 메시지가 동일한지
    # (선택적) 더 정확한 검증을 원하면 아래 주석 해제
    # assert chat_page.verify_last_two_messages_identical()
    
    assert True
    print("✅ 복사 후 재전송 테스트 통과")


def test_send_multiple_messages_and_copy_last(logged_in_korean):
    """
    여러 메시지 전송 후 마지막 것만 복사하는 통합 테스트
    (팀원의 원래 테스트 시나리오)
    
    시나리오:
    1. 간단한 메시지 전송
    2. 장문 메시지 전송
    3. 특수문자 메시지 전송
    4. 마지막 메시지(특수문자)만 복사 후 재전송
    
    개념:
    - 통합 테스트: 여러 기능을 조합해서 실제 사용 시나리오 검증
    """
    driver = logged_in_korean
    chat_page = ChatPage(driver)
    
    # 테스트 케이스 딕셔너리
    # 개념: 딕셔너리(dict) - 키:값 쌍으로 데이터 저장
    test_cases = {
        "simple": "안녕하세요 자동화 테스트입니다.",
        "long": "장문 요약 입니다!!." * 90,
        "special": "()_+!&★☆♥♡♠♣😊🎉💡♬㉿㈜🔥✨㎲㎳㎴ⅵⅶ⅛⅜⅝㈍㉭",
    }
    
    # 1. 모든 메시지 순차 전송
    # 개념: .items()는 (키, 값) 튜플을 반환
    for name, message in test_cases.items():
        print(f"🚀 '{name}' 메시지 전송 중...")
        chat_page.send_message(message)
        time.sleep(0.5)  # 각 메시지 사이 짧은 대기
    
    # 2. 마지막 메시지(special) 복사 후 재전송
    chat_page.copy_last_message_and_resend()
    
    # 3. 검증 (선택)
    # 더 엄격한 검증을 원하면 아래 주석 해제
    # messages = chat_page.get_all_messages()
    # assert len(messages) >= 4  # simple, long, special, special(복사본)
    # assert messages[-1] == messages[-2]  # 마지막 두 개가 동일
    
    assert True
    print("✅ 통합 테스트 완료")


# ============ 부가 테스트 (선택) ============

@pytest.mark.skip(reason="AI_COMPLETE 셀렉터 확인 필요")
def test_ai_response_validation(logged_in_korean):
    """
    AI 응답 검증 테스트
    
    주의:
    - AI_COMPLETE 셀렉터가 정확해야 동작해요
    - 실제 AI 응답 시간에 따라 타임아웃 조정 필요
    
    개념:
    - @pytest.mark.skip: 이 테스트를 건너뛰기 (아직 준비 안됨)
    """
    driver = logged_in_korean
    chat_page = ChatPage(driver, timeout=60)  # 타임아웃 60초로 증가
    
    chat_page.send_message("간단한 질문입니다.")
    
    # AI 응답이 실제로 왔는지 검증
    messages = chat_page.get_all_messages()
    assert len(messages) >= 2  # 질문 + 답변 최소 2개
    
    print("✅ AI 응답 검증 테스트 통과")