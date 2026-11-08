import cv2
from ultralytics import YOLO
import time
import os

model = YOLO("runs/detect/train/weights/best.pt")
def imgcheck(frame):
    # Finds the amount of detected garbage within a frame
    stuff = model.predict(frame)
    amount = len(stuff[0].boxes)
    return amount

def videocheck():
    frames = []

    for path in os.listdir("frames"):
        if imgcheck(rf"frames/{path}"):
            frames.append(int(path.split(".")[0]))

    return sorted(frames)

"""
VIDEO TESTING

start = time.perf_counter()
results = model.predict(
    source="IMG_0930.MOV",
    conf=0.15,
    imgsz=960,
    save=True
)
print("Elapsed:", time.perf_counter() - start,"seconds")
"""

"""
TRAINING CODE

model.train(
    data="dataset/trash.yaml",
    epochs=100,
    imgsz=960,
    batch=8,
    patience=20,
    device="mps",

)
"""


"""
TESTING CODE

results = model.predict(
    source="dataset/images/test",
    save=True,
    conf=0.25
)

metrics = model.val(
    data="dataset/trash.yaml",
    split="test"
)

print(metrics)
"""
