import os
import subprocess
import streamlit as st

# Define path to FFmpeg binary
FFMPEG_PATH = "./bin/ffmpeg"  # FFmpeg must be pre-downloaded and stored in 'bin/'

# Ensure FFmpeg has execute permissions
if not os.access(FFMPEG_PATH, os.X_OK):
    os.chmod(FFMPEG_PATH, 0o755)

st.title("🎬 FFmpeg Video Processor in Streamlit Cloud")

# Test if FFmpeg is working
try:
    result = subprocess.run([FFMPEG_PATH, "-version"], capture_output=True, text=True)
    st.text(result.stdout)
except Exception as e:
    st.error(f"FFmpeg execution failed: {e}")

# Upload video file
uploaded_file = st.file_uploader("📤 Upload a Video File", type=["mp4", "mkv", "avi", "mov"])

if uploaded_file is not None:
    input_video_path = f"input_{uploaded_file.name}"
    
    # Save uploaded video locally
    with open(input_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Convert video using FFmpeg
    output_video_path = f"converted_{uploaded_file.name}"
    
    if st.button("🎥 Convert to MP4"):
        with st.spinner("Processing video..."):
            cmd = [FFMPEG_PATH, "-i", input_video_path, "-c:v", "libx264", output_video_path]
            process = subprocess.run(cmd, capture_output=True, text=True)

            if process.returncode == 0:
                st.success("✅ Video conversion successful!")
                
                # Provide download button
                with open(output_video_path, "rb") as f:
                    st.download_button("⬇️ Download Converted Video", data=f, file_name=output_video_path, mime="video/mp4")
                
                # Cleanup files
                os.remove(input_video_path)
                os.remove(output_video_path)
            else:
                st.error("❌ Video conversion failed. See logs:")
                st.text(process.stderr)
