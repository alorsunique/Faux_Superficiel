# Python file containing the functions for swapping photos

import json
import os
import sys

import cv2


def normal_swap(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                checked_pack, check_JSON_dir):
    combination_list = working_list
    combination_count = 0

    unique_base_list = []
    for combination in combination_list:
        if combination[0] not in unique_base_list:
            unique_base_list.append(combination[0])

    for entry in unique_base_list:
        base_image_path = entry
        base_image = cv2.imread(str(base_image_path))
        try:
            base_faces = buffalo.get(base_image)
            base_pass_condition = True
            print(f"\nBase: {entry.parent.name} | {entry.name}\n")
        except:
            print(
                f"\nError occured: {base_image_path.parent.name}: {base_image_path.name}")
            base_pass_condition = False
        if len(base_faces) > 0 and base_pass_condition:
            transplant_list = []
            for combination in combination_list:
                if entry == combination[0]:
                    transplant_list.append(combination[1])

            for pair_entry in transplant_list:
                combination_count += 1
                transplant_image_path = pair_entry
                transplant_image = cv2.imread(str(transplant_image_path))

                try:
                    transplant_faces = buffalo.get(transplant_image)
                    transplant_pass_condition = True
                except:
                    print(
                        f"\nError occured: {transplant_image_path.parent.name}: {transplant_image_path.name}")
                    transplant_pass_condition = False

                if len(transplant_faces) > 0 and transplant_pass_condition:

                    if base_image_path.parent.name != "Base":
                        base_output_folder_name = base_output_dir / base_image_path.parent.name
                        if not base_output_folder_name.exists():
                            os.mkdir(base_output_folder_name)
                    else:
                        base_output_folder_name = base_output_dir

                    if transplant_image_path.parent.name != "Transplant":
                        transplant_output_folder_name = transplant_output_dir / \
                                                        transplant_image_path.parent.name
                        if not transplant_output_folder_name.exists():
                            os.mkdir(transplant_output_folder_name)
                    else:
                        transplant_output_folder_name = transplant_output_dir

                    sys.stdout.write(
                        f"\r{combination_count}/{combination_length} | {base_image_path.parent.name}: {base_image_path.name} | {transplant_image_path.parent.name}: {transplant_image_path.name}")

                    base_count = 0
                    for base_face in base_faces:
                        base_count += 1
                        transplant_count = 0
                        for transplant_face in transplant_faces:
                            transplant_count += 1
                            base_copy = base_image.copy()
                            base_copy = inswapper.get(
                                base_copy, base_face, transplant_face, paste_back=True)

                            base_name = f"{base_image_path.parent.name}_{base_image_path.stem}"
                            transplant_name = f"{transplant_image_path.parent.name}_{transplant_image_path.stem}"
                            number_name = f"b{base_count}t{transplant_count}.jpg"
                            output_name = f"{base_name}_{transplant_name}_{number_name}"

                            append_string = str(
                                (base_image_path, transplant_image_path))
                            checked_pack.append(append_string.upper())

                            base_output_path = base_output_folder_name / output_name
                            transplant_output_path = transplant_output_folder_name / output_name
                            cv2.imwrite(str(base_output_path), base_copy)
                            cv2.imwrite(str(transplant_output_path), base_copy)

    json_file = open(check_JSON_dir, "w")
    json.dump(checked_pack, json_file)
    json_file.close()


