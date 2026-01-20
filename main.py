import streamlit as st
from PIL import Image
import os
from datetime import datetime

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="👶 우리 아기 추억 앨범",
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
    <h1 style='text-align: center;'>👶🍼 우리 아기 추억 앨범 💕</h1>
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
        img = Image.open(os.path.join(SAVE_DIR, file))

        memo_file = os.path.join(SAVE_DIR, file + ".txt")
        memo_text = ""
        if os.path.exists(memo_file):
            with open(memo_file, "r", encoding="utf-8") as f:
                memo_text = f.read()

        with cols[idx % 3]:
            st.image(img, use_container_width=True)
            if memo_text:
                st.caption("📝 " + memo_text)
