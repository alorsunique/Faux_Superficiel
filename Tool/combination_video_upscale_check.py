import json
import os
import shutil
from pathlib import Path

os.chdir(Path.cwd().parent)

with open("Resources Directory.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

# Setting up the directories

video_folder_dir = resources_dir / "Video"
swap_folder_dir = video_folder_dir / "Swap"

face_dir = swap_folder_dir / "Face"
video_in_dir = swap_folder_dir / "Swap Video Input"
video_out_dir = swap_folder_dir / "Swap Video Upscale"

# Takes note of all face images

face_list = []

for entry in face_dir.rglob('*'):
    if entry.is_file():
        face_list.append(entry)

# Takes note of all video files

video_base_list = []

for entry in video_in_dir.rglob('*'):
    if entry.is_file():
        video_base_list.append(entry)

checked_pack = []

for face in face_list:

    for video in video_base_list:

        video_name_segment = f"{video.stem[-8:]}"

        if face.parent.stem == "Face":
            face_name_segment = f"{face.stem}"
            output_face_folder = video_out_dir
        else:
            face_name_segment = f"{face.parent.stem}_{face.stem}"
            output_face_folder = video_out_dir / f"{face.parent.name}"
            if not output_face_folder.exists():
                os.mkdir(output_face_folder)

        output_folder = output_face_folder / video.parent.name
        if not output_folder.exists():
            os.mkdir(output_folder)

        output_path = output_folder / f"{face_name_segment}_{video_name_segment}{video.suffix}"

        # Check for already done swaps

        if output_path.exists():
            checked_pack.append(str((face, video)).upper())

check_upscale_JSON_dir = video_folder_dir / "Check Upscale Compare.json"
with open(check_upscale_JSON_dir, "w") as json_file:
    json.dump(checked_pack, json_file)

check_JSON_dir = video_folder_dir / "Check Upscale.json"

if check_JSON_dir.exists():
    os.remove(check_JSON_dir)

shutil.copy2(check_upscale_JSON_dir, check_JSON_dir)