def invert_swap(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                checked_pack, check_JSON_dir):
    combination_list = working_list
    combination_count = 0

    unique_base_list = []
    for combination in combination_list:
        if combination[0] not in unique_base_list:
            unique_base_list.append(combination[0])

    for entry in unique_base_list:
        base_image_path = entry
        base_image = cv2.imread(str(base_image_path))
        try:
            base_faces = buffalo.get(base_image)
            base_pass_condition = True
            print(f"\nBase: {entry.parent.name} | {entry.name}\n")
        except:
            print(
                f"\nError occured: {base_image_path.parent.name}: {base_image_path.name}")
            base_pass_condition = False
        if len(base_faces) > 0 and base_pass_condition:
            transplant_list = []
            for combination in combination_list:
                if entry == combination[0]:
                    transplant_list.append(combination[1])

            for pair_entry in transplant_list:
                combination_count += 1
                transplant_image_path = pair_entry
                transplant_image = cv2.imread(str(transplant_image_path))

                try:
                    transplant_faces = buffalo.get(transplant_image)
                    transplant_pass_condition = True
                except:
                    print(
                        f"\nError occured: {transplant_image_path.parent.name}: {transplant_image_path.name}")
                    transplant_pass_condition = False

                if len(transplant_faces) > 0 and transplant_pass_condition:

                    if base_image_path.parent.name != "Transplant":
                        base_output_folder_name = transplant_output_dir / base_image_path.parent.name
                        if not base_output_folder_name.exists():
                            os.mkdir(base_output_folder_name)
                    else:
                        base_output_folder_name = transplant_output_dir

                    if transplant_image_path.parent.name != "Base":
                        transplant_output_folder_name = base_output_dir / \
                                                        transplant_image_path.parent.name
                        if not transplant_output_folder_name.exists():
                            os.mkdir(transplant_output_folder_name)
                    else:
                        transplant_output_folder_name = base_output_dir

                    sys.stdout.write(
                        f"\r{combination_count}/{combination_length} | {base_image_path.parent.name}: {base_image_path.name} | {transplant_image_path.parent.name}: {transplant_image_path.name}")

                    base_count = 0
                    for base_face in base_faces:
                        base_count += 1
                        transplant_count = 0
                        for transplant_face in transplant_faces:
                            transplant_count += 1
                            base_copy = transplant_image.copy()
                            base_copy = inswapper.get(
                                base_copy, transplant_face, base_face, paste_back=True)

                            transplant_name = f"{base_image_path.parent.name}_{base_image_path.stem}"
                            base_name = f"{transplant_image_path.parent.name}_{transplant_image_path.stem}"
                            number_name = f"b{base_count}t{transplant_count}.jpg"
                            output_name = f"{base_name}_{transplant_name}_{number_name}"

                            append_string = str(
                                (transplant_image_path, base_image_path))
                            checked_pack.append(append_string.upper())

                            base_output_path = base_output_folder_name / output_name
                            transplant_output_path = transplant_output_folder_name / output_name
                            cv2.imwrite(str(base_output_path), base_copy)
                            cv2.imwrite(str(transplant_output_path), base_copy)

    json_file = open(check_JSON_dir, "w")
    json.dump(checked_pack, json_file)
    json_file.close()


def normal_swap_all_face(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                         checked_pack, check_JSON_dir):
    combination_list = working_list
    combination_count = 0

    unique_base_list = []
    for combination in combination_list:
        if combination[0] not in unique_base_list:
            unique_base_list.append(combination[0])

    for entry in unique_base_list:
        base_image_path = entry
        base_image = cv2.imread(str(base_image_path))
        try:
            base_faces = buffalo.get(base_image)
            base_pass_condition = True
            print(f"\nBase: {entry.parent.name} | {entry.name}\n")
        except:
            print(
                f"\nError occured: {base_image_path.parent.name}: {base_image_path.name}")
            base_pass_condition = False
        if len(base_faces) > 0 and base_pass_condition:
            transplant_list = []
            for combination in combination_list:
                if entry == combination[0]:
                    transplant_list.append(combination[1])

            for pair_entry in transplant_list:
                combination_count += 1
                transplant_image_path = pair_entry
                transplant_image = cv2.imread(str(transplant_image_path))

                try:
                    transplant_faces = buffalo.get(transplant_image)
                    transplant_pass_condition = True
                except:
                    print(
                        f"\nError occured: {transplant_image_path.parent.name}: {transplant_image_path.name}")
                    transplant_pass_condition = False

                if len(transplant_faces) > 0 and transplant_pass_condition:

                    if base_image_path.parent.name != "Base":
                        base_output_folder_name = base_output_dir / base_image_path.parent.name
                        if not base_output_folder_name.exists():
                            os.mkdir(base_output_folder_name)
                    else:
                        base_output_folder_name = base_output_dir

                    if transplant_image_path.parent.name != "Transplant":
                        transplant_output_folder_name = transplant_output_dir / \
                                                        transplant_image_path.parent.name
                        if not transplant_output_folder_name.exists():
                            os.mkdir(transplant_output_folder_name)
                    else:
                        transplant_output_folder_name = transplant_output_dir

                    sys.stdout.write(
                        f"\r{combination_count}/{combination_length} | {base_image_path.parent.name}: {base_image_path.name} | {transplant_image_path.parent.name}: {transplant_image_path.name}")

                    base_count = 0
                    base_copy = base_image.copy()
                    for base_face in base_faces:
                        base_count += 1
                        transplant_count = 0

                        for transplant_face in transplant_faces:
                            transplant_count += 1
                            base_copy = inswapper.get(
                                base_copy, base_face, transplant_face, paste_back=True)

                    base_name = f"{base_image_path.parent.name}_{base_image_path.stem}"
                    transplant_name = f"{transplant_image_path.parent.name}_{transplant_image_path.stem}"
                    number_name = f"ballt{transplant_count}.jpg"
                    output_name = f"{base_name}_{transplant_name}_{number_name}"

                    append_string = str(
                        (base_image_path, transplant_image_path))
                    checked_pack.append(append_string.upper())

                    base_output_path = base_output_folder_name / output_name
                    transplant_output_path = transplant_output_folder_name / output_name
                    cv2.imwrite(str(base_output_path), base_copy)
                    cv2.imwrite(str(transplant_output_path), base_copy)

    json_file = open(check_JSON_dir, "w")
    json.dump(checked_pack, json_file)
    json_file.close()


