import os
import subprocess
import streamlit as st
import yt_dlp

# Define path to FFmpeg binary (must be uploaded to "bin/")
FFMPEG_PATH = "./bin/ffmpeg"

# Ensure FFmpeg has execute permissions
if not os.access(FFMPEG_PATH, os.X_OK):
    os.chmod(FFMPEG_PATH, 0o755)

st.title("🎬 Video Downloader & Converter")

# Input field for video URL
video_url = st.text_input("🔗 Enter Video URL (YouTube, Vimeo, etc.)")

# Function to download video using yt-dlp
def download_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'vimeo_%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': True,
            'cookiefile': cookie_file  # Uncomment if using cookies for Vimeo
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if not info_dict:
                st.error("❌ Failed to download video.")
                return None

        video_filename = ydl.prepare_filename(info_dict)
        return video_filename

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

if video_url:
    if st.button("⬇️ Download Video"):
        with st.spinner("Downloading video..."):
            video_file = download_video(video_url)

        if video_file and os.path.exists(video_file):
            st.success(f"✅ Download complete: {video_file}")

            # Convert video to MP4
            output_file = "converted_video.mp4"
            if st.button("🎥 Convert to MP4"):
                with st.spinner("Processing video..."):
                    cmd = [FFMPEG_PATH, "-i", video_file, "-c:v", "libx264", output_file]
                    process = subprocess.run(cmd, capture_output=True, text=True)

                    if process.returncode == 0:
                        st.success("✅ Video conversion successful!")

                        # Provide download button for converted video
                        with open(output_file, "rb") as f:
                            st.download_button("⬇️ Download Converted Video", data=f, file_name=output_file, mime="video/mp4")

                        # Cleanup files
                        os.remove(video_file)
                        os.remove(output_file)
                    else:
                        st.error("❌ Video conversion failed. See logs:")
                        st.text(process.stderr)
        else:
            st.error("❌ Video download failed. Please check the URL.")
