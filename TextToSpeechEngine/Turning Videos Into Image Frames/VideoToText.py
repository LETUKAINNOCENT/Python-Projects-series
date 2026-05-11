import os
import re
import cv2
import shutil
import imagehash
import pytesseract

from PIL import Image
from difflib import SequenceMatcher


class VideoBookExtractor:

    # -------------------------------------------------
    # INITIALIZE
    # -------------------------------------------------
    def __init__(
        self,
        hash_threshold=5,
        similarity_threshold=0.60,
        tesseract_config=r'--oem 3 --psm 6'
    ):

        self.hash_threshold = hash_threshold
        self.similarity_threshold = similarity_threshold
        self.tesseract_config = tesseract_config


    # -------------------------------------------------
    # CREATE DIRECTORY
    # -------------------------------------------------
    def create_dir(self, path):

        os.makedirs(path, exist_ok=True)


    # -------------------------------------------------
    # CLEAN OCR TEXT
    # -------------------------------------------------
    def clean_text(self, text):

        text = text.lower()

        text = re.sub(r'\s+', ' ', text)

        return text.strip()


    # -------------------------------------------------
    # PAGE SIGNATURE
    # -------------------------------------------------
    def get_page_signature(self, text, length=150):

        text = self.clean_text(text)

        return text[:length]


    # -------------------------------------------------
    # STEP 1:
    # VIDEO → FRAMES
    # -------------------------------------------------
    def video_to_frames(self, video_path, output_path):

        video_name = os.path.splitext(
            os.path.basename(video_path)
        )[0]

        save_path = os.path.join(
            output_path,
            video_name
        )

        self.create_dir(save_path)

        cap = cv2.VideoCapture(video_path)

        prev_gray = None
        prev_img = None

        page_count = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            # -----------------------------------------
            # FIRST FRAME
            # -----------------------------------------
            if prev_gray is None:

                cv2.imwrite(
                    os.path.join(
                        save_path,
                        f"page_{page_count}.png"
                    ),
                    frame
                )

                page_count += 1

                prev_gray = gray
                prev_img = frame

                continue

            # -----------------------------------------
            # PIXEL DIFFERENCE
            # -----------------------------------------
            diff = cv2.absdiff(
                prev_gray,
                gray
            )

            score = diff.mean()

            # Save only different frames
            if score != 0:

                cv2.imwrite(
                    os.path.join(
                        save_path,
                        f"page_{page_count}.png"
                    ),
                    prev_img
                )

                prev_img = frame
                prev_gray = gray

                page_count += 1

        cap.release()

        return save_path


    # -------------------------------------------------
    # STEP 2:
    # HASH FILTER
    # -------------------------------------------------
    def filter_duplicate_images(
        self,
        frames_path
    ):

        unique_dir = os.path.join(
            frames_path,
            "unique_pages"
        )

        self.create_dir(unique_dir)

        prev_hash = None

        page_count = 0
        count = 0

        for image_file in os.listdir(frames_path):

            if not image_file.endswith(".png"):
                continue

            image_path = os.path.join(
                frames_path,
                f"page_{page_count}.png"
            )

            img = Image.open(image_path)

            current_hash = imagehash.phash(img)

            # -----------------------------------------
            # FIRST IMAGE
            # -----------------------------------------
            if prev_hash is None:

                save_path = os.path.join(
                    unique_dir,
                    f"page_{count}.png"
                )

                shutil.copy(
                    image_path,
                    save_path
                )

                prev_hash = current_hash

                page_count += 1
                count += 1

                continue

            # -----------------------------------------
            # HASH DIFFERENCE
            # -----------------------------------------
            hash_diff = current_hash - prev_hash

            if hash_diff > self.hash_threshold:

                save_path = os.path.join(
                    unique_dir,
                    f"page_{count}.png"
                )

                shutil.copy(
                    image_path,
                    save_path
                )

                prev_hash = current_hash

                count += 1

            page_count += 1

        return unique_dir


    # -------------------------------------------------
    # STEP 3:
    # OCR + SEMANTIC FILTER
    # -------------------------------------------------
    def extract_unique_text(
        self,
        frames_path
    ):

        previous_signature = ""

        all_text = ""

        cout = 0

        for image_file in os.listdir(frames_path):

            if not image_file.endswith(".png"):
                continue

            print(cout)

            image_path = os.path.join(
                frames_path,
                f"page_{cout}.png"
            )

            img = Image.open(image_path)

            text = pytesseract.image_to_string(
                img,
                config=self.tesseract_config
            )

            signature = self.get_page_signature(
                text
            )

            similarity = SequenceMatcher(
                None,
                signature,
                previous_signature
            ).ratio()

            # -----------------------------------------
            # KEEP UNIQUE TEXT
            # -----------------------------------------
            if similarity < self.similarity_threshold:

                print(
                    f"KEEP TEXT: {image_path}"
                )

                all_text += "\n\n" + text

                previous_signature = signature

            cout += 1

        return all_text


    # -------------------------------------------------
    # FULL PIPELINE
    # -------------------------------------------------
    def process_video(
        self,
        video_path,
        output_path
    ):

        # Step 1
        frames_dir = self.video_to_frames(
            video_path,
            output_path
        )

        # Step 2
        unique_frames = self.filter_duplicate_images(
            frames_dir
        )

        # Step 3
        text = self.extract_unique_text(
            unique_frames
        )

        return text