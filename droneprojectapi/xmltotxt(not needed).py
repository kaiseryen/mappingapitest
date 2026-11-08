import os
import xml.etree.ElementTree as ET

# Change these paths
xml_folder = "dataset/AnnotationsHAIDA"
output_folder = "dataset/temp"

# Class mapping
class_map = {
    "bottle": 0
}

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(xml_folder):
    if not filename.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(xml_folder, filename))
    root = tree.getroot()

    width = float(root.find("size/width").text)
    height = float(root.find("size/height").text)

    output_file = os.path.join(
        output_folder,
        filename.replace(".xml", ".txt")
    )

    with open(output_file, "w") as f:

        for obj in root.findall("object"):

            name = obj.find("name").text

            if name not in class_map:
                continue

            class_id = class_map[name]

            box = obj.find("bndbox")

            xmin = float(box.find("xmin").text)
            ymin = float(box.find("ymin").text)
            xmax = float(box.find("xmax").text)
            ymax = float(box.find("ymax").text)

            x_center = ((xmin + xmax) / 2) / width
            y_center = ((ymin + ymax) / 2) / height
            box_width = (xmax - xmin) / width
            box_height = (ymax - ymin) / height

            f.write(
                f"{class_id} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{box_width:.6f} "
                f"{box_height:.6f}\n"
            )

print("Conversion complete.")