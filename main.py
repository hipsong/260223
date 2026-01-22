import streamlit as st
import os
import json
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
# 기본 CSS (최소)
# =====================
st.markdown("""
<style>
.block-container { padding: 1rem; }
.card {
    background: #ffffff;
    padding: 14px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.time {
    font-size: 11px;
    color: #888;
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
    name = st.text_input("이름 (댓글/업로드용)")

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

data = load_data()
data = sorted(data, key=lambda x: x["time"], reverse=True)

# =====================
# 헤더
# =====================
st.title("👶 깜짝이 추억 앨범 💖")
st.caption("사진과 댓글이 시간순으로 쌓여요 ⏳")

# =====================
# 사진 업로드
# =====================
st.subheader("📸 사진 올리기")

desc = st.text_input("사진 한마디")
photo = st.file_uploader("사진 선택", type=["jpg", "png", "jpeg"])

if st.button("업로드 ✨"):
    if photo:
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
        st.success("업로드 완료 💕")
        st.rerun()
    else:
        st.warning("사진을 선택해 주세요")

st.divider()

# =====================
# 갤러리 (for문 하나!)
# =====================
st.subheader("🕒 사진 타임라인")

if not data:
    st.info("아직 사진이 없어요 😊")

for idx, item in enumerate(data):
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.image(
        os.path.join(PHOTO_DIR, item["file"]),
        use_container_width=True
    )

    st.markdown(f"**👤 {item['uploader']}**")
    st.markdown(
        f"<div class='time'>📅 {item['time']}</div>",
        unsafe_allow_html=True
    )

    # 설명
    if user == item["uploader"]:
        new_desc = st.text_input(
            "✏️ 설명 수정",
            value=item["desc"],
            key=f"desc_{idx}"
        )
        if st.button("저장", key=f"save_{idx}"):
            item["desc"] = new_desc
            save_data(data)
            st.rerun()
    else:
        st.write(f"📝 {item['desc']}")

    # 댓글
    st.markdown("💬 댓글")
    for c in item["comments"]:
        st.write(f"- {c['text']} ({c['time']})")

    comment = st.text_input("댓글 쓰기", key=f"cmt_{idx}")
    if st.button("댓글 추가", key=f"addc_{idx}"):
        if comment:
            item["comments"].append({
                "text": f"{user}: {comment}",
                "time": datetime.now(KST).strftime("%Y-%m-%d %H:%M")
            })
            save_data(data)
            st.rerun()

    # =====================
    # 삭제 (업로더만 / 확인 포함)
    # =====================
    if user == item["uploader"]:
        confirm_key = f"confirm_{idx}"

        if st.button("🗑️ 사진 삭제", key=f"del_{idx}"):
            st.session_state[confirm_key] = True

        if st.session_state.get(confirm_key, False):
            st.warning("정말 삭제하시겠습니까?")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("취소", key=f"cancel_{idx}"):
                    st.session_state[confirm_key] = False
            with col2:
                if st.button("삭제", key=f"confirm_del_{idx}"):
                    os.remove(os.path.join(PHOTO_DIR, item["file"]))
                    data.pop(idx)
                    save_data(data)
                    st.session_state.pop(confirm_key, None)
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)





