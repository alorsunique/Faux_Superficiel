import os
from datetime import datetime
from pathlib import Path
import shutil
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from gfpgan import GFPGANer
from realesrgan import RealESRGANer

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Faux_Superficiel Resources"

deep_dir = resources_dir / "Photo Deep"
output_dir = deep_dir / "Output"
output_transplant_dir = output_dir / "Transplant"
upscale_dir = deep_dir / "Upscale"

output_list = []
for entry in output_transplant_dir.rglob('*'):
    if entry.is_file():
        if entry.parent.name == "Transplant":
            output_list.append(f"{entry.name}")
        else:
            output_list.append(f"{entry.parent.name}/{entry.name}")

upscale_list = []
for entry in upscale_dir.rglob('*'):
    if entry.is_file():
        if entry.parent.name == "Upscale":
            upscale_list.append(f"{entry.name}")
        else:
            upscale_list.append(f"{entry.parent.name}/{entry.name}")

output_set = set(output_list)
upscale_set = set(upscale_list)
extra_set = upscale_set.difference(output_set)
to_upscale_set = output_set.difference(upscale_set)

for entry in extra_set:
    file_dir = upscale_dir / entry
    os.remove(file_dir)

dir_list = []

for entry in upscale_dir.rglob('*'):
    if entry.is_dir():
        dir_list.append(entry)



for entry in dir_list:
    if not any(entry.iterdir()):
        print(f"{entry} is empty")
        shutil.rmtree(entry)

general_resources_dir = Path("D:\Projects\General Resources")
RealESRGAN_model_dir = str(general_resources_dir / "RealESRGAN_x2plus.pth")
GFPGAN_model_dir = str(general_resources_dir / "GFPGANv1.4.pth")

to_upscale_list = sorted(list(to_upscale_set))

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
bg_upsampler = RealESRGANer(
    scale=2,
    #model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
    model_path=RealESRGAN_model_dir,
    model=model,
    tile=400,
    tile_pad=10,
    pre_pad=0,
    half=True)  # need to set False in CPU mode

model_path = os.path.join('gfpgan/weights', "GFPGANv1.4" + '.pth')
#model_path = os.path.join('gfpgan/weights', "GFPGANv1.3" + '.pth')
arch = 'clean'
channel_multiplier = 2

restorer = GFPGANer(
    model_path=GFPGAN_model_dir,
    upscale=1,
    arch=arch,
    channel_multiplier=channel_multiplier,
    bg_upsampler=bg_upsampler)


global_now = datetime.now()
global_start_time = global_now
global_current_time = global_now.strftime("%H:%M:%S")
print(f"Session Start Time: {global_current_time}\n")

for entry in to_upscale_list:
    file_dir = output_transplant_dir / entry
    print(file_dir.name)

    input_img = cv2.imread(str(file_dir), cv2.IMREAD_COLOR)
    cropped_faces, restored_faces, restored_img = restorer.enhance(
        input_img,
        paste_back=True,
        weight=0.5)

    if file_dir.parent.name != "Transplant":
        output_folder = upscale_dir / file_dir.parent.name
        if not output_folder.exists():
            os.mkdir(output_folder)
    else:
        output_folder = upscale_dir

    output_name = output_folder / f"{file_dir.name}"
    cv2.imwrite(str(output_name), restored_img)

global_now = datetime.now()
global_finish_time = global_now
global_current_time = global_now.strftime("%H:%M:%S")
print(f"\n\nSession End Time: {global_current_time}")
print(f"Total Session Run Time: {global_finish_time - global_start_time}")
