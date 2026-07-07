import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="우리만의 인스타 맛집 지도", page_icon="📸", layout="wide")

st.title("📸 인스타 릴스 맛집 아카이빙 스토리지")
st.write("인스타그램에서 본 릴스 링크를 추가하고 데이트 지도를 만들어보세요!")

# 세션 상태에 맛집 데이터 저장 공간 만들기
if "insta_places" not in st.session_state:
    st.session_state.insta_places = [
        {
            "name": "연남취향",
            "url": "https://www.instagram.com/reels/C8Bv8S_y_Y_/", # 예시 링크
            "memo": "파스타 비주얼 대박인 곳, 주말 웨이팅 있음!"
        }
    ]

# --- 왼쪽: 맛집 추가하기 폼 ---
with st.sidebar:
    st.header("📌 새 맛집 추가하기")
    with st.form("add_place_form", clear_on_submit=True):
        place_name = st.text_input("📍 식당 이름", placeholder="예: 성수 소문난감자탕")
        reels_url = st.text_input("🔗 릴스/게시글 링크", placeholder="https://www.instagram.com/p/... 또는 /reels/...")
        memo = st.text_area("✍️ 메모 (추천 메뉴 등)", placeholder="예: 매콤한 크림파스타 필수 주문")
        
        submitted = st.form_submit_button("맛집 지지도에 추가")
        
        if submitted:
            if place_name and reels_url:
                # 인스타 주소 표준화 (뒤에 /embed/를 붙이기 위함)
                if not reels_url.endswith("/"):
                    reels_url += "/"
                
                st.session_state.insta_places.append({
                    "name": place_name,
                    "url": reels_url,
                    "memo": memo
                })
                st.success(f"🎉 '{place_name}' 저장 완료!")
                st.rerun()
            else:
                st.error("식당 이름과 릴스 링크는 필수입니다!")

# --- 오른쪽: 저장된 맛집 리스트 & 릴스 보기 ---
st.subheader("🗺️ 우리가 저장한 데이트 맛집 리스트")

if not st.session_state.insta_places:
    st.info("아직 저장된 맛집이 없습니다. 왼쪽 사이드바에서 첫 맛집을 추가해보세요!")
else:
    # 테이블 형태로 먼저 보기
    df = pd.DataFrame(st.session_state.insta_places)
    st.dataframe(df[["name", "memo"]], use_container_width=True)
    
    st.write("---")
    st.subheader("🎬 맛집 릴스 & 위치 확인하기")
    
    # 저장된 맛집들을 바둑판(Grid) 형태로 배치
    places = st.session_state.insta_places
    cols = st.columns(2) # 2열 구성
    
    for idx, place in enumerate(places):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### 📍 {place['name']}")
                st.write(f"💬 {place['memo']}")
                
                # 지도 검색 링크 제공 (네이버 지도, 구글 지도 바로가기 버튼)
                naver_map_url = f"https://map.naver.com/v5/search/{place['name']}"
                google_map_url = f"https://www.google.com/maps/search/{place['name']}"
                
                map_col1, map_col2 = st.columns(2)
                map_col1.markdown(f"[🟢 네이버 지도에서 보기]({naver_map_url})")
                map_col2.markdown(f"[🔵 구글 지도에서 보기]({google_map_url})")
                
                # 💡 핵심: 인스타그램 릴스 임베드 (iframe 활용)
                # 링크 뒤에 'embed'를 붙이면 인스타 웹 뷰어가 뜹니다.
                embed_url = f"{place['url']}embed"
                
                components.iframe(embed_url, height=450, scrolling=True)
