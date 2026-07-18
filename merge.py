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

    timeline.append(
        # clip.crossfadein(TRANSITION)
        clip.with_effects([CrossFadeIn(TRANSITION)])
    )

# ==========================================
# MERGE
# ==========================================

final = CompositeVideoClip(
    timeline,
    size=timeline[0].size
)

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