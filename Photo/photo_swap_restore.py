# Uses GFPGAN to restore the faces

import os
import shutil
from datetime import datetime
from pathlib import Path

import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from gfpgan import GFPGANer
from realesrgan import RealESRGANer

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

photo_folder_dir = resources_dir / "Photo"
output_dir = photo_folder_dir / "Output"
output_transplant_dir = output_dir / "Transplant Output"

restore_dir = photo_folder_dir / "Restore"

if not restore_dir.exists():
    os.mkdir(restore_dir)

# Takes note of all the images in the output transplant folder

output_list = []
for entry in output_transplant_dir.rglob('*'):
    if entry.is_file():
        if entry.parent.name == "Transplant":
            output_list.append(f"{entry.name}")
        else:
            output_list.append(f"{entry.parent.name}/{entry.name}")

# Takes note of all the images in the upscale folder

restore_list = []
for entry in restore_dir.rglob('*'):
    if entry.is_file():
        if entry.parent.name == "Restore":
            restore_list.append(f"{entry.name}")
        else:
            restore_list.append(f"{entry.parent.name}/{entry.name}")

# Set comparison is done here

output_set = set(output_list)
restore_set = set(restore_list)
extra_set = restore_set.difference(output_set)
to_restore_set = output_set.difference(restore_set)
to_restore_list = (list(to_restore_set))

# Deletes all extra photos in the upscale folder
# Extra photos are images with no corresponding image in the output transplant folder

for entry in extra_set:
    file_dir = restore_dir / entry
    os.remove(file_dir)

folder_list = []

for entry in restore_dir.rglob('*'):
    if entry.is_dir():
        folder_list.append(entry)

# Delete all empty folders in the upscale directory

for entry in folder_list:
    if not any(entry.iterdir()):
        print(f"{entry} is empty")
        shutil.rmtree(entry)

# Imports the models used for face reconstruction

with open("RealESRGANx2 Directory.txt", "r") as realESRGAN_text:
    RealESRGAN_model_dir = str(Path(realESRGAN_text.readline()))

with open("GFPGAN Directory.txt", "r") as GFPGAN_text:
    GFPGAN_model_dir = str(Path(GFPGAN_text.readline()))

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
bg_upsampler = RealESRGANer(
    scale=2,
    model_path=RealESRGAN_model_dir,
    model=model,
    tile=400,
    tile_pad=10,
    pre_pad=0,
    half=True)  # need to set False in CPU mode

arch = 'clean'
channel_multiplier = 2

restorer = GFPGANer(
    model_path=GFPGAN_model_dir,
    upscale=1,
    arch=arch,
    channel_multiplier=channel_multiplier,
    bg_upsampler=bg_upsampler)

# Face restoration is done here

global_now = datetime.now()
global_start_time = global_now
global_current_time = global_now.strftime("%H:%M:%S")
print(f"Session Start Time: {global_current_time}\n")

count = 0
max_count = len(to_restore_list)

for entry in to_restore_list:
    count += 1
    file_dir = output_transplant_dir / entry
    print(f"{count}/{max_count} | Working: {file_dir.name}")

    input_img = cv2.imread(str(file_dir), cv2.IMREAD_COLOR)
    cropped_faces, restored_faces, restored_img = restorer.enhance(
        input_img,
        paste_back=True,
        weight=0.5)

    if file_dir.parent.name != "Transplant":
        output_folder = restore_dir / file_dir.parent.name
        if not output_folder.exists():
            os.mkdir(output_folder)
    else:
        output_folder = restore_dir

    output_name = output_folder / f"{file_dir.name}"
    cv2.imwrite(str(output_name), restored_img)

global_now = datetime.now()
global_finish_time = global_now
global_current_time = global_now.strftime("%H:%M:%S")
print(f"\n\nSession End Time: {global_current_time}")
print(f"Total Session Run Time: {global_finish_time - global_start_time}")
