from pathlib import Path
import subprocess

# ----------------------------
# Configuration
# ----------------------------

INPUT_FOLDER = Path("input_videos")
OUTPUT_FOLDER = Path("output_videos")

OUTPUT_FOLDER.mkdir(exist_ok=True)

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
)

# ----------------------------
# Process every video
# ----------------------------

for video in INPUT_FOLDER.iterdir():

    if video.suffix.lower() not in VIDEO_EXTENSIONS:
        continue

    output = OUTPUT_FOLDER / f"{video.stem}_shorts.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video),

        "-vf",
        (
            "scale=1080:1920:"
            "force_original_aspect_ratio=increase,"
            "crop=1080:1920"
        ),

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",

        "-c:a", "aac",
        "-b:a", "192k",

        str(output)
    ]

    print(f"Processing: {video.name}")

    subprocess.run(command)

print("\nDone!")