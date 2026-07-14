from yt_dlp import YoutubeDL

def download_video(url):
    with YoutubeDL({
        "format": "best",
        "outtmpl": "video.%(ext)s"
    }) as ydl:
        ydl.download([url])

    return "video.mp4"