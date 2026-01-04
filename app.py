import streamlit as st
from datetime import date
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="오늘의 별자리 운세",
    page_icon="🔮",
    layout="centered",
)

# -----------------------------
# CSS (폰트/상단 배너 제거/버튼/다크 UI)
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;800&display=swap');

:root{
  --bg:#0b0f1a;
  --card:rgba(255,255,255,.06);
  --line:rgba(255,255,255,.10);
  --text:#e8edf7;
  --muted:#a8b3c7;
  --a1:#7c5cff;
  --a2:#38d39f;
}

html, body, [data-testid="stAppViewContainer"]{
  font-family:'Noto Sans KR', system-ui, -apple-system, sans-serif !important;
  background:
    radial-gradient(900px 500px at 20% -10%, rgba(124,92,255,.35), transparent 60%),
    radial-gradient(900px 500px at 80% 10%, rgba(56,211,159,.20), transparent 55%),
    var(--bg) !important;
  color:var(--text) !important;
}

/* 상단 흰 배너/툴바 제거 */
[data-testid="stHeader"]{background:transparent !important; height:0 !important;}
[data-testid="stToolbar"]{display:none !important;}
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
.block-container{max-width:560px; padding-top:12px;}

/* 카드 */
.card{
  border:1px solid var(--line);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border-radius:18px;
  padding:16px;
  box-shadow:0 10px 30px rgba(0,0,0,.35);
}
.badge{
  display:inline-block; padding:6px 10px; border-radius:999px; font-size:12px;
  background:rgba(124,92,255,.14); border:1px solid rgba(124,92,255,.30);
  color:#e7e2ff; margin-bottom:8px;
}
.h1{font-size:22px; font-weight:800; letter-spacing:-.3px; margin:0;}
.sub{color:var(--muted); font-size:13px; margin-top:6px;}
.hr{height:1px; background:var(--line); margin:12px 0;}
.kv{color:var(--muted); font-size:12px;}
.big{font-size:18px; font-weight:800; margin:2px 0;}
.small{font-size:14px; line-height:1.55;}
.pill{
  display:inline-flex; gap:8px; align-items:center; padding:8px 10px;
  border-radius:999px; border:1px solid var(--line);
  background:rgba(255,255,255,.04); color:var(--muted); font-size:12px;
}

/* 버튼 (흰색 방지) */
div.stButton > button{
  width:100%; border:none !important; border-radius:14px !important;
  padding:.85rem 1rem !important; font-weight:800 !important;
  color:#fff !important;
  background:linear-gradient(135deg, var(--a1), var(--a2)) !important;
}
div.stButton > button:hover{filter:brightness(1.05);}
div.stButton > button:disabled{
  opacity:.45 !important; cursor:not-allowed !important;
  background:rgba(255,255,255,.12) !important;
  color:rgba(255,255,255,.7) !important;
}

