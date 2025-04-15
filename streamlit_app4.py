import streamlit as st
import os
from PIL import Image

# === CONFIG ===
BASE_DIR = "data"

st.title("🎬 Eye-Tracking Heatmap Viewer")
st.markdown("👁️‍🗨️ ดูการกระจายความสนใจของผู้ชมในแต่ละคลิป (แสดงเป็นรูป snapshot ทุก 1 วินาที)")

# 1. เลือก "เรื่อง"
movies = sorted([f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))])
selected_movie = st.selectbox("เลือกเรื่องหนัง", movies)

# 2. เลือก "คลิป"
clips_path = os.path.join(BASE_DIR, selected_movie)
clips = sorted([f for f in os.listdir(clips_path) if os.path.isdir(os.path.join(clips_path, f))])
selected_clip = st.selectbox("เลือกคลิปในเรื่อง", clips)

# 3. หาไฟล์ภาพในคลิปนั้น
clip_path = os.path.join(clips_path, selected_clip)
image_files = sorted([
    f for f in os.listdir(clip_path)
    if f.lower().endswith((".png", ".jpg")) and f[:2].isdigit()
])

# วินาทีที่มี
seconds_available = [int(f[:2]) for f in image_files if f[:2].isdigit()]
seconds_available = sorted(list(set(seconds_available)))

# 4. แสดงภาพ
show_all = st.checkbox("🖼️ แสดงทั้งหมด 30 ภาพแบบ Grid")

if show_all:
    st.markdown("### 🔳 แสดงภาพทั้งหมด (0s–29s)")
    cols = st.columns(6)
    for sec in range(30):
        filename = f"{sec:02d}.jpg"
        path = os.path.join(clip_path, filename)
        if os.path.exists(path):
            img = Image.open(path)
            with cols[sec % 6]:
                st.image(img, caption=f"{sec}s", use_container_width=True)
else:
    if seconds_available:
        selected_sec = st.slider("⏱️ เลือกวินาที (s)", min_value=min(seconds_available), max_value=max(seconds_available), value=min(seconds_available))
        filename = f"{selected_sec:02d}.jpg"
        img_path = os.path.join(clip_path, filename)
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, caption=f"{selected_sec}s", use_container_width=True)
        else:
            st.warning("❌ ไม่พบไฟล์ภาพ")
    else:
        st.warning("❌ ไม่มีภาพในคลิปนี้")
# === Optional: แสดงภาพเป็น GIF แทน Grid ===

import io
import imageio.v2 as imageio  # รองรับ streamlit ได้ดี

show_gif = st.checkbox("🎞️ แสดงเป็น GIF Animation (0s–29s)")

if show_gif:
    images = []
    for sec in range(30):
        filename = f"{sec:02d}.jpg"
        path = os.path.join(clip_path, filename)
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            images.append(img)

    if images:
        # บันทึกเป็น GIF ลง memory
        gif_bytes = io.BytesIO()
        imageio.mimsave(gif_bytes, images, format="GIF", duration=0.3)
        st.image(gif_bytes.getvalue(), caption="GIF 0s–29s", use_container_width=True)
    else:
        st.warning("⚠️ ไม่พบไฟล์ภาพเพียงพอในการสร้าง GIF")        