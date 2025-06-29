import streamlit as st
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import tempfile
import shutil
import zipfile
import base64

st.set_page_config(page_title="🎞️ Video Frame Extractor", layout="wide")
st.title("🎞️ Video Frame Extractor")

video_file = st.file_uploader("📂 Upload a video", type=["mp4", "mov", "avi"])
select_all_flag = st.checkbox("Select All Frames")

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

        st.subheader("🎞️ Select Frames to Download")

        selected_frames = []
        cols = st.columns(6)

        for i in range(total_frames):
            frame_time = i / fps
            frame = clip.get_frame(frame_time)
            img = Image.fromarray(frame)

            with cols[i % 6]:
                st.image(img, caption=f"Frame {i}", use_container_width=True)
                if select_all_flag or st.checkbox(f"Select {i}", key=f"frame_{i}"):
                    selected_frames.append((i, img))

        if selected_frames:
            output_dir = tempfile.mkdtemp()
            file_paths = []
            for idx, img in selected_frames:
                file_path = os.path.join(output_dir, f"frame_{idx:04d}.png")
                img.save(file_path)
                file_paths.append(file_path)

            # ZIP if more than 5, otherwise individual downloads
            if len(file_paths) > 5:
                zip_path = os.path.join(output_dir, "selected_frames.zip")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for f in file_paths:
                        zipf.write(f, os.path.basename(f))

                with open(zip_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    href = f'<a href="data:application/zip;base64,{b64}" download="selected_frames.zip" class="floating-btn">⬇️ Download ZIP ({len(file_paths)} frames)</a>'

                # Inject ZIP download button
                st.markdown(
                    f"""
                    <style>
                    .floating-btn {{
                        position: fixed;
                        bottom: 60px;
                        right: 30px;
                        background-color: #0066cc;
                        color: white;
                        padding: 12px 20px;
                        border-radius: 30px;
                        text-decoration: none;
                        font-weight: bold;
                        font-size: 16px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                        z-index: 9999;
                    }}
                    .floating-btn:hover {{
                        background-color: #004d99;
                        color: white;
                    }}
                    </style>
                    {href}
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown("### ⬇️ Download Selected Frames:")
                for path in file_paths:
                    with open(path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        fname = os.path.basename(path)
                        href = f'<a href="data:image/png;base64,{b64}" download="{fname}">🖼️ {fname}</a>'
                        st.markdown(href, unsafe_allow_html=True)

    finally:
        clip.close()
        os.unlink(tfile.name)
