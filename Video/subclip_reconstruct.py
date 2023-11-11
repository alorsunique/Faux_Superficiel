import os
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Faux_Superficiel Resources"
video_dir = resources_dir / "Video"

if not video_dir.exists():
    os.mkdir(video_dir)

workspace_dir = resources_dir / "Temporary Workspace"

if not resources_dir.exists():
    os.mkdir(resources_dir)

if not workspace_dir.exists():
    os.mkdir(workspace_dir)

os.chdir(workspace_dir)

swap_dir = video_dir / "Swap"
if not swap_dir.exists():
    os.mkdir(swap_dir)

deep_video_out_dir = swap_dir / "Swap Video Output"
if not deep_video_out_dir.exists():
    os.mkdir(deep_video_out_dir)

deep_reconstruct_dir = swap_dir / "Swap Reconstruct"
if not deep_reconstruct_dir.exists():
    os.mkdir(deep_reconstruct_dir)

for face in deep_video_out_dir.iterdir():
    for clip_folder in face.iterdir():

        unique_transplant_list = []

        for clip in clip_folder.iterdir():
            clip_name = str(clip.stem)[:-9]
            if clip_name not in unique_transplant_list:
                unique_transplant_list.append(str(clip.stem)[:-9])

        for transplant in unique_transplant_list:
            clip_list = []
            for entry in clip_folder.iterdir():
                if transplant in str(entry):
                    clip_list.append(entry)

            sorted_list = sorted(clip_list)

            video_clip_added = []
            for sorted_clip in sorted_list:
                video_clip_added.append(VideoFileClip(str(sorted_clip)))

            for clip in video_clip_added:
                clip.reader.close()

            final_video = concatenate_videoclips(video_clip_added)

            output_folder = deep_reconstruct_dir / face.name
            if not output_folder.exists():
                os.mkdir(output_folder)

            output_name = f"{clip_folder.name}_{transplant}.mp4"
            output_path = output_folder / output_name
            try:
                final_video.write_videofile(str(output_path), codec='libx264')
            except OSError as error:
                print(error)
                os.remove(output_path)

            final_video.close()

for entry in workspace_dir.iterdir():
    print(f"Removing: {entry.name}")
    os.remove(entry)
