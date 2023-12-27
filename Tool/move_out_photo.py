import os
import shutil
from pathlib import Path

os.chdir(Path.cwd().parent)

with open("Resources Directory.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

# Setting up the directories

photo_folder_dir = resources_dir / "Photo"

transplant_dir = photo_folder_dir / "Transplant"

output_dir = photo_folder_dir / "Output"
output_base_dir = output_dir / "Base Output"
output_transplant_dir = output_dir / "Transplant Output"
upscale_output_dir = photo_folder_dir / "Upscale"

move_out_dir = photo_folder_dir / "Move Out"

if not move_out_dir.exists():
    os.mkdir(move_out_dir)

move_out_output_dir = move_out_dir / "Output"
move_out_upscale_dir = move_out_dir / "Upscale"

if not move_out_output_dir.exists():
    os.mkdir(move_out_output_dir)

if not move_out_upscale_dir.exists():
    os.mkdir(move_out_upscale_dir)

move_out_transplant_dir = move_out_output_dir / "Transplant Output"

if not move_out_transplant_dir.exists():
    os.mkdir(move_out_transplant_dir)

transplant_folder_list = []

for entry in transplant_dir.iterdir():
    transplant_folder_list.append(entry.name)

output_folder_list = []

for entry in output_transplant_dir.iterdir():
    output_folder_list.append(entry.name)

upscale_folder_list = []

for entry in upscale_output_dir.iterdir():
    upscale_folder_list.append(entry.name)

transplant_set = set(transplant_folder_list)
output_set = set(output_folder_list)
upscale_set = set(upscale_folder_list)

for entry in output_set.difference(transplant_set):
    source_dir = output_transplant_dir / entry
    shutil.move(source_dir, move_out_transplant_dir)

for entry in upscale_set.difference(transplant_set):
    source_dir = upscale_output_dir / entry
    shutil.move(source_dir, move_out_upscale_dir)
