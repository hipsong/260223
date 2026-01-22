import streamlit as st
from PIL import Image
import os
from datetime import datetime

# ===========================
# ⚙️ 페이지 설정 (반드시 맨 위)
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

# ===========================
# 🔐 로그인 (이름 + 암호)
# ===========================
def login():
    st.markdown("## 🔐 👨‍👩‍👦 깜짝이 가족 앨범 입장 💕")

    user_name = st.text_input("이름을 입력하세요 👤", placeholder="예: 아빠")
    password = st.text_input("암호를 입력하세요 🗝️", type="password")

    if st.button("🚪 입장하기"):
        if user_name and password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.user_name = user_name
            st.success(f"💖 환영해요, {user_name}님!")
            st.rerun()
        else:
            st.error("❌ 이름 또는 암호가 틀렸어요")

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
    가족의 사랑으로 기록하는 깜짝이의 하루 💖
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

memo = st.text_input(
    "📝 사진 문구 (선택)",
    placeholder="예: 오늘 처음 웃은 날 😍"
)

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

        with open(filepath + ".author", "w", encoding="utf-8") as f:
            f.write(st.session_state.user_name)

        st.success("🎉 저장 완료! 추억이 추가됐어요 💕")

st.divider()

# ===========================
# 🧸 갤러리
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
        author_path = img_path + ".author"
        comment_path = img_path + "_comments.txt"

        with cols[idx % 2]:
            st.image(Image.open(img_path), use_container_width=True)

            # 작성자
            author = "알 수 없음"
            if os.path.exists(author_path):
                with open(author_path, "r", encoding="utf-8") as f:
                    author = f.read().strip()

            st.caption(f"✍️ 업로드: {author}")

            # 문구
            current_memo = ""
            if os.path.exists(memo_path):
                with open(memo_path, "r", encoding="utf-8") as f:
                    current_memo = f.read()

            if author == st.session_state.user_name:
                new_memo = st.text_area(
                    "📝 사진 문구",
                    value=current_memo,
                    key=f"memo_{file}"
                )

                if st.button("✏️ 문구 저장", key=f"save_{file}"):
                    if new_memo.strip():
                        with open(memo_path, "w", encoding="utf-8") as f:
                            f.write(new_memo)
                        st.success("문구가 수정됐어요 💖")
                    else:
                        if os.path.exists(memo_path):
                            os.remove(memo_path)
                        st.info("문구가 삭제됐어요")
            else:
                if current_memo:
                    st.caption("📝 " + current_memo)
                st.caption("🔒 작성자만 수정 가능")

            st.markdown("---")

            # ===========================
            # 🗑️ 사진 삭제 (작성자만 + 확인)
            # ===========================
            if author == st.session_state.user_name:
                delete_key = f"delete_{file}"
                confirm_key = f"confirm_{file}"

                if st.button("🗑️ 사진 삭제", key=delete_key):
                    st.session_state[confirm_key] = True

                if st.session_state.get(confirm_key):
                    st.warning("⚠️ 정말 삭제할까요? (되돌릴 수 없어요)")
                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button("❌ 취소", key=f"cancel_{file}"):
                            st.session_state[confirm_key] = False

                    with c2:
                        if st.button("✅ 삭제", key=f"yes_{file}"):
                            os.remove(img_path)
                            if os.path.exists(memo_path):
                                os.remove(memo_path)
                            if os.path.exists(author_path):
                                os.remove(author_path)
                            if os.path.exists(comment_path):
                                os.remove(comment_path)

                            st.session_state.pop(confirm_key, None)
                            st.success("🧹 사진이 삭제됐어요")
                            st.rerun()

            # ===========================
            # 💬 댓글
            # ===========================
            st.markdown("💬 **가족 댓글**")

            if os.path.exists(comment_path):
                with open(comment_path, "r", encoding="utf-8") as f:
                    comments = f.readlines()
                for c in comments:
                    st.markdown(f"- {c.strip()}")
            else:
                st.caption("아직 댓글이 없어요 😊")

            comment = st.text_input(
                "댓글 남기기 💖",
                key=f"comment_{file}",
                placeholder="너무 귀여워요 😍"
            )

            if st.button("💌 댓글 등록", key=f"add_comment_{file}"):
                if comment.strip():
                    with open(comment_path, "a", encoding="utf-8") as f:
                        f.write(f"{st.session_state.user_name}: {comment}\n")
                    st.success("댓글이 추가됐어요 💕")
                    st.rerun()
                else:
                    st.warning("댓글을 입력해 주세요")

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


