import streamlit as st
from datetime import date

st.set_page_config(
    page_title="그랜드 마케팅 시안 제작 프롬프트 생성기",
    page_icon="✨",
    layout="wide",
)

BRAND_DEFAULTS = {
    "brand_name": "춘천 그랜드아름다운의원",
    "style": "깔끔하고 고급스러운 피부·미용 clinic marketing style, 프리미엄 병원 느낌, 가독성 높은 구성",
    "avoid": "촌스러운 그라데이션, 과한 장식, 너무 얇은 글씨, 복잡한 배경, 작은 글씨, 오탈자",
}

CSS = """
<style>
.block-container {padding-top: 2rem; padding-bottom: 4rem; max-width: 1320px;}
.grand-title {font-size: 2.4rem; font-weight: 900; letter-spacing: -0.04em; margin-bottom: .2rem; color: #111827;}
.grand-sub {font-size: 1.05rem; color: #667085; margin-bottom: 1.4rem;}
.card {background: white; border: 1px solid #E5E7EB; border-radius: 22px; padding: 1.2rem 1.35rem; box-shadow: 0 8px 24px rgba(15,23,42,.04); margin-bottom: 1rem;}
.section-title {font-size: 1.22rem; font-weight: 800; color: #111827; margin-bottom: .45rem;}
.small-note {font-size:.9rem; color:#667085;}
.result-box {background:#0F172A; color:#F8FAFC; border-radius:18px; padding:1rem; white-space:pre-wrap; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size:.93rem; line-height:1.55;}
.badge {display:inline-block; padding:.22rem .55rem; border-radius:999px; background:#EEF4FF; color:#2563EB; font-size:.82rem; font-weight:700; margin-bottom:.45rem;}
.copy-guide {background:#FFF7ED; border:1px solid #FED7AA; color:#9A3412; border-radius:14px; padding:.85rem 1rem; margin-top:.8rem;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------- helpers -----------------------------
def select_chips(label, options, default=None, key=None, help_text=None):
    return st.radio(label, options, horizontal=True, index=options.index(default) if default in options else 0, key=key, help=help_text)

def multi(label, options, default=None, key=None):
    return st.multiselect(label, options, default=default or [], key=key)

def join_list(items):
    return ", ".join([x for x in items if x]) if items else "미선택"

def clean(value, fallback="미입력"):
    if value is None:
        return fallback
    value = str(value).strip()
    return value if value else fallback

# ----------------------------- Header -----------------------------
st.markdown('<div class="grand-title">그랜드 마케팅 시안 제작 프롬프트 생성기</div>', unsafe_allow_html=True)
st.markdown('<div class="grand-sub">클릭으로 조건을 고르고, 필요한 문구만 입력하면 ChatGPT 이미지 제작용 프롬프트가 자동으로 정리됩니다. OpenAI API Key는 사용하지 않습니다.</div>', unsafe_allow_html=True)

left, right = st.columns([1.18, .82], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 1</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">기본 정보</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        purpose = select_chips("제작 용도", ["홈페이지 팝업", "인스타 피드", "인스타 스토리", "A4 안내문", "이벤트 배너", "병원 내부 부착물", "문자 발송 이미지", "카카오톡 이미지", "기타"], "홈페이지 팝업", "purpose")
        purpose_custom = st.text_input("기타 용도/게시 위치 직접 입력", placeholder="예: 홈페이지 메인 팝업, 관리실 침대 옆 안내문")
    with c2:
        target = st.text_input("대상 고객", placeholder="예: 신규 고객, 내원 환자, 20~30대, 중장년층")
        post_location = st.text_input("게시 위치", placeholder="예: 홈페이지 팝업, 인스타그램, 원내 게시")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 2</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">이미지 규격</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.1, .8, .9])
    with c1:
        size = select_chips("크기", ["800×800", "900×506", "1080×1080", "1080×1920", "A4 세로", "A4 가로", "기타"], "800×800", "size")
        size_custom = st.text_input("기타 크기 직접 입력", placeholder="예: 900×506px, 42cm×90cm")
    with c2:
        use_type = select_chips("사용 방식", ["온라인용", "인쇄용", "둘 다"], "온라인용", "use_type")
    with c3:
        file_type = multi("필요 파일 형식", ["PNG", "JPG", "PDF", "PPT", "HWP용 이미지", "인쇄용 고화질", "수정 가능한 원본 필요"], ["PNG"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 3</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">들어갈 문구</div>', unsafe_allow_html=True)
    title = st.text_input("메인 제목", placeholder="예: 6월 휴진 안내 / 그랜드 6월 제모 이벤트")
    subtitle = st.text_input("서브 문구", placeholder="예: 6월 휴진 일정을 안내드립니다")
    detail = st.text_area("상세 내용", height=120, placeholder="예: 6월 3일 지방선거, 6월 6일 현충일\n또는 시술명/가격/구성 입력")
    footer = st.text_input("하단 안내문구", placeholder="예: VAT 별도 / 예약 필수 / 마취크림 별도")
    brand_option = select_chips("병원명 표기", ["그랜드아름다운의원", "춘천 그랜드아름다운의원", "그랜드메디컬센터", "GRAND BEAUTY CLINIC", "표기 안 함", "기타"], "그랜드아름다운의원", "brand_option")
    brand_custom = st.text_input("기타 병원명/브랜드명 직접 입력", placeholder="예: G 그랜드아름다운의원")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 4</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">디자인 톤</div>', unsafe_allow_html=True)
    mood = multi("원하는 분위기", ["깔끔한 병원 스타일", "고급스러운 프리미엄", "부드러운 여성스러운", "여름 느낌", "시원한 아쿠아", "심플한 안내문", "강남 피부과 이벤트 느낌", "차분하고 신뢰감 있는", "귀엽고 MZ 느낌", "Apple 스타일", "피부과 이벤트 스타일"], ["깔끔한 병원 스타일", "고급스러운 프리미엄"])
    colors = multi("색감", ["화이트", "베이지", "골드베이지", "하늘색", "블루", "네이비", "핑크", "민트", "그레이", "블랙&화이트", "기존 이미지 색감 유지", "기타"], [])
    color_custom = st.text_input("기타 색감 직접 입력", placeholder="예: 화이트+소프트 블루, 골드베이지 포인트")
    avoid = st.text_area("원하지 않는 느낌", height=80, value=BRAND_DEFAULTS["avoid"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 5</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">참고 이미지 / 수정 방향</div>', unsafe_allow_html=True)
    ref_mode = multi("참고 이미지 사용 방식", ["그대로 활용", "배경만 활용", "분위기만 참고", "색감만 참고", "레이아웃만 참고", "글씨만 수정", "사이즈만 변경", "홈페이지 참고"], ["분위기만 참고"])
    modify = st.text_area("수정 요청 / 참고 방향", height=90, placeholder="예: 춘천 그랜드아름다운의원 홈페이지 참고, 달력 형식, 휴진 안내")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 6</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">레이아웃 / 가독성</div>', unsafe_allow_html=True)
    layout = multi("레이아웃", ["중앙 정렬", "왼쪽 정렬", "상단 제목 + 하단 내용", "가운데 큰 제목 + 아래 상세 내용", "카드형 박스 구성", "표 형식", "2단 구성", "3단 구성", "메뉴판 스타일", "포스터 스타일", "기존 이미지와 동일", "달력 형식"], ["중앙 정렬"])
    emphasis = st.text_input("강조할 부분", placeholder="예: 가격, 이벤트명, 휴진일, 병원명")
    font = multi("폰트 느낌", ["기본 고딕체", "굵고 잘 보이는 글씨", "프리텐다드 느낌", "에스코어드림 느낌", "고급스러운 산세리프", "너무 얇지 않은 글씨", "기존 폰트 유지"], ["굵고 잘 보이는 글씨", "고급스러운 산세리프"])
    readability = st.text_area("폰트/가독성 주의점", height=80, placeholder="예: 어르신도 잘 보이게 크게, 제목은 강하게, 가격은 더 크게")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">STEP 7</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">생성 옵션</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        prompt_strength = select_chips("프롬프트 상세도", ["간단", "표준", "상세"], "상세", "prompt_strength")
    with c2:
        typo_caution = st.checkbox("한글 오탈자 방지 문구 강하게 넣기", value=True)
        no_logo = st.checkbox("로고는 임의 생성하지 않기", value=True)
    deadline = st.text_input("마감일", placeholder="예: 오늘 중, 내일 오전")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- Prompt creation -----------------------------
final_purpose = purpose_custom if purpose == "기타" and purpose_custom.strip() else purpose
final_size = size_custom if size == "기타" and size_custom.strip() else size
final_brand = "" if brand_option == "표기 안 함" else (brand_custom if brand_option == "기타" and brand_custom.strip() else brand_option)
final_colors = join_list(colors + ([color_custom] if color_custom.strip() else []))
final_style = join_list(mood)
final_ref = join_list(ref_mode)

base_prompt = f"""[이미지 제작 요청]

