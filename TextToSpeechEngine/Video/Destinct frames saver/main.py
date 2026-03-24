import os
import cv2
from glob import glob

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_pages(video_path, save_dir, threshold=15):
    name = os.path.splitext(os.path.basename(video_path))[0]
    save_path = os.path.join(save_dir, name)
    create_dir(save_path)

    cap = cv2.VideoCapture(video_path)

    prev_gray = None
    prev_img = None
    page_count = 0
    frame_idx = 0
    save_next_change = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            # cv2.imwrite(os.path.join(save_path, f"page_{page_count}.png"), frame)
            page_count += 1
            prev_gray = gray
            prev_img = frame
            continue

        diff = cv2.absdiff(prev_gray, gray)
        score = diff.mean()

        if score > threshold:

            if(save_next_change):
                cv2.imwrite(os.path.join(save_path, f"page_{page_count}.png"), prev_img)
                save_next_change = False
            else :
                save_next_change = True
            
            prev_img = frame
            page_count += 1
              
        prev_gray = gray
        frame_idx += 1

    cap.release()
    print(f"Extracted {page_count} pages")

if __name__ == "__main__":
    video_paths = glob("videos/*")
    save_dir = "__pages__"

    for path in video_paths:
        extract_pages(path, save_dir,10)