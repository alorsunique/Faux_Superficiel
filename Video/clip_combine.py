import gc
import os
from pathlib import Path

from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Faux_Superficiel Resources"

video_dir = resources_dir / "Video"

if not video_dir.exists():
    os.mkdir(video_dir)

workspace_dir = video_dir / "Temporary Workspace"

clip_output_dir = video_dir / "Clip Output"
if not clip_output_dir.exists():
    os.mkdir(clip_output_dir)

clip_combine_dir = video_dir / "Clip Combine"
if not clip_combine_dir.exists():
    os.mkdir(clip_combine_dir)

unique_title_list = []

for entry in clip_output_dir.iterdir():
    print(entry.name)
    name_split = entry.name.split("_")
    print(name_split[:-1])
    unique_title = "_".join(name_split[:-1])
    print(unique_title)
    if unique_title not in unique_title_list:
        unique_title_list.append(unique_title)

print(unique_title_list)

for unique_title in unique_title_list:

    clip_list = []

    for entry in clip_output_dir.iterdir():
        entry_split = entry.name.split("_")
        title = "_".join(entry_split[:-1])

        if title == unique_title:
            clip_list.append(entry)

    print(clip_list)

    sorted_clip_list = sorted(clip_list)

    video_clip_added = []
    for sorted_clip in sorted_clip_list:
        video_clip_added.append(VideoFileClip(str(sorted_clip)))

    for clip in video_clip_added:
        clip.reader.close()

    final_video = concatenate_videoclips(video_clip_added)



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





