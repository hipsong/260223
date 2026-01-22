import streamlit as st
from PIL import Image
import os
from datetime import datetime

# ===========================
# ⚙️ 페이지 설정 (맨 위)
# ===========================
st.set_page_config(
    page_title="👶 깜짝이 추억 앨범",
    page_icon="🍼",
    layout="centered"
)

# ===========================
# 🔐 가족 암호
# ===========================
APP_PASSWORD = "1234"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.markdown("## 🔐 👨‍👩‍👦 깜짝이 가족 앨범 입장 💕")
    password = st.text_input("암호를 입력하세요 🗝️", type="password")

    if st.button("🚪 입장하기"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.success("💖 환영해요!")
            st.rerun()
        else:
            st.error("❌ 암호가 틀렸어요")

if not st.session_state.authenticated:
    login()
    st.stop()

# ===========================
# 📁 저장 폴더
# ===========================
SAVE_DIR = "baby_photos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ===========================
# 🎀 제목
# ===========================
st.markdown(
    """
    <h1 style='text-align: center;'>👶🍼 깜짝이 추억 앨범 💕</h1>
    <p style='text-align: center; font-size:18px;'>
    가족의 사랑이 기록되는 공간 💖
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ===========================
# 📸 사진 업로드
# ===========================
st.subheader("📸 사진 올리기")

uploaded_file = st.file_uploader(
    "아기 사진을 선택해 주세요 💖",
    type=["jpg", "jpeg", "png"]
)

memo = st.text_input("📝 오늘의 문구 (선택)", placeholder="예: 처음 웃은 날 😍")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("💾 추억 저장하기"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        filepath = os.path.join(SAVE_DIR, filename)

        image.save(filepath)

        if memo:
            with open(filepath + ".txt", "w", encoding="utf-8") as f:
                f.write(memo)

        st.success("🎉 저장 완료!")

st.divider()

# ===========================
# 🧸 갤러리 + 문구 수정
# ===========================
st.subheader("🧸 아기 사진 갤러리")

files = sorted(
    [f for f in os.listdir(SAVE_DIR) if f.lower().endswith(("jpg", "jpeg", "png"))],
    reverse=True
)

if not files:
    st.info("아직 사진이 없어요 🥺")
else:
    cols = st.columns(2)

    for idx, file in enumerate(files):
        img_path = os.path.join(SAVE_DIR, file)
        memo_path = img_path + ".txt"

        with cols[idx % 2]:
            st.image(Image.open(img_path), use_container_width=True)

            # 기존 문구 읽기
            current_memo = ""
            if os.path.exists(memo_path):
                with open(memo_path, "r", encoding="utf-8") as f:
                    current_memo = f.read()

            # 문구 수정 입력창
            new_memo = st.text_area(
                "📝 사진 문구",
                value=current_memo,
                key=f"memo_edit_{file}"
            )

            if st.button("✏️ 문구 수정 저장", key=f"save_memo_{file}"):
                if new_memo.strip():
                    with open(memo_path, "w", encoding="utf-8") as f:
                        f.write(new_memo)
                    st.success("💖 문구가 수정됐어요")
                else:
                    if os.path.exists(memo_path):
                        os.remove(memo_path)
                    st.info("문구가 삭제되었어요")

            # 사진 삭제
            if st.button("🗑️ 사진 삭제", key=f"del_{file}"):
                os.remove(img_path)
                if os.path.exists(memo_path):
                    os.remove(memo_path)
                st.rerun()

# ===========================
# 🌈 몽글몽글 배경
# ===========================
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
