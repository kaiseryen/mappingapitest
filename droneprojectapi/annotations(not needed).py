import cv2
import os

image_path = "dataset/images/test/data1_48.jpg"
label_path = "dataset/labels/test/data1_48.txt"

image = cv2.imread(image_path)

h, w = image.shape[:2]

with open(label_path, "r") as f:
    for line in f:
        cls, xc, yc, bw, bh = map(float, line.split())

        xmin = int((xc - bw / 2) * w)
        ymin = int((yc - bh / 2) * h)
        xmax = int((xc + bw / 2) * w)
        ymax = int((yc + bh / 2) * h)

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"Class {int(cls)}",
            (xmin, ymin - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

cv2.imshow("Annotations", image)
cv2.waitKey(0)
cv2.destroyAllWindows()