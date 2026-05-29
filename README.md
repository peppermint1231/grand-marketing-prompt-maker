# 그랜드 마케팅 시안 제작 프롬프트 생성기

이미지 제작 조건을 클릭/입력하면 ChatGPT에 붙여넣을 수 있는 이미지 제작 프롬프트를 자동 생성하는 Streamlit 앱입니다.

## 주요 기능

- API Key 없이 프롬프트만 생성
- 1단 구성 레이아웃
- 생성된 프롬프트는 페이지 가장 아래에 표시
- 프롬프트 상세도 선택
  - 간단: ChatGPT 자유도 높음
  - 표준: 자유도와 조건 반영 균형
  - 상세: 이용자 요구사항 중심으로 엄격하게
- 프롬프트 복사 버튼
- TXT 저장 버튼

## 배포 방법

1. GitHub 레포에 아래 파일을 업로드합니다.
   - app.py
   - requirements.txt
   - README.md
   - .streamlit/config.toml
2. Streamlit Community Cloud에서 해당 레포를 선택합니다.
3. Main file path는 `app.py`로 설정합니다.
4. Deploy를 누릅니다.