/* 입력 */
[data-testid="stDateInput"] input{border-radius:14px !important;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 별자리 계산
# -----------------------------
def get_zodiac(month, day):
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "염소자리"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "물병자리"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "물고기자리"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "양자리"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "황소자리"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "쌍둥이자리"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "게자리"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "사자자리"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "처녀자리"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
        return "천칭자리"
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "전갈자리"
    else:
        return "사수자리"

# -----------------------------
# 조합형 운세 엔진 (반복 체감 ↓)
# -----------------------------
TONES = ["차분한","신중한","유연한","집중되는","정리되는","속도가 붙는","선택이 중요한","변수 많은"]
AREAS = ["일정","금전","관계","업무","결정","연락","컨디션","우선순위"]
ACTIONS = ["정리","확인","조정","대화","집중","휴식","보류","재점검"]

OPENERS = [
    "오늘 전체 흐름은 {tone} 방향입니다.",
    "당장 결과보다 {tone} 판단이 유리한 날입니다.",
    "초반은 흔들려도 {tone} 기준을 잡으면 안정됩니다.",
]
SITUATIONS = [
    "{area} 쪽에서 작은 변수가 생길 수 있습니다.",
    "{area}은(는) 급하게 밀어붙이지 않는 게 좋습니다.",
    "{area}은(는) 1~2가지만 확실히 잡으면 충분합니다.",
]
ADVICES = [
    "{action}을 먼저 하면 불필요한 소모를 줄일 수 있습니다.",
    "{action} 기준으로 판단하면 오차가 줄어듭니다.",
]
CARES = [
    "급한 결론은 피하세요. 한 박자 늦추는 쪽이 이득입니다.",
    "숫자/조건 재확인이 필요합니다.",
]
CLOSERS = [
    "서두르지 않아도 결과는 따라옵니다.",
    "오늘은 속도보다 방향이 중요합니다.",
]
LUCKY_COLORS = ["파랑","초록","보라","회색","베이지","남색"]
LUCKY_TIMES = ["오전 9~11시","점심 직후","오후 2~4시","저녁 7~9시"]
LUCKY_NUMBERS = list(range(1,37))

def generate_fortune(zodiac, birth):
    seed = int(date.today().strftime("%Y%m%d")) + int(birth.strftime("%Y%m%d")) + sum(ord(c) for c in zodiac)
    random.seed(seed)
    tone = random.choice(TONES)
    area = random.choice(AREAS)
    action = random.choice(ACTIONS)
    return {
        "date": date.today().strftime("%Y.%m.%d"),
        "zodiac": zodiac,
        "scores": {
            "overall": random.randint(1,5),
            "money": random.randint(1,5),
            "love": random.randint(1,5),
            "work": random.randint(1,5),
        },
        "oneLine": random.choice(OPENERS).format(tone=tone),
        "flow": random.choice(SITUATIONS).format(area=area),
        "care": random.choice(CARES),
        "action": random.choice(ADVICES).format(action=action),
        "summary": random.choice(CLOSERS),
        "lucky": {
            "color": random.choice(LUCKY_COLORS),
            "time": random.choice(LUCKY_TIMES),
            "number": random.choice(LUCKY_NUMBERS),
        }
    }

# -----------------------------
# UI
# -----------------------------
st.markdown('<div class="h1">오늘의 별자리 운세</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">생일만 입력하면 별자리는 자동 계산됩니다 · 카드 요약</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
birth = st.date_input(
    "생년월일",
    value=None,
    min_value=date(1900,1,1),
    max_value=date.today(),
    format="YYYY-MM-DD"
)
btn = st.button("운세 보기", use_container_width=True, disabled=(birth is None))
st.markdown('</div>', unsafe_allow_html=True)

if btn and birth:
    zodiac = get_zodiac(birth.month, birth.day)
    f = generate_fortune(zodiac, birth)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">요약 운세</span>', unsafe_allow_html=True)

    l, r = st.columns([0.7,0.3])
    with l:
        st.markdown(f'<div class="big">{f["zodiac"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kv">{f["date"]} 기준</div>', unsafe_allow_html=True)
    with r:
        st.markdown(f'<div class="pill">🍀 {f["lucky"]["color"]} · {f["lucky"]["number"]} · {f["lucky"]["time"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    st.caption("종합운"); st.progress(f["scores"]["overall"]/5)
    st.caption("금전운"); st.progress(f["scores"]["money"]/5)
    st.caption("연애운"); st.progress(f["scores"]["love"]/5)
    st.caption("직장운"); st.progress(f["scores"]["work"]/5)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("#### 한 줄 조언"); st.markdown(f'<div class="small">{f["oneLine"]}</div>', unsafe_allow_html=True)
    st.markdown("#### 오늘의 흐름"); st.markdown(f'<div class="small">{f["flow"]}</div>', unsafe_allow_html=True)

    with st.expander("자세히 보기"):
        st.markdown("**조심할 점**"); st.write(f["care"])
        st.markdown("**추천 행동**"); st.write(f["action"])
        st.markdown("**마무리**"); st.write(f["summary"])

    st.markdown('</div>', unsafe_allow_html=True)

st.caption("※ 조합형 문장 기반 MVP · 반복 체감 최소화")
