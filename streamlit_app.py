"""ARTSPOT: a no-key Streamlit exhibition discovery demo."""

import csv
import io
from datetime import date
from pathlib import Path

import streamlit as st

from scripts.process_exhibitions import load_exhibitions

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="ARTSPOT | 서울 전시 탐색", page_icon="🎨", layout="wide")

st.markdown("""<style>
  .stApp { background: #faf8f4; }
  h1, h2, h3 { color: #25382c; }
  [data-testid="stMetric"] { background: #eeeae1; border-radius: 12px; padding: 16px; }
  .block-container { max-width: 1100px; padding-top: 2.5rem; }
</style>""", unsafe_allow_html=True)

DISTRICTS = {"Jongno-gu": "종로구", "Jung-gu": "중구", "Seongdong-gu": "성동구", "Mapo-gu": "마포구"}
GENRES = {"Painting": "회화", "Photography": "사진", "Media Art": "미디어아트", "Sculpture": "조각"}

st.caption("SEOUL ART EXHIBITION DISCOVERY · WEEK 10 PROJECT")
st.title("ARTSPOT")
st.markdown("### 나의 취향으로 찾는 전시 한 편")
st.write("날짜와 예산, 관심 지역과 장르를 골라 전시를 탐색해 보세요.")
st.warning("학습용 데모입니다. 전시명·전시장·일정·요금은 모두 가상 예시이며 실제 전시 정보가 아닙니다.")

try:
    records = load_exhibitions(ROOT / "data/exhibitions.csv")
except (OSError, ValueError) as exc:
    st.error(f"예시 데이터를 읽을 수 없습니다: {exc}")
    st.stop()

with st.sidebar:
    st.header("나의 전시 조건")
    st.caption("처음에는 예시 날짜로 설정됩니다.")
    selected_date = st.date_input("방문 날짜", value=date(2026, 11, 3))
    budget = st.slider("최대 관람료 (원)", 0, 30000, 10000, step=1000)
    district = st.selectbox("지역", ["전체"] + sorted({DISTRICTS.get(r["district"], r["district"]) for r in records}))
    genre = st.selectbox("장르", ["전체"] + sorted({GENRES.get(r["genre"], r["genre"]) for r in records}))
    order = st.selectbox("정렬", ["관람료 낮은 순", "종료일 빠른 순"])
    st.divider()
    st.caption("API 키 없이 사용할 수 있습니다. 선택한 조건은 개인 계정에 저장하지 않습니다.")
    st.link_button("GitHub 프로젝트 보기", "https://github.com/tjsgud10/ARTSPOT")

active = [r for r in records if date.fromisoformat(r["start_date"]) <= selected_date <= date.fromisoformat(r["end_date"])]
matches = [r for r in active if r["price_krw"] <= budget
           and (district == "전체" or DISTRICTS.get(r["district"], r["district"]) == district)
           and (genre == "전체" or GENRES.get(r["genre"], r["genre"]) == genre)]
sort_key = (lambda r: (r["price_krw"], r["end_date"], r["id"])) if order == "관람료 낮은 순" else (lambda r: (r["end_date"], r["price_krw"], r["id"]))
matches.sort(key=sort_key)

cols = st.columns(3)
cols[0].metric("전체 예시 전시", f"{len(records)}건")
cols[1].metric("선택 날짜의 전시", f"{len(active)}건")
cols[2].metric("조건에 맞는 전시", f"{len(matches)}건")
st.divider()
st.subheader("추천 전시")
st.caption(f"{selected_date.isoformat()} · {budget:,}원 이하 · {district} · {genre}")

if not matches:
    st.info("조건에 맞는 예시 전시가 없습니다. 예산을 늘리거나 지역·장르를 전체로 바꿔 보세요. 2026-11-03에는 예시 전시 3건이 있습니다.")
else:
    for row in matches:
        with st.container(border=True):
            left, right = st.columns([4, 1])
            left.caption(f"가상 전시 · {GENRES.get(row['genre'], row['genre'])} · {DISTRICTS.get(row['district'], row['district'])}")
            left.subheader(row["title"])
            left.write(f"{row['venue']} | {row['start_date']} ~ {row['end_date']}")
            right.metric("예시 관람료", "무료" if row["price_krw"] == 0 else f"{row['price_krw']:,}원")
    export = io.StringIO(newline="")
    writer = csv.DictWriter(export, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(matches)
    st.download_button("추천 목록 CSV 다운로드", export.getvalue().encode("utf-8-sig"), file_name="artspot_sample_recommendations.csv", mime="text/csv")

with st.expander("전체 예시 데이터 보기"):
    st.dataframe(records, hide_index=True, use_container_width=True)
with st.expander("이 프로젝트는 어떻게 동작하나요?"):
    st.write("CSV 파일을 읽고 방문 날짜, 예산, 지역, 장르로 필터링합니다. 추천은 명시된 조건과 정렬 규칙에 따른 결과이며 AI 개인화 추천이 아닙니다.")
    st.write("GitHub Actions는 같은 CSV를 Python으로 처리하고 결과를 저장합니다. 웹앱은 저장소의 CSV를 직접 읽습니다.")
st.caption("ARTSPOT · 예술과 고급 빅데이터 10주차 실습 · Fictional sample data only")
