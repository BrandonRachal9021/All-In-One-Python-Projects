import yt_dlp

def download_video(url, resolution='highest'):
    try:
        # If user wants specific resolution, pick progressive stream
        if resolution != 'highest':
            fmt = f'best[height<={resolution}]'
        else:
            # Best quality (video+audio separate, requires ffmpeg)
            fmt = 'bestvideo+bestaudio/best'

        ydl_opts = {
            'format': fmt,
            'outtmpl': '%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Download completed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ").strip()
    video_resolution = input("Enter resolution (e.g., 720 or leave blank for highest): ").strip()
    download_video(video_url, video_resolution or 'highest')