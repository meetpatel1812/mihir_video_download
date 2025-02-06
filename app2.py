# import streamlit as st
# import yt_dlp
# import os

# st.title("🎬 Vimeo Private Video Downloader")

# video_url = st.text_input("Enter Vimeo Video URL:")
# cookie_file = "cookies.txt"  # Ensure this file exists

# def download_video(url):
#     try:
#         ydl_opts = {
#             'format': 'bestvideo+bestaudio/best',
#             'outtmpl': 'vimeo_%(title)s.%(ext)s',
#             'quiet': False,
#             'no_warnings': True,
#             'cookiefile': cookie_file  # Load Vimeo session cookies
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
            
#             if not info_dict:
#                 st.error("Could not extract video information. The video may be private or restricted.")
#                 return None

#             video_title = info_dict.get('title', 'vimeo_video')
#             video_filename = ydl.prepare_filename(info_dict)

#             st.write(f"**Video Title:** {video_title}")
            
#             if 'thumbnail' in info_dict:
#                 st.image(info_dict['thumbnail'], caption="Thumbnail", use_column_width=True)

#             if st.button("Download Video"):
#                 with st.spinner(f"Downloading {video_title}..."):
#                     ydl.download([url])

#                 if os.path.exists(video_filename):
#                     with open(video_filename, "rb") as f:
#                         st.success("✅ Download complete!")
#                         st.download_button(
#                             "Save Video",
#                             data=f,
#                             file_name=os.path.basename(video_filename),
#                             mime="video/mp4"
#                         )
#                     os.remove(video_filename)
#                 else:
#                     st.error("❌ Download failed. The video might be restricted or unavailable.")

#     except Exception as e:
#         st.error(f"⚠️ Error: {str(e)}")

# if video_url:
#     download_video(video_url)



import streamlit as st
import yt_dlp
import os
import ffmpeg  # ffmpeg-python wrapper

st.title("🎬 Vimeo Private Video Downloader")

video_url = st.text_input("Enter Vimeo Video URL:")
cookie_file = "cookies.txt"  # Ensure this file exists

def download_video(url):
    try:
        # ydl_opts = {
        #     'format': 'bestvideo+bestaudio/best',
        #     'outtmpl': 'vimeo_%(title)s.%(ext)s',
        #     'quiet': False,
        #     'no_warnings': True,
        #     'cookiefile': cookie_file  # Load Vimeo session cookies
        # }
        ydl_opts = {
    'format': 'bv*+ba/best',  # Picks the best available single file format
    'outtmpl': 'vimeo_%(title)s.%(ext)s',
    'quiet': False,
    'no_warnings': True,
    'cookiefile': cookie_file,
    'merge_output_format': 'mp4'  # Ensures output is in MP4 format
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

                output_file = f"{video_title}.mp4"
                ffmpeg.input(video_filename).output(output_file, vcodec='libx264').run()

                if os.path.exists(output_file):
                    with open(output_file, "rb") as f:
                        st.success("✅ Download complete!")
                        st.download_button(
                            "Save Video",
                            data=f,
                            file_name=os.path.basename(output_file),
                            mime="video/mp4"
                        )
                    os.remove(video_filename)
                    os.remove(output_file)
                else:
                    st.error("❌ Download failed. The video might be restricted or unavailable.")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

if video_url:
    download_video(video_url)
