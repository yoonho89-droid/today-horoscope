import streamlit as st
from datetime import date
import random

# -----------------------------
# 페이지 설정 (이 블록엔 이것만!)
# -----------------------------
st.set_page_config(
    page_title="오늘의 별자리 운세",
    page_icon="🔮",
    layout="centered",
)

# -----------------------------
# 유튜브 채널 버튼 (모바일 안정)
# -----------------------------
YOUTUBE_CHANNEL = "https://www.youtube.com/channel/UCzom9LzxN8wTioBPnMSSadg"

try:
    st.link_button("▶️ 해외 동요 유튜브 채널", YOUTUBE_CHANNEL)
except Exception:
    st.markdown(f"▶️ [해외 동요 유튜브 채널 바로가기]({YOUTUBE_CHANNEL})")

# -----------------------------
# CSS (하나만! <style>도 하나만!)
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;800&display=swap');

/* ✅ 유튜브 버튼(st.link_button) 강제 표시 + 스타일 고정 */
[data-testid="stLinkButton"] {
  display: flex !important;
  justify-content: center !important;
  margin: 10px 0 20px 0 !important;
}
[data-testid="stLinkButton"] a {
  display: block !important;
  width: 100% !important;
  max-width: 420px !important;
  padding: 14px 16px !important;
  border-radius: 14px !important;
  background: #ff0000 !important;
  color: #ffffff !important;
  font-weight: 800 !important;
  text-decoration: none !important;
  text-align: center !important;
}
a, a:visited { color: #ffffff !important; }

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
