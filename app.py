import streamlit as st
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import tempfile

st.set_page_config(page_title="🎞️ Video Frame Extractor", layout="wide")
st.title("🎞️ Video Frame Extractor (No OpenCV)")

video_file = st.file_uploader("📂 Upload a video", type=["mp4", "mov", "avi"])

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(video_file.read())
    tfile.flush()

    try:
        clip = VideoFileClip(tfile.name)
        fps = clip.fps
        duration = clip.duration
        total_frames = int(fps * duration)
        st.success(f"Video loaded. Duration: {duration:.2f}s | FPS: {fps:.2f} | Total Frames: {total_frames}")

        st.subheader("🎞️ Select Frames to Extract")

        selected_frames = []
        cols = st.columns(6)  # Grid: 6 thumbnails per row

        for i in range(total_frames):
            frame_time = i / fps
            frame = clip.get_frame(frame_time)
            img = Image.fromarray(frame)

            with cols[i % 6]:
                st.image(img, caption=f"Frame {i}", use_container_width=True)
                if st.checkbox(f"Select {i}", key=f"frame_{i}"):
                    selected_frames.append((i, img))

        if selected_frames:
            if st.button("📥 Extract Selected Frames"):
                output_dir = "selected_frames"
                os.makedirs(output_dir, exist_ok=True)
                for idx, img in selected_frames:
                    filename = os.path.join(output_dir, f"frame_{idx:04d}.png")
                    img.save(filename)
                st.success(f"✅ Saved {len(selected_frames)} frames to `{output_dir}/`")
    finally:
        clip.close()
        os.unlink(tfile.name)
