import yt_dlp
import os
import uuid

def download_video(url: str) -> str:
    """
    Downloads a video from the given URL using yt-dlp and returns the file path.
    Saves the file with a unique ID to prevent collisions.
    """
    video_id = str(uuid.uuid4())
    output_template = f"temp_video_{video_id}.%(ext)s"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
    }
    
    print(f"Downloading video from {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Find the actual filename it downloaded to
            downloaded_file = ydl.prepare_filename(info_dict)
            return downloaded_file
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
