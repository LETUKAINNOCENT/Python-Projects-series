import os
import cv2
from glob import glob

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_frame(video_path, save_dir, gap=1):  # default = 1 (max frames)
    name = os.path.splitext(os.path.basename(video_path))[0]
    save_path = os.path.join(save_dir, name)
    create_dir(save_path)

    cap = cv2.VideoCapture(video_path)
    
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Save every frame when gap=1
        if idx % gap == 0:
            cv2.imwrite(os.path.join(save_path, f"{idx}.png"), gray)

        idx += 1

    cap.release()

if __name__ == "__main__":
    video_paths = glob("videos/*")
    save_dir = "__local__save"

    for path in video_paths:
        save_frame(path, save_dir)  # no need to pass gap