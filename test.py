import os

ffmpeg_path = os.environ.get("FFMPEG_PATH")
if ffmpeg_path:
    print(f"FFmpeg path: {ffmpeg_path}")
else:
    print("FFmpeg path not found in the system environment.")