def invert_swap_all_face(working_list, buffalo, base_output_dir, transplant_output_dir, inswapper, combination_length,
                         checked_pack, check_JSON_dir):
    combination_list = working_list
    combination_count = 0

    unique_base_list = []
    for combination in combination_list:
        if combination[0] not in unique_base_list:
            unique_base_list.append(combination[0])

    for entry in unique_base_list:
        base_image_path = entry
        base_image = cv2.imread(str(base_image_path))
        try:
            base_faces = buffalo.get(base_image)
            base_pass_condition = True
            print(f"\nBase: {entry.parent.name} | {entry.name}\n")
        except:
            print(
                f"\nError occured: {base_image_path.parent.name}: {base_image_path.name}")
            base_pass_condition = False
        if len(base_faces) > 0 and base_pass_condition:
            transplant_list = []
            for combination in combination_list:
                if entry == combination[0]:
                    transplant_list.append(combination[1])

            for pair_entry in transplant_list:
                combination_count += 1
                transplant_image_path = pair_entry
                transplant_image = cv2.imread(str(transplant_image_path))

                try:
                    transplant_faces = buffalo.get(transplant_image)
                    transplant_pass_condition = True
                except:
                    print(
                        f"\nError occured: {transplant_image_path.parent.name}: {transplant_image_path.name}")
                    transplant_pass_condition = False

                if len(transplant_faces) > 0 and transplant_pass_condition:

                    if base_image_path.parent.name != "Transplant":
                        base_output_folder_name = transplant_output_dir / base_image_path.parent.name
                        if not base_output_folder_name.exists():
                            os.mkdir(base_output_folder_name)
                    else:
                        base_output_folder_name = transplant_output_dir

                    if transplant_image_path.parent.name != "Base":
                        transplant_output_folder_name = base_output_dir / \
                                                        transplant_image_path.parent.name
                        if not transplant_output_folder_name.exists():
                            os.mkdir(transplant_output_folder_name)
                    else:
                        transplant_output_folder_name = base_output_dir

                    sys.stdout.write(
                        f"\r{combination_count}/{combination_length} | {base_image_path.parent.name}: {base_image_path.name} | {transplant_image_path.parent.name}: {transplant_image_path.name}")

                    base_count = 0
                    base_copy = transplant_image.copy()
                    for base_face in base_faces:
                        base_count += 1
                        transplant_count = 0
                        for transplant_face in transplant_faces:
                            transplant_count += 1
                            base_copy = inswapper.get(
                                base_copy, transplant_face, base_face, paste_back=True)

                    transplant_name = f"{base_image_path.parent.name}_{base_image_path.stem}"
                    base_name = f"{transplant_image_path.parent.name}_{transplant_image_path.stem}"
                    number_name = f"ballt{transplant_count}.jpg"
                    output_name = f"{base_name}_{transplant_name}_{number_name}"

                    append_string = str(
                        (transplant_image_path, base_image_path))
                    checked_pack.append(append_string.upper())

                    base_output_path = base_output_folder_name / output_name
                    transplant_output_path = transplant_output_folder_name / output_name
                    cv2.imwrite(str(base_output_path), base_copy)
                    cv2.imwrite(str(transplant_output_path), base_copy)

    json_file = open(check_JSON_dir, "w")
    json.dump(checked_pack, json_file)
    json_file.close()
