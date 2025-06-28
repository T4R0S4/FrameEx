# app.py
import streamlit as st
import cv2
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="Video Frame Extractor", layout="wide")
st.title("🎞️ Video Frame Extractor")

# Upload video
video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if video_file:
    # Save video to a temp file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    timestamps = []

    with st.spinner("Extracting frames..."):
        frame_number = 0
        success, frame = cap.read()
        while success:
            frames.append(frame)
            timestamps.append(frame_number / fps)
            frame_number += 1
            success, frame = cap.read()
        cap.release()

    st.success(f"✅ Loaded {len(frames)} frames")

    # Select frames
    selected = []
    st.subheader("Preview and Select Frames")
    cols = st.columns(4)
    for idx, frame in enumerate(frames):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        with cols[idx % 4]:
            st.image(pil_img, caption=f"Frame {idx}", use_column_width=True)
            if st.checkbox(f"Select Frame {idx}", key=idx):
                selected.append(idx)

    # Save selected
    if selected:
        if st.button("📥 Extract Selected Frames"):
            out_dir = "selected_frames"
            os.makedirs(out_dir, exist_ok=True)
            for idx in selected:
                out_path = os.path.join(out_dir, f"frame_{idx:04d}.png")
                cv2.imwrite(out_path, frames[idx])
            st.success(f"Saved {len(selected)} frames to: `{out_dir}/`")
    else:
        st.warning("Select at least one frame to extract.")
