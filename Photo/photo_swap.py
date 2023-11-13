import itertools
import json
import os
from pathlib import Path

import insightface
from insightface.app import FaceAnalysis

from Photo import swapping_pack as sp

os.chdir(Path.cwd().parent)

# Buffalo and Inswapper are imported here

# buffalo =FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"]) # For CPU use only
buffalo = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider"])
buffalo.prepare(ctx_id=0, det_size=(640, 640))

with open("Inswapper Directory.txt", "r") as inswapper_text:
    inswapper_path = Path(inswapper_text.readline())

print(f"Importing inswapper")

# inswapper = insightface.model_zoo.get_model(str(inswapper_path), download=False, download_zip = False, providers=["CPUExecutionProvider"]) # For CPU use only
inswapper = insightface.model_zoo.get_model(str(
    inswapper_path), download=False, download_zip=False, providers=["CUDAExecutionProvider"])

# Setting up the directories


with open("Resources Directory.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

if not resources_dir.exists():
    os.mkdir(resources_dir)

photo_folder_dir = resources_dir / "Photo"
if not photo_folder_dir.exists():
    os.mkdir(photo_folder_dir)

base_dir = photo_folder_dir / "Base"
if not base_dir.exists():
    os.mkdir(base_dir)

transplant_dir = photo_folder_dir / "Transplant"
if not transplant_dir.exists():
    os.mkdir(transplant_dir)

output_dir = photo_folder_dir / "Output"
if not output_dir.exists():
    os.mkdir(output_dir)

base_output_dir = output_dir / "Base Output"
if not base_output_dir.exists():
    os.mkdir(base_output_dir)

transplant_output_dir = output_dir / "Transplant Output"
if not transplant_output_dir.exists():
    os.mkdir(transplant_output_dir)

# Performing a check on combinations to be done

base_file_list = []

for entry in base_dir.rglob('*'):
    if entry.is_file():
        base_file_list.append(entry)

transplant_file_list = []

for entry in transplant_dir.rglob('*'):
    if entry.is_file():
        transplant_file_list.append(entry)

checked_pack = []
check_JSON_dir = photo_folder_dir / "Check.json"

if check_JSON_dir.exists():
    if os.stat(check_JSON_dir).st_size > 0:
        with open(check_JSON_dir, "r") as json_file:
            checked_pack = json.load(json_file)

combination_list = list(itertools.product(
    base_file_list, transplant_file_list))
copy_list = combination_list.copy()
for entry in copy_list:
    if str(entry).upper() in checked_pack:
        combination_list.remove(entry)

combination_length = len(combination_list)
print(f"Combinations to be performed: {len(combination_list)}")

# Determining which swap function will be used

unique_base_list = set()
unique_transplant_list = set()
for combination in combination_list:
    base_entry = combination[0]
    transplant_entry = combination[1]
    unique_base_list.add(base_entry)
    unique_transplant_list.add(transplant_entry)

print(f"Size of initial base: {len(unique_base_list)}")
print(f"Size of initial transplant: {len(unique_transplant_list)}")

if len(unique_base_list) >= len(unique_transplant_list):
    print(f"Transplant will be used as base")
    base_as_tranplant_condition = True
else:
    print(f"Base retained")
    base_as_tranplant_condition = False

if base_as_tranplant_condition:
    inverted_list = sorted([(entry_2, entry_1)
                            for entry_1, entry_2 in combination_list])
    working_list = inverted_list
else:
    working_list = sorted(combination_list)

# Swapping is done here

if not base_as_tranplant_condition:
    print(f"Performing Normal Swap")
    sp.normal_swap(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                   checked_pack, check_JSON_dir)
else:
    print(f"Performing Invert Swap")
    sp.invert_swap(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                   checked_pack, check_JSON_dir)