아래 조건에 맞춰 마케팅 이미지 시안을 제작해 주세요.

1. 제작 용도
- 용도: {clean(final_purpose)}
- 게시 위치: {clean(post_location)}
- 대상 고객: {clean(target)}

2. 이미지 규격
- 크기: {clean(final_size)}
- 사용 방식: {clean(use_type)}
- 파일 형식: {join_list(file_type)}

3. 들어갈 문구
- 메인 제목: {clean(title)}
- 서브 문구: {clean(subtitle)}
- 상세 내용:\n{clean(detail)}
- 하단 안내문구: {clean(footer)}
- 병원명 표기: {clean(final_brand, '표기 안 함')}

4. 디자인 톤
- 원하는 분위기: {final_style}
- 색감: {final_colors}
- 원하지 않는 느낌: {clean(avoid)}

5. 참고 이미지 / 수정 방향
- 참고 이미지 사용 방식: {final_ref}
- 수정 요청: {clean(modify)}

6. 레이아웃 / 가독성
- 레이아웃: {join_list(layout)}
- 강조할 부분: {clean(emphasis)}
- 폰트 느낌: {join_list(font)}
- 폰트/가독성 주의점: {clean(readability)}

7. 제작 기준
- 춘천 그랜드아름다운의원 홈페이지의 깔끔하고 신뢰감 있는 병원 스타일을 참고해 주세요.
- 전체적으로 {BRAND_DEFAULTS['style']}로 제작해 주세요.
- 텍스트는 실제 병원 이벤트/안내 이미지처럼 읽기 쉽게 배치해 주세요.
- 제목, 핵심 문구, 안내 문구의 크기 위계를 명확히 잡아 주세요.
"""

extra = []
if typo_caution:
    extra.append("- 한글 문구와 날짜, 요일, 가격, 시술명에 오탈자가 없도록 특히 주의해 주세요.")
if no_logo:
    extra.append("- 실제 로고 파일이 제공되지 않았다면 임의 로고를 만들지 말고, 병원명은 깔끔한 텍스트로만 표기해 주세요.")
if prompt_strength == "상세":
    extra.extend([
        "- 배경은 너무 복잡하지 않게 하고, 중앙 문구가 잘 보이도록 여백을 충분히 주세요.",
        "- 병원 홈페이지 팝업/이벤트 이미지에 바로 사용할 수 있는 완성도 높은 디자인으로 구성해 주세요.",
        "- 고급스러운 포인트 컬러를 소량만 사용하고, 전체 분위기는 깔끔하게 유지해 주세요.",
    ])
elif prompt_strength == "간단":
    extra.append("- 간결하고 깔끔한 구성으로 제작해 주세요.")

if deadline.strip():
    extra.append(f"- 마감 참고: {deadline.strip()}")

final_prompt = base_prompt + "\n" + "\n".join(extra)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">PROMPT</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">완성된 ChatGPT 이미지 생성 프롬프트</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-note">아래 내용을 복사해서 ChatGPT에 그대로 붙여넣으면 됩니다.</div>', unsafe_allow_html=True)
    st.text_area("프롬프트 결과", value=final_prompt, height=620, label_visibility="collapsed")
    st.download_button("프롬프트 TXT 저장", data=final_prompt, file_name="grand_marketing_prompt.txt", mime="text/plain")
    st.markdown('<div class="copy-guide">복사는 결과창 안을 클릭한 뒤 Ctrl+A → Ctrl+C를 누르면 가장 확실합니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">빠른 예시</div>', unsafe_allow_html=True)
    if st.button("예시: 6월 휴진 안내 자동 입력"):
        st.session_state["purpose"] = "홈페이지 팝업"
        st.session_state["size"] = "800×800"
        st.rerun()
    st.markdown("""
    - 제목: 6월 휴진 안내  
    - 내용: 6월 3일 지방선거 / 6월 6일 현충일  
    - 레이아웃: 달력 형식 + 중앙 정렬  
    - 분위기: 깔끔한 병원 스타일 + 고급스러운 프리미엄
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("© GRAND Marketing Prompt Maker | API Key 없이 프롬프트만 생성하는 도구")
