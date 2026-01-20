import streamlit as st
from PIL import Image
import os
from datetime import datetime
import streamlit as st

APP_PASSWORD = "1234"  # 👈 가족 암호

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.markdown("## 🔐 깜짝이 가족 앨범 👶💕")
    password = st.text_input(
        "암호를 입력하세요 🗝️",
        type="password"
    )

    if st.button("👨‍👩‍👦 입장하기"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.success("💖 환영해요, 가족 여러분!")
            st.rerun()
        else:
            st.error("❌ 암호가 틀렸어요")

if not st.session_state.authenticated:
    login()
    st.stop()  # ⛔ 여기서 앱 전체 중단

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="👶 깜짝이 추억 앨범",
    page_icon="🍼",
    layout="centered"
)

SAVE_DIR = "baby_photos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------------------
# 제목
# ---------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>👶🍼 깜짝이 추억 앨범 💕</h1>
    <p style='text-align: center; font-size:18px;'>
    아빠가 사랑으로 만든 사진 보관함 📸✨
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------------------
# 사진 업로드
# ---------------------------
st.subheader("📸 사진 올리기")
uploaded_file = st.file_uploader(
    "아기 사진을 선택해 주세요 💖",
    type=["jpg", "jpeg", "png"]
)

memo = st.text_input("📝 오늘의 한마디 (선택)", placeholder="예: 처음 웃은 날 😍")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="💗 업로드된 사진", use_container_width=True)

    if st.button("💾 추억 저장하기"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        filepath = os.path.join(SAVE_DIR, filename)

        image.save(filepath)

        if memo:
            with open(filepath + ".txt", "w", encoding="utf-8") as f:
                f.write(memo)

        st.success("🎉 저장 완료! 소중한 추억이 하나 더 생겼어요 💕")

st.divider()

# ---------------------------
# 갤러리
# ---------------------------


st.subheader("🧸 아기 사진 갤러리")

files = sorted(
    [f for f in os.listdir(SAVE_DIR) if f.lower().endswith(("png", "jpg", "jpeg"))],
    reverse=True
)

if not files:
    st.info("아직 사진이 없어요 🥺 첫 추억을 남겨보세요!")
else:
    cols = st.columns(3)

    for idx, file in enumerate(files):
        img_path = os.path.join(SAVE_DIR, file)
        memo_path = img_path + ".txt"

        with cols[idx % 3]:
            img = Image.open(img_path)
            st.image(img, use_container_width=True)

            # 메모 표시
            if os.path.exists(memo_path):
                with open(memo_path, "r", encoding="utf-8") as f:
                    st.caption("📝 " + f.read())

            # 삭제 버튼
            delete_key = f"delete_{file}"
            confirm_key = f"confirm_{file}"

            if st.button("🗑️ 삭제", key=delete_key):
                st.session_state[confirm_key] = True

            # 삭제 확인
            if st.session_state.get(confirm_key):
                st.warning("⚠️ 정말 삭제할까요? (되돌릴 수 없어요 🥺)")
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("❌ 취소", key=f"cancel_{file}"):
                        st.session_state[confirm_key] = False

                with col2:
                    if st.button("✅ 삭제할래요", key=f"yes_{file}"):
                        os.remove(img_path)
                        if os.path.exists(memo_path):
                            os.remove(memo_path)

                        st.success("🧹 추억이 삭제되었어요")
                        st.session_state.pop(confirm_key, None)
                        st.rerun()
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            180deg,
            #FFF1F8 0%,
            #E8F6FF 50%,
            #FFFFFF 100%
        );
    }
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit as st

st.title("👶 아기 앨범 테스트 🎶")


