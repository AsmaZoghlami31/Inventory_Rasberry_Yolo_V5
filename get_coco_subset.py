from ultralytics.data.utils import download_coco_dataset
import json
import os
import shutil

# Download COCO val2017 (5K images)
coco_dir = r"C:\Users\zoghl\Projects\YOLO\yolov5\datasets\coco"
os.makedirs(coco_dir, exist_ok=True)
download_coco_dataset("val2017", coco_dir)  # Downloads to datasets\coco

# Load annotations
with open(f"{coco_dir}/annotations/instances_val2017.json") as f:
    coco_data = json.load(f)

# Filter images with "person" (0) or "cell phone" (67)
target_classes = [0, 67]  # COCO IDs
image_ids = set()
for ann in coco_data["annotations"]:
    if ann["category_id"] in target_classes:
        image_ids.add(ann["image_id"])

# Copy relevant images
coco_images_dir = f"{coco_dir}/images/val2017"
coco_labels_dir = f"{coco_dir}/labels/val2017"
os.makedirs(coco_labels_dir, exist_ok=True)
for img in coco_data["images"]:
    if img["id"] in image_ids:
        img_path = f"{coco_images_dir}/{img['file_name']}"
        shutil.copy(img_path, f"{coco_dir}/filtered_images/{img['file_name']}")

# Convert COCO to YOLO format for filtered images
from ultralytics.data.converter import convert_coco
convert_coco(labels_dir=f"{coco_dir}/annotations/", output_dir=coco_labels_dir, use_keypoints=False)
print("COCO subset ready!")