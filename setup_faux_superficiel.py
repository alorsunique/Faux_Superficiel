import os
from pathlib import Path

resources_dir_text = "Resources_Path.txt"

with open(resources_dir_text, 'a') as writer:
    writer.close()

model_dir_text = "Inswapper_Model_Path.txt"

with open(model_dir_text, 'a') as writer:
    writer.close()

model_dir_text = "GFPGAN_Model_Path.txt"

with open(model_dir_text, 'a') as writer:
    writer.close()

model_dir_text = "RealESRGAN_Model_Path.txt"

with open(model_dir_text, 'a') as writer:
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

    photo_dir = resources_dir / "Photo"

    if not photo_dir.exists():
        os.mkdir(photo_dir)

    video_dir = resources_dir / "Video"

    if not video_dir.exists():
        os.mkdir(video_dir)
else:
    print(f"Empty resource text file")