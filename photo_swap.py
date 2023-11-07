import numpy as np
import os
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from pathlib import Path
import itertools
import json
import sys
import shutil
import combination_pack as cp


# buffalo =FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"]) # For CPU use only
buffalo = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider"])
buffalo.prepare(ctx_id=0, det_size=(640, 640))

inswapper_folder = Path("D:\Projects\General Resources")
inswapper_path = inswapper_folder / "inswapper_128.onnx"

print(f"Importing inswapper")

# inswapper = insightface.model_zoo.get_model(str(inswapper_path), download=False, download_zip = False, providers=["CPUExecutionProvider"]) # For CPU use only
inswapper = insightface.model_zoo.get_model(str(
    inswapper_path), download=False, download_zip=False, providers=["CUDAExecutionProvider"])


project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Faux_Superficiel Resources"

if not resources_dir.exists():
    os.mkdir(resources_dir)

deep_dir = resources_dir / "Photo Deep"
if not deep_dir.exists():
    os.mkdir(deep_dir)

output_dir = deep_dir / "Output"
if not output_dir.exists():
    os.mkdir(output_dir)

base_output_dir = output_dir / "Base"
if not base_output_dir.exists():
    os.mkdir(base_output_dir)

transplant_output_dir = output_dir / "Transplant"
if not transplant_output_dir.exists():
    os.mkdir(transplant_output_dir)

base_dir = deep_dir / "Base"
if not base_dir.exists():
    os.mkdir(base_dir)

transplant_dir = deep_dir / "Transplant"
if not transplant_dir.exists():
    os.mkdir(transplant_dir)

base_file_list = []

for entry in base_dir.rglob('*'):
    if entry.is_file():
        base_file_list.append(entry)

transplant_file_list = []

for entry in transplant_dir.rglob('*'):
    if entry.is_file():
        transplant_file_list.append(entry)

checked_pack = []
check_JSON_dir = deep_dir / "Check.json"

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

if not base_as_tranplant_condition:
    print(f"Performing Normal Swap")
    cp.normal_swap(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                checked_pack, check_JSON_dir)
else:
    print(f"Performing Invert Swap")
    cp.invert_swap(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                checked_pack, check_JSON_dir)
