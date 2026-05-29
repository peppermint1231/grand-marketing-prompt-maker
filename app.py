import streamlit as st
from datetime import datetime
import html
import json

st.set_page_config(
    page_title="그랜드 마케팅 시안 제작 프롬프트 생성기",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#f6f9fc;
  --card:#ffffff;
  --ink:#172033;
  --muted:#657386;
  --line:#dce7f3;
  --blue:#2f80ed;
  --blue2:#65b7ff;
  --navy:#12345b;
  --soft:#eef6ff;
  --orange:#ff8a3d;
}

html, body, [class*="css"] {font-family:'Noto Sans KR', sans-serif !important;}
.block-container{padding-top:2.2rem; max-width:1040px;}

.hero{
  position:relative; overflow:hidden; border-radius:30px; padding:36px 38px;
  background:linear-gradient(135deg, #ffffff 0%, #f3f9ff 52%, #eaf6ff 100%);
  border:1px solid rgba(47,128,237,.14);
  box-shadow:0 20px 60px rgba(19,52,91,.08);
  margin-bottom:26px;
}
.hero:after{
  content:""; position:absolute; width:360px; height:360px; right:-120px; top:-150px;
  background:radial-gradient(circle, rgba(101,183,255,.28), rgba(101,183,255,0) 62%);
}
.eyebrow{font-size:13px; letter-spacing:.16em; color:var(--blue); font-weight:800; margin-bottom:10px;}
.hero h1{font-size:42px; letter-spacing:-.045em; margin:0; line-height:1.18; color:var(--ink); font-weight:800;}
.hero p{margin:14px 0 0; font-size:17px; color:var(--muted); line-height:1.75;}

.step-card{
  background:rgba(255,255,255,.92); border:1px solid rgba(220,231,243,.9);
  border-radius:24px; padding:24px 26px; margin:0 0 18px;
  box-shadow:0 12px 36px rgba(19,52,91,.055);
}
.step-head{display:flex; align-items:center; gap:12px; margin-bottom:16px;}
.step-num{
  width:34px; height:34px; border-radius:12px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(135deg, #2f80ed, #68baff); color:white; font-weight:800; font-size:14px;
  box-shadow:0 10px 20px rgba(47,128,237,.2);
}
.step-title{font-size:21px; font-weight:800; color:var(--ink); letter-spacing:-.035em;}
.step-desc{font-size:13px; color:var(--muted); margin:-8px 0 16px 46px; line-height:1.55;}
.soft-divider{height:1px; background:linear-gradient(90deg, transparent, #dbe8f5 18%, #dbe8f5 82%, transparent); margin:20px 0;}

[data-testid="stMultiSelect"] label, [data-testid="stSelectbox"] label, [data-testid="stTextInput"] label, [data-testid="stTextArea"] label, [data-testid="stRadio"] label{
  font-weight:700 !important; color:var(--navy) !important;
}
.stButton > button{
  border-radius:14px !important; border:0 !important; background:linear-gradient(135deg,#2f80ed,#5aa8ff) !important;
  color:#fff !important; font-weight:800 !important; padding:.72rem 1.1rem !important;
  box-shadow:0 14px 28px rgba(47,128,237,.24) !important;
}
.stDownloadButton > button{
  border-radius:14px !important; border:1px solid #cfe0f2 !important; background:#fff !important;
  color:#12345b !important; font-weight:800 !important; padding:.72rem 1.1rem !important;
}
.result-card{
  background:#ffffff; border:1px solid rgba(220,231,243,.96); border-radius:26px;
  padding:26px; box-shadow:0 18px 50px rgba(19,52,91,.08); margin:22px 0 50px;
}
.result-title{font-size:22px; font-weight:800; color:var(--ink); margin-bottom:6px;}
.result-sub{font-size:13px; color:var(--muted); line-height:1.6; margin-bottom:16px;}
.pill-note{background:#eef6ff; color:#12345b; border:1px solid #d7eaff; border-radius:16px; padding:14px 16px; font-size:13px; line-height:1.6; margin-bottom:14px;}
.copybox{border-radius:18px; border:1px dashed #c8d8ea; background:#fbfdff; padding:16px; max-height:680px; overflow:auto; white-space:pre-wrap; color:#172033; font-size:14px; line-height:1.68;}
.copybtn{
  width:100%; border:0; cursor:pointer; margin:10px 0 10px; border-radius:14px; padding:13px 16px;
  color:#fff; font-weight:800; font-size:15px; background:linear-gradient(135deg,#172033,#2f80ed);
  box-shadow:0 14px 28px rgba(47,128,237,.24);
}
.small-muted{font-size:12px; color:#7a8899; line-height:1.55;}
.badge{display:inline-flex; align-items:center; gap:6px; border-radius:999px; background:#f0f7ff; border:1px solid #d8eaff; padding:6px 10px; color:#245a94; font-size:12px; font-weight:700; margin-right:6px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

def step_start(num: int, title: str, desc: str = ""):
    st.markdown(f"""
    <div class="step-card">
      <div class="step-head"><div class="step-num">{num}</div><div class="step-title">{title}</div></div>
      {f'<div class="step-desc">{desc}</div>' if desc else ''}
    """, unsafe_allow_html=True)

def step_end():
    st.markdown("</div>", unsafe_allow_html=True)

def join_list(values):
    if not values:
        return "미선택"
    return ", ".join(values)

def clean(value):
    if value is None:
        return "미입력"
    if isinstance(value, str) and value.strip() == "":
        return "미입력"
    return value

def make_prompt(data):
    detail = data["prompt_detail"]
    if detail.startswith("간단"):
        intro = "아래 조건을 참고해 ChatGPT의 디자인 감각을 살려 자유롭게 마케팅 이미지 시안을 제작해 주세요. 핵심 조건은 지키되, 전체 분위기와 레이아웃은 보기 좋게 제안해 주세요."
        strict = "자유롭게 재해석 가능하지만, 메인 문구·날짜·병원명 등 핵심 정보는 정확히 반영해 주세요."
    elif detail.startswith("상세"):
        intro = "아래 조건을 최대한 엄격하게 반영해 마케팅 이미지 시안을 제작해 주세요. 사용자가 입력한 문구, 레이아웃, 색감, 강조 요소를 우선하고 불필요한 임의 요소는 추가하지 마세요."
        strict = "입력 조건에서 벗어나지 말고, 오탈자 없이 깔끔하고 가독성 높은 결과물로 구성해 주세요."
    else:
        intro = "아래 조건을 기준으로 균형 잡힌 마케팅 이미지 시안을 제작해 주세요. 사용자가 선택한 조건을 중심으로 하되, 이미지 완성도를 위해 필요한 범위에서 자연스럽게 다듬어 주세요."
        strict = "사용자 조건과 디자인 완성도의 균형을 맞추고, 핵심 정보는 정확하게 반영해 주세요."

    prompt = f"""[이미지 제작 요청]

{intro}

1. 제작 용도
- 용도: {data['purpose']}
- 게시 위치: {clean(data['placement'])}
- 대상 고객: {clean(data['target'])}

2. 이미지 규격
- 크기: {data['size']}
- 사용 방식: {data['usage']}
- 파일 형식: {join_list(data['file_types'])}

3. 들어갈 문구
- 메인 제목: {clean(data['main_title'])}
- 서브 문구: {clean(data['sub_title'])}
- 상세 내용:
{clean(data['details'])}
- 하단 안내문구: {clean(data['bottom_note'])}
- 병원명 표기: {data['clinic_name']}

4. 디자인 톤
- 원하는 분위기: {join_list(data['moods'])}
- 색감: {join_list(data['colors'])}
- 원하지 않는 느낌: {join_list(data['avoid']) if data['avoid'] else clean(data['avoid_custom'])}

5. 참고 이미지 / 수정 방향
- 참고 이미지 사용 방식: {join_list(data['reference_use'])}
- 수정 요청: {clean(data['edit_request'])}

6. 레이아웃 / 가독성
- 레이아웃: {join_list(data['layouts'])}
- 강조할 부분: {clean(data['emphasis'])}
- 폰트 느낌: {join_list(data['fonts'])}
- 폰트/가독성 주의점: {clean(data['font_note'])}

7. 제작 기준
- 춘천 그랜드아름다운의원 홈페이지의 깔끔하고 신뢰감 있는 병원 스타일을 참고해 주세요.
- 전체적으로 깔끔하고 고급스러운 피부·미용 clinic marketing style, 프리미엄 병원 느낌, 가독성 높은 구성으로 제작해 주세요.
- 텍스트는 실제 병원 이벤트/안내 이미지처럼 읽기 쉽게 배치해 주세요.
- 제목, 핵심 문구, 안내 문구의 크기 위계를 명확히 잡아 주세요.
- 한글 문구와 날짜, 요일, 가격, 시술명에 오탈자가 없도록 특히 주의해 주세요.
- 실제 로고 파일이 제공되지 않았다면 임의 로고를 만들지 말고, 병원명은 깔끔한 텍스트로만 표기해 주세요.
- 배경은 너무 복잡하지 않게 하고, 중앙 문구가 잘 보이도록 여백을 충분히 주세요.
- 병원 홈페이지 팝업/이벤트 이미지에 바로 사용할 수 있는 완성도 높은 디자인으로 구성해 주세요.
- 고급스러운 포인트 컬러를 소량만 사용하고, 전체 분위기는 깔끔하게 유지해 주세요.
- {strict}
"""
    if detail.startswith("상세"):
        prompt += "\n8. 추가 엄수 사항\n- 사용자가 입력하지 않은 가격, 날짜, 시술명, 이벤트 조건은 임의로 만들지 마세요.\n- 글씨가 너무 작아지지 않게 하고, 모바일/홈페이지 팝업에서도 한눈에 읽히게 해 주세요.\n- 배경 장식보다 정보 전달과 가독성을 우선해 주세요.\n"
    return prompt.strip()

st.markdown("""
<div class="hero">
  <div class="eyebrow">GRAND PROMPT MAKER</div>
  <h1>그랜드 마케팅 시안 제작<br/>프롬프트 생성기</h1>
  <p>이미지 제작 조건을 클릭하고 필요한 문구만 입력하면, ChatGPT에 바로 붙여넣을 수 있는 이미지 제작 프롬프트가 자동으로 정리됩니다.</p>
</div>
""", unsafe_allow_html=True)

step_start(1, "제작 용도", "어디에 사용할 이미지인지 선택해 주세요. 필요하면 게시 위치와 대상 고객은 직접 입력할 수 있습니다.")
purpose = st.selectbox("용도", ["홈페이지 팝업", "인스타 피드", "인스타 스토리", "A4 안내문", "이벤트 배너", "병원 내부 부착물", "문자 발송 이미지", "카카오톡 이미지", "기타"])
c1, c2 = st.columns(2)
with c1:
    placement = st.text_input("게시 위치", placeholder="예: 홈페이지 메인 팝업")
with c2:
    target = st.text_input("대상 고객", placeholder="예: 신규 고객, 내원 환자")
step_end()

step_start(2, "이미지 규격", "사용할 화면이나 인쇄물에 맞는 크기를 선택해 주세요.")
c1, c2, c3 = st.columns([1,1,1])
with c1:
    size = st.selectbox("크기", ["800×800", "900×506", "1080×1080", "1080×1920", "A4 세로", "A4 가로", "기타"])
with c2:
    usage = st.selectbox("사용 방식", ["온라인용", "인쇄용", "온라인+인쇄용"])
with c3:
    file_types = st.multiselect("파일 형식", ["PNG", "JPG", "PDF", "PPT", "HWP용 이미지", "인쇄용 고화질", "수정 가능한 원본 필요"], default=["PNG"])
step_end()

step_start(3, "들어갈 문구", "제목과 본문은 정확히 입력할수록 결과물이 좋아집니다. 모르는 내용은 ‘조사해줘’처럼 적어도 됩니다.")
main_title = st.text_input("메인 제목", placeholder="예: 6월 휴진안내")
sub_title = st.text_input("서브 문구", placeholder="예: 6월 휴진 일정을 안내해드립니다.")
details = st.text_area("상세 내용", placeholder="예: 6월 3일 지방선거 / 6월 6일 현충일", height=130)
bottom_note = st.text_input("하단 안내문구", placeholder="예: VAT 별도 / 예약 필수 / 필요없음")
clinic_name = st.selectbox("병원명 표기", ["그랜드아름다운의원", "그랜드메디컬센터", "GRAND BEAUTY CLINIC", "표기 안 함", "기타"])
step_end()

step_start(4, "디자인 톤", "원하는 분위기와 색감을 선택해 주세요. 원하지 않는 느낌은 결과물의 방향을 잡는 데 중요합니다.")
moods = st.multiselect("원하는 분위기", ["깔끔한 병원 스타일", "고급스러운 프리미엄", "부드러운 여성스러운", "여름 느낌", "시원한 아쿠아", "심플한 안내문", "강남 피부과 이벤트 느낌", "차분하고 신뢰감 있는", "귀엽고 MZ 느낌"], default=["깔끔한 병원 스타일", "고급스러운 프리미엄"])
colors = st.multiselect("색감", ["화이트", "베이지", "골드베이지", "하늘색", "블루", "네이비", "핑크", "민트", "그레이", "블랙&화이트", "기존 색감 유지", "기타"], default=["화이트", "하늘색"])
avoid = st.multiselect("원하지 않는 느낌", ["촌스러운 그라데이션", "과한 장식", "너무 얇은 글씨", "복잡한 배경", "작은 글씨", "오탈자", "저가형 전단지 느낌", "과한 그림 요소"])
avoid_custom = st.text_input("원하지 않는 느낌 직접 입력", placeholder="예: 너무 유치한 느낌, 글씨가 흐린 느낌")
step_end()

step_start(5, "참고 이미지 / 수정 방향", "참고 이미지를 어떻게 활용할지 선택하고, 필요한 수정 요청을 입력해 주세요.")
reference_use = st.multiselect("참고 이미지 사용 방식", ["그대로 활용", "배경만 활용", "분위기만 참고", "색감만 참고", "레이아웃만 참고", "글씨만 수정", "사이즈만 변경"], default=["분위기만 참고"])
edit_request = st.text_area("수정 요청", placeholder="예: 춘천 그랜드아름다운의원 홈페이지 참고, 달력 형식", height=90)
step_end()

step_start(6, "레이아웃 / 가독성", "문구 배치와 강조할 부분을 선택해 주세요. 병원 안내 이미지는 가독성이 가장 중요합니다.")
layouts = st.multiselect("레이아웃", ["중앙 정렬", "왼쪽 정렬", "상단 제목+하단 내용", "가운데 큰 제목+아래 상세 내용", "카드형 박스 구성", "표 형식", "2단 구성", "3단 구성", "메뉴판 스타일", "포스터 스타일", "기존 이미지와 동일"], default=["중앙 정렬"])
emphasis = st.text_input("강조할 부분", placeholder="예: 휴진일, 가격, 이벤트명")
fonts = st.multiselect("폰트 느낌", ["기본 고딕체", "굵고 잘 보이는 글씨", "프리텐다드 느낌", "에스코어드림 느낌", "고급스러운 산세리프", "너무 얇지 않은 글씨", "기존 폰트 유지"], default=["굵고 잘 보이는 글씨", "고급스러운 산세리프"])
font_note = st.text_input("폰트/가독성 주의점", placeholder="예: 어르신도 잘 보이게 크게")
step_end()

step_start(7, "생성 옵션", "프롬프트 상세도에 따라 ChatGPT가 디자인을 자유롭게 해석할지, 입력 조건을 엄격하게 따를지 결정합니다.")
prompt_detail = st.radio(
    "프롬프트 상세도",
    ["간단 - ChatGPT 자유도 높음", "표준 - 자유도와 조건 반영 균형", "상세 - 이용자 요구사항 중심으로 엄격하게"],
    index=1,
    horizontal=False,
)
st.markdown("""
<div class="pill-note">
  <span class="badge">간단</span> 핵심 조건만 정리해 ChatGPT가 감각적으로 시안을 제안합니다.<br/>
  <span class="badge">표준</span> 선택값은 반영하되 디자인 완성도를 위해 자연스럽게 다듬습니다.<br/>
  <span class="badge">상세</span> 이용자가 입력한 조건을 최대한 그대로 지키도록 프롬프트를 촘촘하게 만듭니다.
</div>
""", unsafe_allow_html=True)
done = st.button("완료 · 프롬프트 생성", use_container_width=True)
step_end()

data = dict(
    purpose=purpose, placement=placement, target=target,
    size=size, usage=usage, file_types=file_types,
    main_title=main_title, sub_title=sub_title, details=details,
    bottom_note=bottom_note, clinic_name=clinic_name,
    moods=moods, colors=colors, avoid=avoid, avoid_custom=avoid_custom,
    reference_use=reference_use, edit_request=edit_request,
    layouts=layouts, emphasis=emphasis, fonts=fonts, font_note=font_note,
    prompt_detail=prompt_detail,
)

prompt = make_prompt(data)

st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.markdown('<div class="result-title">생성된 프롬프트</div>', unsafe_allow_html=True)
st.markdown('<div class="result-sub">위 항목을 모두 선택한 뒤, 아래 프롬프트를 복사해서 ChatGPT에 붙여넣으면 이미지 제작 요청문으로 바로 사용할 수 있습니다.</div>', unsafe_allow_html=True)

escaped = html.escape(prompt)
prompt_json = json.dumps(prompt)
st.markdown(f'<div class="copybox" id="promptBox">{escaped}</div>', unsafe_allow_html=True)
st.components.v1.html(f"""
<button class="copybtn" onclick='navigator.clipboard.writeText({prompt_json}).then(()=>{{document.getElementById("msg").innerText="복사 완료! ChatGPT에 붙여넣어 주세요."}}).catch(()=>{{document.getElementById("msg").innerText="복사가 안 되면 아래 프롬프트를 직접 드래그해서 복사해 주세요."}})'>프롬프트 복사하기</button>
<div id="msg" style="font-family:Arial,sans-serif;font-size:13px;color:#2f80ed;font-weight:700;margin-bottom:10px;"></div>
<style>
.copybtn{{width:100%;border:0;cursor:pointer;border-radius:14px;padding:13px 16px;color:#fff;font-weight:800;font-size:15px;background:linear-gradient(135deg,#172033,#2f80ed);box-shadow:0 14px 28px rgba(47,128,237,.24);}}
</style>
""", height=72)
st.download_button(
    "TXT로 저장하기",
    data=prompt,
    file_name=f"grand_prompt_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
    use_container_width=True,
)
st.markdown('<div class="small-muted">※ 이 앱은 API Key 없이 프롬프트만 생성합니다. 이미지는 ChatGPT 채팅창에 붙여넣어 생성하면 됩니다.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
