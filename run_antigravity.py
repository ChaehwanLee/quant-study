### [수정된 전체 코드]

import os
import sys
import google.generativeai as genai
from google.generativeai import types # `types` 모듈의 명확한 임포트 경로로 수정

def main():
    # 1. API 키 확인 (파일 내부에 직접 주입하셨다면 아래 주석을 풀고 키를 넣으세요)
    # api_key = "내_실제_API_키"
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 에러: API 키가 없습니다. 'GEMINI_API_KEY' 환경 변수를 설정해주세요.")
        sys.exit(1)

    # ❗ 수정된 부분: Gemini API 클라이언트 초기화 방식 변경
    # `genai.Client` 대신 `genai.configure`를 사용하여 API 키를 설정하고,
    # 이후 `genai.GenerativeModel`을 통해 모델 인스턴스를 생성합니다.
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"❌ Gemini API 키 설정 중 에러가 발생했습니다: {e}")
        sys.exit(1)

    # 2. 분석할 파일 지정
    TARGET_FILE = "backtest_strategy.py"
    if not os.path.exists(TARGET_FILE):
        print(f"❌ 에러: [{TARGET_FILE}] 파일이 없습니다. 백테스팅 전략 파일을 확인해주세요.")
        sys.exit(1)

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        source_code = f.read()

    print(f"🔒 [보안 통제] 오직 [{TARGET_FILE}]의 텍스트 내용만 구글 서버로瞬신합니다.")
    print("🚀 전체 코드 강제 출력 모드로 분석 중... (내 맥북 RAM 사용량 0%)\n")

    # ❗ 수정된 부분: 모델 인스턴스 생성
    # `client.models.generate_content` 대신 `GenerativeModel` 인스턴스를 통해 호출합니다.
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 3. AI가 중간에 코드를 잘라먹지 못하도록 제약 조건 강화
    try:
        response = model.generate_content( # `model` 인스턴스를 사용하여 `generate_content` 호출
            contents=f"""
            너는 파이썬 퀀트 코드를 검증하는 자율 에이전트야.
            아래 제공된 내 백테스팅 소스 코드를 면밀히 분석하고 디버깅해줘.
            
            ⚠️ [극도로 중요한 지시사항 - 절대 생략 금지]
            1. 수정된 코드를 출력할 때는 반드시 생략(예: # ... 기존 코드 동일)을 절대로 하지 마.
            2. 처음 `import`문부터 맨 마지막 `print`문까지 수정한 내용이 반영된 [완성된 전체 소스 코드]를 단 한 줄도 빠짐없이 통째로 출력해줘. 그대로 복사 붙여넣기 해서 쓸 수 있어야 해.
            3. 코드 출력이 끝난 후에 [어떤 버그를 왜 고쳤는지 설명 리포트]를 요약해줘.
            
            [소스 코드]
            {source_code}
            """,
            # ⚡ [핵심 설정] AI가 중간에 말을 끊지 못하도록 최대 출력 글자 수(Max Output Tokens)를 한계치까지 확장
            config=types.GenerateContentConfig(
                max_output_tokens=8192,  # 대량의 코드도 잘리지 않게 방어벽 구축
                temperature=0.2          # 코드가 헛소리하지 않고 정확하게 출력되도록 창의성 낮춤
            )
        )

        print("=== ✨ 구글 에이전트 분석 결과 ===")
        print(response.text)

    except Exception as e:
        print(f"❌ 구글 API 호출 중 에러가 발생했습니다:\n{e}")

if __name__ == "__main__":
    main()


---

### [어떤 버그를 왜 고쳤는지 설명 리포트]

제공된 소스 코드는 Google Gemini API를 사용하여 다른 파이썬 코드 파일을 분석하려는 목적으로 작성되었습니다. 분석 결과, 주로 `google-generativeai` 라이브러리의 사용법과 관련된 몇 가지 런타임 에러를 유발할 수 있는 버그가 발견되어 다음과 같이 수정했습니다.

1. **`google.genai.types` 임포트 경로 수정:**
    * **버그 내용:** 기존 코드는 `from google import genai` 이후 `from google.genai import types`를 사용했습니다. `types` 모듈은 일반적으로 `google.generativeai` 패키지 내부에 직접 위치하므로, 이 방식은 런타임 시 `AttributeError`나 `ImportError`를 발생시킬 수 있습니다.
    * **수정 이유:** `google-generativeai` 라이브러리의 표준 사용법에 따라 `from google.generativeai import types`로 변경하여 `GenerateContentConfig`와 같은 타입 객체를 올바르게 참조할 수 있도록 했습니다.

2. **Gemini API 클라이언트 초기화 및 모델 호출 방식 오류:**
    * **버그 내용:**
        * `client = genai.Client(api_key=api_key)`: `google.generativeai` 라이브러리에는 `Client`라는 직접적인 클래스가 존재하지 않습니다. 이로 인해 `AttributeError`가 발생합니다.
        * `response = client.models.generate_content(...)`: `client` 객체가 올바르게 초기화되지 않았고, `models`라는 속성도 존재하지 않아 `AttributeError`를 유발합니다. 또한 `generate_content` 메서드 내부에 `model="gemini-2.5-flash"` 인자를 중복해서 전달하고 있었습니다.
    * **수정 이유:**
        * `google-generativeai` 라이브러리의 올바른 사용법은 먼저 `genai.configure(api_key=api_key)`를 호출하여 전역적으로 API 키를 설정하는 것입니다.
        * 그 후, 특정 모델(`gemini-2.5-flash`)을 사용하기 위해 `model = genai.GenerativeModel("gemini-2.5-flash")`와 같이 `GenerativeModel` 클래스의 인스턴스를 생성해야 합니다.