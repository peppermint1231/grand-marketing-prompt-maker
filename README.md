# 그랜드 마케팅 시안 제작 프롬프트 생성기

이미지 생성 API를 사용하지 않는 Streamlit 기반 프롬프트 생성기입니다.
항목을 클릭/입력하면 ChatGPT에 붙여넣을 이미지 제작 프롬프트가 자동 생성됩니다.

## 파일 구성
- `app.py` : Streamlit 앱 메인 파일
- `requirements.txt` : 필요한 패키지 목록
- `.streamlit/config.toml` : 화면 테마 설정

## 배포 방법
1. GitHub 레포 `grand-marketing-prompt-maker`에 이 파일들을 업로드합니다.
2. Streamlit Community Cloud에 로그인합니다.
3. Create app 클릭
4. Repository: `peppermint1231/grand-marketing-prompt-maker`
5. Branch: `main`
6. Main file path: `app.py`
7. Deploy 클릭

## 사용 방법
1. 제작 목적, 크기, 문구, 디자인 톤 등을 선택합니다.
2. 필요하면 직접 입력칸에 내용을 추가합니다.
3. 하단의 생성된 프롬프트를 복사합니다.
4. ChatGPT에 붙여넣고 이미지 제작을 요청합니다.

