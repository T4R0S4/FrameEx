# app.py
import streamlit as st
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import tempfile

st.set_page_config(page_title="Video Frame Extractor", layout="wide")
st.title("🎞️ Video Frame Extractor (No OpenCV)")

video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    clip = VideoFileClip(tfile.name)
    duration = int(clip.duration)
    st.success(f"Video duration: {duration} seconds")

    selected_times = []
    cols = st.columns(4)

    st.subheader("Select timestamps (seconds):")
    for i in range(0, duration, 2):  # Set interval
        frame = clip.get_frame(i)
        img = Image.fromarray(frame)
        with cols[i % 4]:
            st.image(img, caption=f"{i}s", use_column_width=True)
            if st.checkbox(f"Select {i}s", key=i):
                selected_times.append(i)

    if selected_times:
        if st.button("📥 Extract Selected Frames"):
            out_dir = "selected_frames"
            os.makedirs(out_dir, exist_ok=True)
            for sec in selected_times:
                img = Image.fromarray(clip.get_frame(sec))
                img.save(os.path.join(out_dir, f"frame_{sec:03d}.png"))
            st.success(f"Saved {len(selected_times)} frames to `{out_dir}/`")
