import streamlit as st
import os, json
from datetime import datetime, timezone, timedelta

# =====================
# 시간대 (대한민국)
# =====================
KST = timezone(timedelta(hours=9))

# =====================
# 페이지 설정
# =====================
st.set_page_config(
    page_title="👶 깜짝이 앨범",
    page_icon="🍼",
    layout="centered"
)

st.write("")
st.write("")

PASSWORD = "0223"
DATA_FILE = "data.json"
PHOTO_DIR = "photos"

os.makedirs(PHOTO_DIR, exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# =====================
# 🎨 UI CSS (요즘 감성)
# =====================
st.markdown("""
<style>
.stApp {
    background-color: #f5f6f8;
    font-family: -apple-system, BlinkMacSystemFont, "Pretendard",
                 "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.block-container {
    padding: 1rem;
}

.post-card {
    background: #ffffff;
    padding: 16px;
    border-radius: 20px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
    margin-bottom: 24px;
}

.header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.uploader {
    font-weight: 600;
    font-size: 15px;
}

.time {
    font-size: 12px;
    color: #888;
}

.desc {
    font-size: 15px;
    margin-top: 6px;
}

.comment {
    font-size: 14px;
    margin-top: 6px;
    color: #444;
}

.delete-text {
    color: #ff4d4f;
    font-size: 13px;
    background: none;
    border: none;
    padding: 0;
}

.confirm-box {
    margin-top: 8px;
    font-size: 14px;
    color: #d33;
}
</style>
""", unsafe_allow_html=True)

# =====================
# 로그인
# =====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.authenticated:
    st.title("🔐 우리 가족만 들어와요")

    pw = st.text_input("암호", type="password")
    name = st.text_input("이름")

    if st.button("입장 💕"):
        if pw == PASSWORD and name:
            st.session_state.authenticated = True
            st.session_state.user_name = name
            st.rerun()
        else:
            st.error("암호 또는 이름을 확인해 주세요")

    st.stop()

user = st.session_state.user_name

# =====================
# 데이터 함수
# =====================
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

data = sorted(load_data(), key=lambda x: x["time"], reverse=True)

# =====================
# 헤더
# =====================
st.title("👶 깜짝이 추억 앨범 💖")
st.caption("시간이 지나면 더 소중해질 기록들")

# =====================
# 업로드
# =====================
with st.expander("📸 사진 올리기"):
    desc = st.text_input("사진 한마디")
    photo = st.file_uploader("사진 선택", type=["jpg","png","jpeg"])

    if st.button("업로드 ✨") and photo:
        now = datetime.now(KST)
        filename = f"{now.strftime('%Y%m%d%H%M%S')}_{photo.name}"

        with open(os.path.join(PHOTO_DIR, filename), "wb") as f:
            f.write(photo.getbuffer())

        data.append({
            "file": filename,
            "uploader": user,
            "desc": desc,
            "time": now.strftime("%Y-%m-%d %H:%M"),
            "comments": []
        })

        save_data(data)
        st.rerun()

st.divider()

# =====================
# 🕒 타임라인 (for문 1개)
# =====================
for idx, item in enumerate(data):
    st.markdown("<div class='post-card'>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='header-row'>
            <div class='uploader'>👤 {item['uploader']}</div>
            <div class='time'>📅 {item['time']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(os.path.join(PHOTO_DIR, item["file"]), use_container_width=True)

    # 설명
    if user == item["uploader"]:
        new_desc = st.text_input(
            "설명",
            value=item["desc"],
            key=f"desc_{idx}"
        )
        if st.button("저장", key=f"save_{idx}"):
            item["desc"] = new_desc
            save_data(data)
            st.rerun()
    else:
        st.markdown(f"<div class='desc'>📝 {item['desc']}</div>",
                    unsafe_allow_html=True)

    # 댓글
    for c in item["comments"]:
        st.markdown(
            f"<div class='comment'>💬 {c['text']} <span class='time'>({c['time']})</span></div>",
            unsafe_allow_html=True
        )

    comment = st.text_input("댓글 쓰기", key=f"cmt_{idx}")
    if st.button("댓글 추가", key=f"addc_{idx}") and comment:
        item["comments"].append({
            "text": f"{user}: {comment}",
            "time": datetime.now(KST).strftime("%Y-%m-%d %H:%M")
        })
        save_data(data)
        st.rerun()

    # ---------------- 삭제 (SNS 스타일)
    if user == item["uploader"]:
        confirm_key = f"confirm_{idx}"

        if st.button("🗑️ 삭제", key=f"del_{idx}", help="사진 삭제"):
            st.session_state[confirm_key] = True

        if st.session_state.get(confirm_key):
            st.markdown("<div class='confirm-box'>이 사진을 삭제할까요?</div>",
                        unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("취소", key=f"cancel_{idx}"):
                    st.session_state[confirm_key] = False
            with col2:
                if st.button("삭제", key=f"confirm_del_{idx}"):
                    os.remove(os.path.join(PHOTO_DIR, item["file"]))
                    data.pop(idx)
                    save_data(data)
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)




