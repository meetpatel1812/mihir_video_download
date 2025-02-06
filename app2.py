import streamlit as st
import yt_dlp
import os

st.title("🎬 Vimeo Private Video Downloader")

# Input for Vimeo video URL
video_url = st.text_input("Enter Vimeo Video URL:")

# Path to the cookies file and FFmpeg binaries
cookie_file = "cookies.txt"  # Ensure this file exists
ffmpeg_path = os.path.join("bin", "ffmpeg.exe")  # Path to ffmpeg.exe
ffplay_path = os.path.join("bin", "ffplay.exe")  # Path to ffplay.exe
ffprobe_path = os.path.join("bin", "ffprobe.exe")  # Path to ffprobe.exe

def download_video(url):
    try:
        # Options for yt-dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'vimeo_%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': True,
            'cookiefile': cookie_file,  # Load Vimeo session cookies
            'ffmpeg_location': os.path.dirname(ffmpeg_path),  # Set FFmpeg directory
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(url, download=False)
            
            if not info_dict:
                st.error("Could not extract video information. The video may be private or restricted.")
                return None

            # Get video title and prepare filename
            video_title = info_dict.get('title', 'vimeo_video')
            video_filename = ydl.prepare_filename(info_dict)

            st.write(f"**Video Title:** {video_title}")
            
            # Display thumbnail if available
            if 'thumbnail' in info_dict:
                st.image(info_dict['thumbnail'], caption="Thumbnail", use_column_width=True)

            # Download button
            if st.button("Download Video"):
                with st.spinner(f"Downloading {video_title}..."):
                    ydl.download([url])  # Download the video

                # Check if the file was downloaded successfully
                if os.path.exists(video_filename):
                    with open(video_filename, "rb") as f:
                        st.success("✅ Download complete!")
                        st.download_button(
                            "Save Video",
                            data=f,
                            file_name=os.path.basename(video_filename),
                            mime="video/mp4"
                        )
                    os.remove(video_filename)  # Clean up the file after offering it for download
                else:
                    st.error("❌ Download failed. The video might be restricted or unavailable.")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# Start the download process if a URL is provided
if video_url:
    download_video(video_url)