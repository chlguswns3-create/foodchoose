import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="오늘 뭐 먹지? 데이트 메뉴 추천", page_icon="❤️", layout="centered")

# 데이터베이스 (원하는 메뉴와 맛집 정보를 자유롭게 수정하세요!)
MENU_DATA = {
    "일식/일반": ["초밥", "돈카츠", "라멘", "규동", "사케동", "텐동"],
    "양식/분위기": ["파스타", "화덕피자", "스테이크", "리조또", "라자냐"],
    "한식/깔끔": ["갈비찜", "낙곱새", "보쌈/족발", "샤브샤브", "석갈비"],
    "아시안/이색": ["쌀국수", "팟타이", "마라탕", "딤섬", "타코/멕시칸"],
    "가벼운 음식": ["브런치", "샐러드 보울", "샌드위치", "포케"]
}

# 모든 메뉴 평탄화 list
ALL_MENUS = [menu for sublist in MENU_DATA.values() for menu in sublist]

# 세션 상태 초기화 (월드컵용)
if "worldcup_round" not in st.session_state:
    st.session_state.worldcup_round = 0
    st.session_state.candidates = []
    st.session_state.winners = []

# --- UI 레이아웃 ---
st.title("❤️ 데이트 메뉴 구출 작전!")
st.subheader("오늘 여자친구랑 뭐 먹을지 딱 정해드립니다.")
st.write("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["🎲 랜덤 룰렛", "📂 카테고리 픽", "🏆 메뉴 월드컵"])

# --- TAB 1: 랜덤 룰렛 ---
with tab1:
    st.header("고민하기 귀찮을 땐?")
    if st.button("✨ 아무거나 하나만 골라줘! ✨", key="random_btn"):
        with st.spinner("오늘의 운명적인 메뉴는..."):
            time.sleep(1) # 감성을 위한 1초 대기
            picked = random.choice(ALL_MENUS)
            st.balloons()
            st.success(f"🎉 오늘 데이트 추천 메뉴는 **[{picked}]** 입니다! 맛있게 드세요!")

# --- TAB 2: 카테고리 픽 ---
with tab2:
    st.header("오늘 땡기는 장르가 있다면?")
    category = st.selectbox("어떤 스타일이 좋으세요?", list(MENU_DATA.keys()))
    
    if category:
        st.write(f"**{category}** 추천 리스트:")
        cols = st.columns(3)
        for idx, menu in enumerate(MENU_DATA[category]):
            with cols[idx % 3]:
                st.info(f"📍 {menu}")

# --- TAB 3: 메뉴 월드컵 (간이 버전) ---
with tab3:
    st.header("🆚 둘 다 좋은데? 메뉴 월드컵")
    st.write("진짜 안 골라질 때는 토너먼트로 가보시죠!")
    
    if st.button("월드컵 시작하기/재설정"):
        # 랜덤하게 4개 메뉴 뽑아서 시작
        st.session_state.candidates = random.sample(ALL_MENUS, 4)
        st.session_state.winners = []
        st.session_state.worldcup_round = 1

    if st.session_state.worldcup_round == 1:
        st.write("### 4강전: 다음 중 더 끌리는 것은?")
        cands = st.session_state.candidates
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👉 {cands[0]}", key="wc1"):
                st.session_state.winners.append(cands[0])
                st.session_state.worldcup_round = 2
                st.rerun()
        with col2:
            if st.button(f"👉 {cands[1]}", key="wc2"):
                st.session_state.winners.append(cands[1])
                st.session_state.worldcup_round = 2
                st.rerun()
                
    elif st.session_state.worldcup_round == 2:
        st.write("### 4강전 두 번째 판!")
        cands = st.session_state.candidates
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👉 {cands[2]}", key="wc3"):
                st.session_state.winners.append(cands[2])
                st.session_state.worldcup_round = 3
                st.rerun()
        with col2:
            if st.button(f"👉 {cands[3]}", key="wc4"):
                st.session_state.winners.append(cands[3])
                st.session_state.worldcup_round = 3
                st.rerun()

    elif st.session_state.worldcup_round == 3:
        st.write("### 🏆 대망의 결승전! 🏆")
        winners = st.session_state.winners
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🥇 {winners[0]}", key="wc_f1"):
                st.session_state.worldcup_round = 4
                st.session_state.final_winner = winners[0]
                st.rerun()
        with col2:
            if st.button(f"🥇 {winners[1]}", key="wc_f2"):
                st.session_state.worldcup_round = 4
                st.session_state.final_winner = winners[1]
                st.rerun()

    elif st.session_state.worldcup_round == 4:
        st.snow()
        st.success(f"💖 치열한 접전 끝에 결정된 오늘 메뉴는 **[{st.session_state.final_winner}]** 입니다!!")
        if st.button("다시 하기"):
            st.session_state.worldcup_round = 0
            st.rerun()
