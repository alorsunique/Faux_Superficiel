# This script should create subclips of a chose interval of a given video for the whole duration of the video

import os
import shutil
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips

os.chdir(Path.cwd().parent)

with open("Resources Directory.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

video_folder_dir = resources_dir / "Video"

if not video_folder_dir.exists():
    os.mkdir(video_folder_dir)

workspace_dir = video_folder_dir / "Temporary Workspace"

if not resources_dir.exists():
    os.mkdir(resources_dir)

if not workspace_dir.exists():
    os.mkdir(workspace_dir)

# Change working directory
os.chdir(workspace_dir)

subclip_input_dir = video_folder_dir / "Subclip Input"
if not subclip_input_dir.exists():
    os.mkdir(subclip_input_dir)

subclip_output_dir = video_folder_dir / "Subclip Output"
if not subclip_output_dir.exists():
    os.mkdir(subclip_output_dir)

# Subclip creation for every video in the input folder is done here

for video_file in subclip_input_dir.iterdir():
    video = VideoFileClip(str(video_file))
    video_fps = video.fps

    interval = 5  # Clips of specified seconds will be creation
    current_start_time = 0
    current_end_time = interval

    N = 8  # Padding for the clip number
    count = 0

    # Create a folder containing all the clips
    clip_folder_dir = subclip_output_dir / f"{video_file.stem}"
    if not clip_folder_dir.exists():
        os.mkdir(clip_folder_dir)

    # This loop should create all the clips possible with integer multiple of the interval
    while current_end_time < video.duration:
        print(f"Start: {current_start_time} | End: {current_end_time}")

        count += 1
        output_name = f"{video_file.stem}_{count:0{N}}{video_file.suffix}"
        output_path = clip_folder_dir / output_name

        subclip = video.subclip(current_start_time, current_end_time)
        subclip.write_videofile(str(output_path), audio_codec='aac')

        current_start_time += interval
        current_end_time += interval

    # This should finish the remaining part of the last clip
    if current_start_time <= video.duration:
        current_end_time = video.duration
        print(f"Start: {current_start_time} | End: {current_end_time}")

        count += 1

        output_name = f"{video_file.stem}_{count:0{N}}{video_file.suffix}"
        output_path = clip_folder_dir / output_name

        subclip = video.subclip(current_start_time, current_end_time)
        subclip.write_videofile(str(output_path), audio_codec='aac')

    video.reader.close()

# It is possible that creating the subclips can get corrupted
# Checking if any of the subclips is corrupted is done here

print(f"Checking Subclips")

for video_folder in subclip_output_dir.iterdir():

    subclip_list = []

    for subclip in video_folder.iterdir():
        subclip_list.append(subclip)

    sorted_subclip_list = sorted(subclip_list)

    # Attempt at building the clips again to see if there is no corrupted subclip

    video_clip_added = []
    for sorted_clip in sorted_subclip_list:
        video_clip_added.append(VideoFileClip(str(sorted_clip)))

    for clip in video_clip_added:
        clip.reader.close()

    final_video = concatenate_videoclips(video_clip_added)
    output_dir = workspace_dir / f"{video_folder.name}.mp4"

    print(f"Rebuilding {video_folder.name}")

    try:
        # A video file will be written regardless of the result of this try except block
        final_video.write_videofile(str(output_dir), codec='libx264')
    except OSError as error:

        print(error)
        # However here, the folder where subclips were written will be deleted if there is a corrupted subclip
        # All the remaining folders in the subclip output are considered valid
        shutil.rmtree(video_folder)

    final_video.close()

# Clearing of the temporary workspace
for entry in workspace_dir.iterdir():
    print(f"Removing: {entry.name}")
    os.remove(entry)
