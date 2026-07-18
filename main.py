import os
from moviepy import VideoFileClip

INPUT_FOLDER = "Input"
OUTPUT_FOLDER = "Output"


os.makedirs(OUTPUT_FOLDER, exist_ok=True)

VIDEO_EXTENSIONS = (".mp4", ".mkv", ".avi", ".mov")

for filename in os.listdir(INPUT_FOLDER):

    if filename.lower().endswith(VIDEO_EXTENSIONS):

        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"{filename}"
        )

        try:
            print(f"Processing: {filename}")

            video = VideoFileClip(input_path)

            # Remove last 3 secondsn
            trimmed = video.subclipped(0, video.duration - 2)

            trimmed.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac"
            )

            video.close()
            trimmed.close()

            print(f"Saved: {output_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Done.")