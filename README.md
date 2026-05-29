# 그랜드 마케팅 시안 제작 프롬프트 생성기

API Key 없이 사용하는 Streamlit 기반 이미지 생성 프롬프트 생성기입니다.
선택형 항목과 수기 입력을 바탕으로 ChatGPT에 붙여넣을 이미지 제작 프롬프트를 생성합니다.

## 배포 방법

1. GitHub 레포지토리 `peppermint1231/grand-marketing-prompt-maker`에 아래 파일을 업로드합니다.
   - app.py
   - requirements.txt
   - .streamlit/config.toml
   - README.md
2. Streamlit Community Cloud에서 앱을 배포합니다.
   - Repository: `peppermint1231/grand-marketing-prompt-maker`
   - Branch: `main`
   - Main file path: `app.py`
3. Deploy 클릭 후 생성된 주소를 즐겨찾기 해두고 사용합니다.

## 사용 방식

1. STEP별 항목을 클릭 선택합니다.
2. 필요한 문구는 직접 입력합니다.
3. 프롬프트 상세도를 선택합니다.
   - 간단: ChatGPT 자유도 높음
   - 표준: 선택값과 디자인 균형
   - 상세: 입력 조건 중심으로 엄격하게 제작
4. 완료 버튼을 누르면 프롬프트가 생성됩니다.
5. 복사 버튼 또는 TXT 저장 버튼을 사용합니다.
