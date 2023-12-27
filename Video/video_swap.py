import gc
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2
import insightface
from insightface.app import FaceAnalysis
from moviepy.editor import ImageSequenceClip
from moviepy.editor import VideoFileClip


def print_size(size):
    print_size = float(size)
    partition_count = 0
    while print_size >= 1000:
        print_size /= 1000
        partition_count += 1
    if partition_count == 0:
        partition_text = "B"
    elif partition_count == 1:
        partition_text = "KB"
    elif partition_count == 2:
        partition_text = "MB"
    elif partition_count == 3:
        partition_text = "GB"
    print_size_string = f"{round(print_size, 2)} {partition_text}"
    return print_size_string


os.chdir(Path.cwd().parent)

print(f"Importing Buffalo")
buffalo = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider"])
buffalo.prepare(ctx_id=0, det_size=(640, 640))

with open("Inswapper Directory.txt", "r") as inswapper_text:
    inswapper_path = Path(inswapper_text.readline())

print(f"Importing inswapper")

inswapper = insightface.model_zoo.get_model(str(inswapper_path), download=False, download_zip=False,
                                            providers=["CUDAExecutionProvider"])

with open("Resources Directory.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

video_folder_dir = resources_dir / "Video"

if not video_folder_dir.exists():
    os.mkdir(video_folder_dir)

workspace_dir = video_folder_dir / "Temporary Workspace"

if not workspace_dir.exists():
    os.mkdir(workspace_dir)

# Changes the working directory to the workspace
os.chdir(workspace_dir)

swap = video_folder_dir / "Swap"
if not swap.exists():
    os.mkdir(swap)

swap_video_input_dir = swap / "Swap Video Input"
if not swap_video_input_dir.exists():
    os.mkdir(swap_video_input_dir)

swap_video_out_dir = swap / "Swap Video Output"
if not swap_video_out_dir.exists():
    os.mkdir(swap_video_out_dir)

transplant_faces_dir = swap / "Face"
if not transplant_faces_dir.exists():
    os.mkdir(transplant_faces_dir)

checked_pack = []
check_JSON_dir = video_folder_dir / "Check.json"

if check_JSON_dir.exists():
    if os.stat(check_JSON_dir).st_size > 0:
        with open(check_JSON_dir, "r") as json_file:
            checked_pack = json.load(json_file)

transplant_faces_list = []

for entry in transplant_faces_dir.rglob('*'):
    if entry.is_file():
        transplant_faces_list.append(entry)

video_file_list = []

for entry in swap_video_input_dir.rglob('*'):
    if entry.is_file():
        video_file_list.append(entry)

global_now = datetime.now()
global_start_time = global_now
global_current_time = global_now.strftime("%H:%M:%S")
print(f"Session Start Time: {global_current_time}\n")

for face in transplant_faces_list:
    face_image = cv2.imread(str(face))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

    transplant_faces = buffalo.get(face_image)
    transplant_face = transplant_faces[0]

    for video_file in video_file_list:

        print(f"Working with: {face.parent.name} {face.stem} | {video_file.parent.name} {video_file.name}")
        combination = (face, video_file)

        if not str(combination).upper() in checked_pack:

            video_path = video_file

            video = VideoFileClip(str(video_path))
            audio = video.audio
            fps = video.fps
            frames = video.iter_frames(fps=fps)
            duration = video.duration
            frame_estimate = int(duration * fps)

            new_frame_list = []
            count = 0

            now = datetime.now()
            start_time = now
            current_time = now.strftime("%H:%M:%S")
            print(f"Combination Start Time: {current_time}\n")

            for frame in frames:
                count += 1
                sys.stdout.write(f"\rFrame {count} | Estimated {frame_estimate} Frames")
                append_frame = frame

                try:
                    base_faces = buffalo.get(frame)
                    pass_condition = True
                except:
                    pass_condition = False

                if len(base_faces) > 0 and len(transplant_faces) > 0 and pass_condition:
                    base_copy = frame.copy()
                    for base_face in base_faces:
                        base_copy = inswapper.get(base_copy, base_face, transplant_faces[0], paste_back=True)
                    append_frame = base_copy
                new_frame_list.append(append_frame)

            time.sleep(1)

            new_video = ImageSequenceClip(new_frame_list, fps=fps)
            new_video = new_video.set_audio(audio)

            video.reader.close()
            gc.collect()

            video_name_segment = f"{video_file.stem[-8:]}"

            if face.parent.stem == "Face":
                face_name_segment = f"{face.stem}"
                output_face_folder = swap_video_out_dir
            else:
                face_name_segment = f"{face.parent.stem}_{face.stem}"
                output_face_folder = swap_video_out_dir / f"{face.parent.name}"
                if not output_face_folder.exists():
                    os.mkdir(output_face_folder)

            output_folder = output_face_folder / video_file.parent.name
            if not output_folder.exists():
                os.mkdir(output_folder)

            output_path = output_folder / f"{face_name_segment}_{video_name_segment}{video_file.suffix}"
            new_video.write_videofile(str(output_path), codec='libx264')

            now = datetime.now()
            finish_time = now
            current_time = now.strftime("%H:%M:%S")
            print(f"\n\nCombination End Time: {current_time}")
            print(f"Total Combination Run Time: {finish_time - start_time}")

            new_video.close()
            gc.collect()

            checked_pack.append(str(combination).upper())

            json_file = open(check_JSON_dir, "w")
            json.dump(checked_pack, json_file)
            json_file.close()

global_now = datetime.now()
global_finish_time = global_now
global_current_time = global_now.strftime("%H:%M:%S")
print(f"\n\nSession End Time: {global_current_time}")
print(f"Total Session Run Time: {global_finish_time - global_start_time}")

# Clearing of the temporary workspace
for entry in workspace_dir.iterdir():
    print(f"Removing: {entry.name}")
    os.remove(entry)
