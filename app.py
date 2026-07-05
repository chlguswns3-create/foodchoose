import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="재미 가득! 데이트 메뉴 결정기", page_icon="🎲", layout="centered")

# 데이터베이스 (기본 메뉴 구성)
NORMAL_MENUS = [
    "초밥", "돈카츠", "라멘", "파스타", "화덕피자", "스테이크", 
    "갈비찜", "낙곱새", "샤브샤브", "쌀국수", "타코", "브런치"
]

# 영수증 챌린지용 (메뉴별 대략적인 2인 기준 예상 가격)
MENU_PRICES = {
    "파스타 & 피자 세트": 38000,
    "커플 초밥 세트": 42000,
    "돈카츠 2인 정식": 28000,
    "뜨끈한 샤브샤브": 35000,
    "즉석 떡볶이 & 튀김": 18000,
    "쌀국수 & 짜조": 26000,
    "스테이크 썰기": 75000,
    "수제버거 & 감튀": 24000,
    "분위기 좋은 브런치": 32000,
    "치킨 & 맥주(음료)": 26000,
    "고급 참치회": 80000,
    "마라탕 & 꿔바로우": 30000
}

st.title("🎲 오늘 저녁은 게임으로 정한다!")
st.subheader("여자친구와 함께 고르는 복불복 데이트 메뉴")
st.write("---")

# 4가지 새로운 탭 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "🎲 랜덤 룰렛", 
    "💣 러시안룰렛", 
    "🧭 내비게이션 룰렛", 
    "💰 예산 챌린지"
])

# --- TAB 1: 랜덤 룰렛 ---
with tab1:
    st.header("🎲 평범하고 무난한 랜덤 픽")
    st.write("가장 안전하고 호불호 없는 메뉴 중 하나를 무작위로 골라줍니다.")
    
    if st.button("✨ 운명의 메뉴 뽑기 ✨", key="btn_tab1"):
        with st.spinner("맛있는 메뉴 고르는 중..."):
            time.sleep(0.8)
            picked = random.choice(NORMAL_MENUS)
            st.balloons()
            st.success(f"🎉 오늘 데이트 추천 메뉴는 **[{picked}]** 입니다!")

# --- TAB 2: 메뉴판 러시안룰렛 ---
with tab2:
    st.header("💣 메뉴판 러시안룰렛")
    st.write("무난한 음식들 사이에 **장난스러운 폭탄 메뉴**가 딱 하나 섞여 있습니다. 걸리면 진짜 먹기?!")
    
    # 폭탄 메뉴 정의
    bomb_menus = ["민트초코 피자", "취청오이 샌드위치", "불닭발에 주먹밥 (땀 한바가지)", "군대식 군대리아", "편의점 꿀조합 정식"]
    
    if st.button("🔫 방아쇠 당기기 (룰렛 돌리기)", key="btn_tab2"):
        with st.spinner("철컥철컥... 과연 결과는?"):
            time.sleep(1.2)
            
            # 20% 확률로 폭탄 메뉴 당첨, 80% 확률로 정상 메뉴
            if random.random() < 0.2:
                bomb_picked = random.choice(bomb_menus)
                st.error(f"💥 크악!! 폭탄에 당첨되었습니다!! 오늘의 메뉴는 **[{bomb_picked}]** 입니다! (약속은 약속!)")
            else:
                safe_picked = random.choice(NORMAL_MENUS)
                st.success(f"😮 휴~ 안전합니다! 맛있는 **[{safe_picked}]** 당첨!")

# --- TAB 3: 내비게이션 반경 룰렛 ---
with tab3:
    st.header("🧭 내비게이션 반경 룰렛")
    st.write("지금 계신 곳에서 스마트폰을 들고 이 지시대로 걸어가 보세요! 완전히 새로운 맛집을 찾을지도?")
    
    directions = ["직진", "좌회전", "우회전", "뒤로 돌아 가기"]
    steps = ["첫 번째 골목", "두 번째 골목", "30걸음 직진 후 보이는 첫 가게", "눈에 띄는 화려한 간판의 가게"]
    
    if st.button("🗺️ 미션 생성하기", key="btn_tab3"):
        with st.spinner("운명의 나침반을 돌리는 중..."):
            time.sleep(0.8)
            d = random.choice(directions)
            s = random.choice(steps)
            
            st.info("🎯 **오늘의 이동 미션:**")
            st.subheader(f"📍 지금 위치에서 [{d}] 한 뒤, [{s}]로 무조건 들어가기!")
            st.caption("주의: 카페나 편의점이 나오면 그 옆집으로 가기!")

# --- TAB 4: 영수증 예산 챌린지 ---
with tab4:
    st.header("💰 영수증 예산 챌린지")
    st.write("오늘 저녁 데이트 지출 제한선을 정해주세요! 가격 조건에 딱 맞는 2인 기준 메뉴를 매칭해 드립니다.")
    
    # 예산 입력 (슬라이더)
    budget = st.slider("오늘의 저녁 예산 한도는? (2인 기준)", min_value=20000, max_value=100000, value=40000, step=5000)
    
    if st.button("💵 예산 맞춤 메뉴 찾기", key="btn_tab4"):
        # 입력한 예산 이하의 메뉴들만 필터링
        affordable_menus = [menu for menu, price in MENU_PRICES.items() if price <= budget]
        
        if affordable_menus:
            picked_menu = random.choice(affordable_menus)
            picked_price = MENU_PRICES[picked_menu]
            
            st.snow()
            st.success(f"💳 영수증 통과! 예산 범위 안에서 즐기는 추천 메뉴:")
            st.subheader(f"🍽️ {picked_menu}")
            st.write(f"💵 예상 가격: 약 {picked_price:,}원 (지정하신 {budget:,}원 이하!)")
        else:
            st.warning("⚠️ 앗! 설정하신 예산이 너무 낮아 선택할 수 있는 메뉴가 없습니다. 예산을 조금만 더 올려주세요! 🥹")
