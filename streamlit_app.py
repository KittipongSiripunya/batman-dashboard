import streamlit as st
import os
from PIL import Image

# --- ตั้ง path หลัก ---
BASE_DIR = "/Users/ronacsexks/Desktop/info visual/batman_dashboard"

# --- หัวเรื่อง ---
st.title("Batman Eye-Tracking Snapshots")
st.markdown("👁️ ดูการกระจายความสนใจของผู้ชมในแต่ละคลิป (แสดงเป็นรูป snapshot ทุก 5 วินาที)")

# --- รายชื่อโฟลเดอร์คลิป ---
clips = sorted([f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))])

# --- เลือกคลิป ---
selected_clip = st.selectbox("เลือกคลิป", clips)

# --- แสดงรูปในคลิปที่เลือก ---
clip_path = os.path.join(BASE_DIR, selected_clip)
image_files = sorted([f for f in os.listdir(clip_path) if f.endswith(".png")])

# --- Toggle แบบ grid หรือ dropdown ---
view_mode = st.radio("โหมดการแสดงผล", ["📜 เรียงตามเวลา", "🎞️ ทีละรูป (dropdown)"])

if view_mode == "📜 เรียงตามเวลา":
    for img_file in image_files:
        st.image(os.path.join(clip_path, img_file), caption=img_file, use_column_width=True)
else:
    selected_img = st.selectbox("เลือกรูปเวลา", image_files)
    st.image(os.path.join(clip_path, selected_img), caption=selected_img, use_column_width=True)