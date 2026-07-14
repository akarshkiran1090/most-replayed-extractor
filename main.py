from yt_dlp import YoutubeDL
from download import download_video

url = input("Enter URL: ")
video_file = download_video(url)

import subprocess

def create_clip(video_file, start, end, output):
    subprocess.run([
        "ffmpeg",
        "-i", video_file,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy",
        output
    ])

with YoutubeDL({
    "format": "best",
    "outtmpl": "%(id)s.%(ext)s",
    "force_overwrites": True
}) as ydl:
    info = ydl.extract_info(url, download=False)

heatmap = info.get("heatmap", [])

top = sorted(
    heatmap,
    key=lambda x: x["value"],
    reverse=True
)
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

print("\nTop Replay Peaks:\n")
for point in top[:10]:
    print(
        f"{format_time(point['start_time'])}"
        f" - "
        f"{format_time(point['end_time'])}"
        f" | Score: {point['value']:.3f}"
    )

def overlaps(start, end, clips):
    for clip_start, clip_end in clips:
        if start < clip_end and end > clip_start:
            return True

    return False

print("\nSuggested Clips:\n")

accepted_clips = []

clip_num = 1

for point in top:

    start = max(0, point["start_time"] - 15)
    end = point["end_time"] + 15

    if overlaps(start, end, accepted_clips):
        continue

    accepted_clips.append((start, end))

    create_clip(
        video_file,
        start,
        end,
        f"clip{clip_num}.mp4"
    )

    clip_num += 1

    if len(accepted_clips) == 5:
        break