import json
import os
from collections import defaultdict

# ----------------------------------------------------
# Paths
# ----------------------------------------------------
DATASET = "dataset"

ANNOTATIONS = os.path.join(DATASET, "annotations", "annotations.json")
SPLITS = os.path.join(DATASET, "annotations", "train_val_test_distribution_file.json")

LABELS = os.path.join(DATASET, "labels")

# ----------------------------------------------------
# Create label folders
# ----------------------------------------------------
for split in ("train", "val", "test"):
    os.makedirs(os.path.join(LABELS, split), exist_ok=True)

# ----------------------------------------------------
# Load files
# ----------------------------------------------------
print("Loading JSON...")

with open(ANNOTATIONS, "r") as f:
    coco = json.load(f)

with open(SPLITS, "r") as f:
    split_data = json.load(f)

print("Done.")

# ----------------------------------------------------
# Build image lookup
# ----------------------------------------------------
images = {}

for img in coco["images"]:
    images[img["id"]] = img

print(f"Images: {len(images)}")

# ----------------------------------------------------
# Build category map
# ----------------------------------------------------
categories = sorted(coco["categories"], key=lambda c: c["id"])

category_map = {}

print("\nClasses:")

for new_id, cat in enumerate(categories):
    category_map[cat["id"]] = new_id
    print(f" {new_id} -> {cat['name']}")

# ----------------------------------------------------
# Build filename -> split lookup
# ----------------------------------------------------
filename_to_split = {}

for split in ("train", "val", "test"):
    for filename in split_data[split]:
        filename_to_split[filename.lower()] = split

# ----------------------------------------------------
# Group annotations by image
# ----------------------------------------------------
annotations_by_image = defaultdict(list)

for ann in coco["annotations"]:
    annotations_by_image[ann["image_id"]].append(ann)

print(f"\nAnnotations: {len(coco['annotations'])}")

# ----------------------------------------------------
# Statistics
# ----------------------------------------------------
images_written = 0
labels_written = 0
images_skipped = 0
bad_boxes = 0

# ----------------------------------------------------
# Convert
# ----------------------------------------------------
print("\nConverting...\n")

for image_id, image in images.items():

    filename = image["file_name"]

    split = filename_to_split.get(filename.lower())

    if split is None:
        images_skipped += 1
        continue

    width = image["width"]
    height = image["height"]

    if width <= 0 or height <= 0:
        images_skipped += 1
        continue

    label_path = os.path.join(
        LABELS,
        split,
        os.path.splitext(filename)[0] + ".txt"
    )

    with open(label_path, "w") as out:

        for ann in annotations_by_image[image_id]:

            bbox = ann.get("bbox")

            if bbox is None or len(bbox) != 4:
                bad_boxes += 1
                continue

            x, y, w, h = bbox

            if w <= 0 or h <= 0:
                bad_boxes += 1
                continue

            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height
            w /= width
            h /= height

            class_id = category_map.get(ann["category_id"])

            if class_id is None:
                print("Unknown category:", ann["category_id"])
                continue

            out.write(
                f"{class_id} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{w:.6f} "
                f"{h:.6f}\n"
            )

            labels_written += 1

    images_written += 1

# ----------------------------------------------------
# Create YAML automatically
# ----------------------------------------------------
yaml_path = os.path.join(DATASET, "trash.yaml")

with open(yaml_path, "w") as f:

    f.write(f"path: {DATASET}\n\n")
    f.write("train: images/train\n")
    f.write("val: images/val\n")
    f.write("test: images/test\n\n")

    f.write("names:\n")

    for new_id, cat in enumerate(categories):
        f.write(f"  {new_id}: {cat['name']}\n")

# ----------------------------------------------------
# Summary
# ----------------------------------------------------
print("\n==============================")
print("Conversion Complete")
print("==============================")
print(f"Images processed : {images_written}")
print(f"Labels written   : {labels_written}")
print(f"Bad boxes        : {bad_boxes}")
print(f"Skipped images   : {images_skipped}")
print(f"YAML created     : {yaml_path}")
print("==============================")