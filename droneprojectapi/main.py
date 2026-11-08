
"""
PROJECT NOTES

clean up the code

"""



import time
import filesetup
import frames_to_map
import json
import ai_main
from map import mapopener


start = time.perf_counter()
video_path = input("Enter video path: ")
srt_path = input("Enter srt path: ")
filesetup.clear_folder()
filesetup.create_frames(video_path)
frames_to_map.mapmarker(frames_to_map.linksrt(ai_main.videocheck()))


print("time passed:", time.perf_counter() - start,"seconds") # Timer

with open("map/markers.json","r") as f:
    data = json.load(f)

print(data)










