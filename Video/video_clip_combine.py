import math
import os
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips

os.chdir(Path.cwd().parent)

with open("Resources Directory.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

video_dir = resources_dir / "Video"
workspace_dir = video_dir / "Temporary Workspace"

os.chdir(workspace_dir)

clip_output_dir = video_dir / "Clip Output"
if not clip_output_dir.exists():
    os.mkdir(clip_output_dir)

clip_combine_dir = video_dir / "Clip Combine"
if not clip_combine_dir.exists():
    os.mkdir(clip_combine_dir)

# This part searches for all unique titles

unique_title_list = []

for entry in clip_output_dir.iterdir():
    entry_name_split = entry.name.split("_")
    unique_title = "_".join(entry_name_split[:-1])
    if unique_title not in unique_title_list:
        unique_title_list.append(unique_title)

# This part processes clips of the same video

for unique_title in unique_title_list:

    clip_list = []

    for entry in clip_output_dir.iterdir():
        entry_name_split = entry.name.split("_")
        title = "_".join(entry_name_split[:-1])

        if title == unique_title:
            clip_list.append(entry)

    sorted_clip_list = sorted(clip_list)

    video_clip_added = []
    for sorted_clip in sorted_clip_list:
        video_clip_added.append(VideoFileClip(str(sorted_clip)))

    for clip in video_clip_added:
        clip.reader.close()

    final_video = concatenate_videoclips(video_clip_added)
    print(f"Video duration: {final_video.duration}")
    print(f"Floor seconds: {math.floor(final_video.duration)}")

    if math.floor(final_video.duration) % 5 == 0:
        print("Removing the last and a quarter second")
        final_video = final_video.subclip(0, final_video.duration - 1.25)

    print(f"Trimmed duration: {final_video.duration}")

    output_name = f"{unique_title}.mp4"
    output_path = clip_combine_dir / output_name
    try:
        final_video.write_videofile(str(output_path), codec='libx264')
    except OSError as error:
        print(error)
        os.remove(output_path)

    final_video.close()

for entry in workspace_dir.iterdir():
    print(f"Removing: {entry.name}")
    os.remove(entry)
