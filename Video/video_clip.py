# This script should extract a subclip from a video file

import gc
import os
from pathlib import Path

from moviepy.editor import VideoFileClip

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Faux_Superficiel Resources"

video_dir = resources_dir / "Video"

if not video_dir.exists():
    os.mkdir(video_dir)

workspace_dir = video_dir / "Temporary Workspace"

if not resources_dir.exists():
    os.mkdir(resources_dir)

if not workspace_dir.exists():
    os.mkdir(workspace_dir)

# Changes the working directory to the workspace
os.chdir(workspace_dir)

clip_input_dir = video_dir / "Clip Input"
if not clip_input_dir.exists():
    os.mkdir(clip_input_dir)

clip_output_dir = video_dir / "Clip Output"
if not clip_output_dir.exists():
    os.mkdir(clip_output_dir)

input_list = []

for entry in clip_input_dir.rglob('*'):
    if entry.is_file():
        input_list.append(entry)

break_condition = False
N = 8
# Main loop of the program
while True:
    in_count = 0
    print(f"0: Exit Loop")
    for input_video in input_list:
        print(f"{in_count + 1}: {input_list[in_count].name}")
        in_count += 1

    try:
        choice = int(input(f"Select Option: "))

        if int(choice) == 0:
            break_condition = True
        elif int(choice) < 0 or int(choice) > len(input_list):
            print(f"Out of Bound")
        else:
            # Creation of clips is done here

            entry = input_list[choice - 1]
            print(f"Video: {entry.stem}")
            t_i = int(input(f"Starting Time: "))
            t_f = int(input(f"Ending Time: "))
            initial_t_f = t_f
            interval = t_f - t_i

            # In the interval_subclip code, the interval was set to 5 seconds hence the modulo of 5
            if interval % 5 == 0:
                print("Shifting End Time by 0.25 s")
                t_f += 0.25

            output_name = f"{entry.stem}_{t_i:0{N}}-{initial_t_f:0{N}}{entry.suffix}"
            output_path = clip_output_dir / output_name

            video = VideoFileClip(str(entry))
            new_clip = video.subclip(t_i, t_f)
            new_clip.write_videofile(str(output_path), audio_codec='aac')
            new_clip.close()
            video.reader.close()
            gc.collect()

    except:
        print(f"Did not catch that")

    if break_condition:
        break

# Clearing of the temporary workspace
for entry in workspace_dir.iterdir():
    print(f"Removing: {entry.name}")
    os.remove(entry)

