import streamlit as st
import os
import json
from datetime import datetime

# =====================
# 기본 설정
# =====================
st.set_page_config(
    page_title="👶 깜짝이 앨범",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PASSWORD = "0223"
DATA_FILE = "data.json"
PHOTO_DIR = "photos"

os.makedirs(PHOTO_DIR, exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# =====================
# CSS (모바일 최적화)
# =====================
st.markdown("""
<style>
/* 모바일 여백 제거 */
.block-container {
    padding: 1rem 0.8rem;
}

/* 카드 느낌 */
.photo-card {
    background: white;
    padding: 12px;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 18px;
}

/* 버튼 작게 */
.small-btn button {
    padding: 4px 10px;
    font-size: 12px;
    border-radius: 8px;
}

/* 설명 글씨 */
.desc {
    font-size: 14px;
}

/* 타임라인 */
.time {
    font-size: 11px;
    color: #888;
}
</style>
""", unsafe_allow_html=True)

# =====================
# 로그인
# =====================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 우리 가족 전용 공간")
    pw = st.text_input("암호를 입력하세요", type="password")
    if st.button("입장하기 💕"):
        if pw == PASSWORD:
            st.session_state.auth = True
            st.experimental_rerun()
        else:
            st.error("암호가 틀렸어요 😢")
    st.stop()

# =====================
# 데이터
# =====================
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

data = load_data()

# 최신순 정렬
data = sorted(data, key=lambda x: x["time"], reverse=True)

# =====================
# 헤더
# =====================
st.title("👶 깜짝이의 추억 앨범 💖")
st.caption("사진 하나하나가 타임라인으로 쌓여요 ⏳")

# =====================
# 업로드
# =====================
st.subheader("📸 사진 올리기")

name = st.text_input("🙋 이름")
desc = st.text_input("📝 사진 한마디")
photo = st.file_uploader("사진 선택", type=["jpg", "png", "jpeg"])

if st.button("업로드 ✨"):
    if name and photo:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.name}"
        path = os.path.join(PHOTO_DIR, filename)

        with open(path, "wb") as f:
            f.write(photo.getbuffer())

        data.append({
            "file": filename,
            "uploader": name,
            "desc": desc,
            "time": now,
            "comments": []
        })
        save_data(data)
        st.success("업로드 완료 💕")
        st.experimental_rerun()
    else:
        st.warning("이름과 사진은 꼭 필요해요!")

st.divider()

# =====================
# 갤러리 (모바일 친화)
# =====================
st.subheader("🕒 사진 타임라인")

for idx, item in enumerate(data):
    st.markdown('<div class="photo-card">', unsafe_allow_html=True)

    st.image(os.path.join(PHOTO_DIR, item["file"]), use_column_width=True)

    st.markdown(f"**👤 {item['uploader']}**")
    st.markdown(f"<div class='time'>📅 {item['time']}</div>", unsafe_allow_html=True)

    # 설명
    if name == item["uploader"]:
        new_desc = st.text_input(
            "✏️ 설명 수정",
            value=item["desc"],
            key=f"desc_{idx}"
        )
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if st.button("저장", key=f"save_{idx}"):
            item["desc"] = new_desc
            save_data(data)
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='desc'>📝 {item['desc']}</div>", unsafe_allow_html=True)

    # 댓글
    st.markdown("💬 댓글")
    for c in item["comments"]:
        st.markdown(f"- {c['text']}  <span class='time'>({c['time']})</span>", unsafe_allow_html=True)

    comment = st.text_input("댓글 남기기", key=f"cmt_{idx}")
    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button("댓글 추가", key=f"addc_{idx}"):
        if comment:
            item["comments"].append({
                "text": f"{name}: {comment}",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_data(data)
            st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 삭제
    if name == item["uploader"]:
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if st.button("🗑️ 사진 삭제", key=f"del_{idx}"):
            os.remove(os.path.join(PHOTO_DIR, item["file"]))
            data.pop(idx)
            save_data(data)
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)



