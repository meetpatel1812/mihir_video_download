import streamlit as st
import yt_dlp
import os

st.title("🎬 Vimeo Private Video Downloader")

video_url = st.text_input("Enter Vimeo Video URL:")
cookie_file = "cookies.txt"  # Ensure this file exists

def download_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'vimeo_%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': True,
            'cookiefile': cookie_file  # Load Vimeo session cookies
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            if not info_dict:
                st.error("Could not extract video information. The video may be private or restricted.")
                return None

            video_title = info_dict.get('title', 'vimeo_video')
            video_filename = ydl.prepare_filename(info_dict)

            st.write(f"**Video Title:** {video_title}")
            
            if 'thumbnail' in info_dict:
                st.image(info_dict['thumbnail'], caption="Thumbnail", use_column_width=True)

            if st.button("Download Video"):
                with st.spinner(f"Downloading {video_title}..."):
                    ydl.download([url])

                if os.path.exists(video_filename):
                    with open(video_filename, "rb") as f:
                        st.success("✅ Download complete!")
                        st.download_button(
                            "Save Video",
                            data=f,
                            file_name=os.path.basename(video_filename),
                            mime="video/mp4"
                        )
                    os.remove(video_filename)
                else:
                    st.error("❌ Download failed. The video might be restricted or unavailable.")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

if video_url:
    download_video(video_url)
