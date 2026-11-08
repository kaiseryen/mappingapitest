from pathlib import Path
import shutil


imgs = [Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/test"),
        Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/train"),
        Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/val")]

anns = [Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/test"),
        Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/train"),
        Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/val")]


img1 = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/temp")
ann1 = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/temp")

imgf = sorted(img1.glob("*"))
annf = sorted(ann1.glob("*"))
#trash_folder.mkdir(exist_ok=True)

for n in range(1):

    for i,file_path in enumerate(imgf):
        if file_path.is_file():

            if i % 8 == 0:
                toimg = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/test")
                toann = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/test")
            elif i % 8 == 1:
                toimg = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/val")
                toann = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/val")
            else:
                toimg = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/images/train")
                toann = Path("/Users/kaiseryen/Downloads/droneprojectapi/dataset/labels/train")


            d1 = toimg / file_path.name
            d2 = toann / annf[i].name
            print(f"{file_path.name} -> {d1}")
            print(f"{annf[i].name} -> {d2}")

            shutil.move(str(file_path), d1)
            shutil.move(str(annf[i]), d2)


            i += 1

print("big fart butt poop")
