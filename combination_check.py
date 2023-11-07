from pathlib import Path

import os
import itertools
import json
import shutil

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Faux_Superficiel Resources"

deep_dir = resources_dir / "Photo Deep"
base_dir = deep_dir / "Base"
transplant_dir = deep_dir / "Transplant"
output_dir = deep_dir / "Output"
output_base_dir = output_dir / "Base"
output_transplant_dir = output_dir / "Transplant"

base_file_list = []

for entry in base_dir.rglob('*'):
    if entry.is_file():
        base_file_list.append(entry)

transplant_file_list = []

for entry in transplant_dir.rglob('*'):
    if entry.is_file():
        transplant_file_list.append(entry)

combined_processed_list_dict = dict()
for entry in output_dir.rglob('*'):
    if entry.is_file():
        combined_processed_list_dict[entry] = 0

checked_pack = []

for base_file in base_file_list:

    base_entry = base_file
    if base_entry.parent.name != "Base":
        base_parent_name = base_entry.parent.name
        base_name = base_entry.stem
        base_output_name = f"{base_parent_name}_{base_name}"
        base_search_dir = output_base_dir / base_entry.parent.name
    else:
        base_output_name = base_entry.stem
        base_search_dir = output_base_dir

    for transplant_file in transplant_file_list:

        # Determine the output name

        transplant_entry = transplant_file
        if transplant_entry.parent.name != "Transplant":
            transplant_parent_name = transplant_entry.parent.name
            transplant_name = transplant_entry.stem
            transplant_output_name = f"{transplant_parent_name}_{transplant_name}"
            transplant_search_dir = output_transplant_dir / transplant_entry.parent.name
        else:
            transplant_output_name = transplant_entry.stem
            transplant_search_dir = output_transplant_dir

        combination_output_name = f"{base_output_name}_{transplant_output_name}"

        base_condition = False
        transplant_condition = False

        if base_search_dir.exists():
            for output_file in base_search_dir.iterdir():

                output_file_name = str(output_file.stem)

                if combination_output_name in output_file_name:
                    combined_processed_list_dict[output_file] = 1
                    base_condition = True

        if transplant_search_dir.exists():
            for output_file in transplant_search_dir.iterdir():
                output_file_name = str(output_file.stem)

                if combination_output_name in output_file_name:
                    combined_processed_list_dict[output_file] = 1
                    transplant_condition = True

        if base_condition and transplant_condition:
            checked_pack.append(str((base_file, transplant_file)).upper())

check_JSON_dir = deep_dir / "Check Compare.json"
with open(check_JSON_dir, "w") as json_file:
    json.dump(checked_pack, json_file)

for entry in combined_processed_list_dict:
    if combined_processed_list_dict[entry] == 0:
        if entry.exists():
            print(f"Removing {entry}")
            os.remove(str(entry))

dir_list = []

for entry in output_dir.rglob('*'):
    if entry.is_dir():
        dir_list.append(entry)

for entry in base_dir.rglob('*'):
    if entry.is_dir():
        dir_list.append(entry)

for entry in transplant_dir.rglob('*'):
    if entry.is_dir():
        dir_list.append(entry)

for entry in dir_list:
    if not any(entry.iterdir()):
        print(f"{entry} is empty")
        shutil.rmtree(entry)

out_check_JSON_dir = deep_dir / "Check.json"

if out_check_JSON_dir.exists():
    os.remove(out_check_JSON_dir)

shutil.copy2(check_JSON_dir, out_check_JSON_dir)