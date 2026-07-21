"""
Automatic COD Sniper Montage Maker
----------------------------------
Input:
    clips/
        clip1.mp4
        clip2.mp4
        clip3.mp4
        ...
Output:
    sniper_montage.mp4
"""
from pathlib import Path
from moviepy import *
from tqdm import tqdm
from moviepy.video.fx.CrossFadeIn import CrossFadeIn
from moviepy.audio.fx.AudioFadeIn import AudioFadeIn
import random

# ==========================================
# SETTINGS
# ==========================================
INPUT_FOLDER = "clips"
OUTPUT_FILE = "sniper_montage.mp4"
TRANSITION = 0.4          # seconds
FPS = 60
RANDOM_ORDER = False
REMOVE_AUDIO = False
TARGET_RESOLUTION = None  # e.g. (1920, 1080) to force-resize all clips, or None to use first clip's size

# ==========================================
# LOAD FILES
# ==========================================
video_files = []
for ext in ("*.mp4", "*.mov", "*.avi", "*.mkv", "*.webm"):
    video_files.extend(Path(INPUT_FOLDER).glob(ext))
video_files = sorted(video_files)

if RANDOM_ORDER:
    random.shuffle(video_files)

if len(video_files) == 0:
    raise Exception("No videos found!")

print(f"Found {len(video_files)} clips")

# ==========================================
# LOAD CLIPS
# ==========================================
clips = []
for file in tqdm(video_files):
    clip = VideoFileClip(str(file))
    if REMOVE_AUDIO:
        clip = clip.without_audio()
    clips.append(clip)

target_size = TARGET_RESOLUTION or clips[0].size

# Resize any mismatched clips so CompositeVideoClip doesn't misalign them
clips = [
    c if c.size == target_size else c.resized(target_size)
    for c in clips
]

# ==========================================
# APPLY TRANSITIONS
# ==========================================
timeline = []
current_time = 0
for i, clip in enumerate(clips):
    if i == 0:
        clip = clip.with_start(0)
        current_time = clip.duration
    else:
        clip = clip.with_start(current_time - TRANSITION)
        current_time += clip.duration - TRANSITION

        clip = clip.with_effects([CrossFadeIn(TRANSITION)])
        if clip.audio is not None:
            clip = clip.with_audio(
                clip.audio.with_effects([AudioFadeIn(TRANSITION)])
            )

    timeline.append(clip)

# ==========================================
# MERGE
# ==========================================
final = CompositeVideoClip(timeline, size=target_size)
final = final.with_duration(current_time)

# ==========================================
# EXPORT
# ==========================================
final.write_videofile(
    OUTPUT_FILE,
    codec="libx264",
    audio_codec="aac",
    fps=FPS,
    threads=8,
    preset="medium"
)

print("\nDone!")
