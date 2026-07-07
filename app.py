import streamlit as st
import random
import time

st.set_page_config(page_title="나만의 맛집 보물상자", page_icon="💝", layout="wide")

# 임시 데이터베이스 (기본 데이터 예시)
# 이미지는 테스트용 오픈 소스 주소입니다. 나중에 실제 음식 사진 URL로 바꾸시면 됩니다!
if "my_restaurants" not in st.session_state:
    st.session_state.my_restaurants = [
        {
            "name": "성수 오레노카츠",
            "category": "일식",
            "region": "성수동",
            "menu_pic": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?q=80&w=400",
            "desc": "체다치즈 돈카츠가 비주얼 폭발하는 곳!"
        },
        {
            "name": "성수 쵸리상경",
            "category": "한식",
            "region": "성수동",
            "menu_pic": "https://images.unsplash.com/photo-1608897013039-887f21d8c804?q=80&w=400",
            "desc": "깔끔하고 정갈한 솥밥 맛집, 웨이팅 필수"
        },
        {
            "name": "동탄 포레스트",
            "category": "퓨전/아시안",
            "region": "동탄",
            "menu_pic": "https://images.unsplash.com/photo-1552611052-33e04de081de?q=80&w=400",
            "desc": "왕갈비 쌀국수 국물이 끝내주는 곳"
        },
        {
            "name": "동탄 리틀노작",
            "category": "양식",
            "region": "동탄",
            "menu_pic": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?q=80&w=400",
            "desc": "파스타 분위기 맛집, 데이트 코스로 강추"
        }
    ]

# 맛집 카드(아이콘) 그리는 함수
def draw_restaurant_card(res):
    with st.container(border=True):
        # 1) 대표 사진
        st.image(res["menu_pic"], use_container_width=True)
        # 2) 음식점 이름
        st.subheader(res["name"])
        # 3) 음식 구별 및 지역 정보 태그
        st.markdown(f"`{res['category']}` `{res['region']}`")
        st.caption(res["desc"])
        # 4) 네이버 지도 연동 링크
        naver_map_url = f"https://map.naver.com/v5/search/{res['name']}"
        st.markdown(f"[🗺️ 네이버 지도 열기]({naver_map_url})")

# --- 메인 레이아웃 ---
st.title("💝 데이트 맛집 보물상자")
st.write("우리만의 맛집 리스트를 비주얼 카드로 관리하고, 재미있게 골라보세요!")
st.write("---")

# --- 사이드바: 1) 맛집 등록하기 ---
with st.sidebar:
    st.header("📌 새 맛집 등록")
    with st.form("add_form", clear_on_submit=True):
        new_name = st.text_input("가게 이름", placeholder="예: 성수 대성갈비")
        new_category = st.selectbox("음식 종류", ["한식", "일식", "양식", "중식", "퓨전/아시안", "디저트/카페"])
        new_region = st.text_input("지역 (동/도시 단위)", placeholder="예: 성수동, 동탄, 홍대")
        new_pic = st.text_input("대표 사진 URL (인터넷 이미지 주소)", placeholder="https://...")
        new_desc = st.text_area("한줄 설명", placeholder="예: 수요미식회 나온 갈비 골목 맛집!")
        
        submit = st.form_submit_button("맛집 상자에 저장")
        if submit:
            if new_name and new_region:
                # 사진 주소가 없으면 기본 음식 이미지 대체
                pic_url = new_pic if new_pic else "https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=400"
                st.session_state.my_restaurants.append({
                    "name": new_name,
                    "category": new_category,
                    "region": new_region.strip(),
                    "menu_pic": pic_url,
                    "desc": new_desc
                })
                st.success(f"'{new_name}' 등록 완료!")
                st.rerun()
            else:
                st.error("가게 이름과 지역은 필수 입력입니다.")

# --- 메인 화면 상단: 5) 시각적 랜덤 추천 (룰렛) ---
st.header("🎲 오늘의 운명 픽! (애니메이션 추천)")
all_regions = list(set([res["region"] for res in st.session_state.my_restaurants]))

roulette_col1, roulette_col2 = st.columns([1, 3])

with roulette_col1:
    selected_roulette_region = st.selectbox("어느 지역에서 고를까요?", all_regions, key="roulette_reg")
    start_roulette = st.button("🔥 돌려돌려 맛집 룰렛! 🔥", use_container_width=True)

with roulette_col2:
    # 룰렛을 돌릴 후보들 필터링
    candidates = [res for res in st.session_state.my_restaurants if res["region"] == selected_roulette_region]
    
    # 룰렛 애니메이션 구역 슬롯 확보
    animation_slot = st.empty()
    
    if start_roulette:
        if len(candidates) > 0:
            # 시각적으로 맛집 아이콘이 빠르게 바뀌는 연출 (총 12번 셔플)
            for i in range(12):
                temp_pick = random.choice(candidates)
                with animation_slot.container():
                    st.markdown("### 🌀 맛집 탐색 중... 🌀")
                    # 돌아가는 모습을 시각적으로 보여주기 위해 카드를 실시간 렌더링
                    draw_restaurant_card(temp_pick)
                time.sleep(0.15 + (i * 0.03)) # 갈수록 조금씩 느려지는 효과
            
            # 최종 확정 결과
            final_pick = random.choice(candidates)
            with animation_slot.container():
                st.balloons()
                st.success(f"🏆 오늘의 데이트 메뉴는 바로 여기!!")
                draw_restaurant_card(final_pick)
        else:
            st.warning("선택한 지역에 등록된 맛집이 없습니다.")
    else:
        st.write("위 버튼을 누르면 맛집 카드가 빙글빙글 돌아가며 무작위로 선택됩니다!")

st.write("---")

# --- 메인 화면 하단: 2) & 4) 지역별 맛집 아이콘 리스트 모아보기 ---
st.header("🗺️ 우리의 맛집 아이콘 보드")

# 지역 선택 필터 (전체 보기도 가능)
filter_region = st.selectbox("지역별로 모아보기", ["전체 보기"] + all_regions)

# 필터링 처리
if filter_region == "전체 보기":
    display_list = st.session_state.my_restaurants
else:
    display_list = [res for res in st.session_state.my_restaurants if res["region"] == filter_region]

# 한 줄에 3개씩 맛집 아이콘(카드) 배치
if display_list:
    cols = st.columns(3)
    for idx, res in enumerate(display_list):
        with cols[idx % 3]:
            draw_restaurant_card(res)
else:
    st.info("등록된 맛집이 없습니다. 왼쪽 사이드바에서 맛집을 추가해 주세요!")
