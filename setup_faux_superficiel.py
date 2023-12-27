import os
from pathlib import Path

resources_dir_text = "Resources_Path.txt"

with open(resources_dir_text, 'a') as writer:
    writer.close()

entry_list = []

with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())
    reader.close()

if entry_list[0]:
    resources_dir = Path(entry_list[0])
    print(f"Resources Directory: {resources_dir}")

    if not resources_dir.exists():
        os.mkdir(resources_dir)

    input_dir = resources_dir / "Input"
    if not input_dir.exists():
        os.mkdir(input_dir)

    output_dir = resources_dir / "Output"
    if not output_dir.exists():
        os.mkdir(output_dir)
