# Run this right after the download finishes
from stegano import lsb
import os

clean_folder = "D:/stegoproject/dataset/clean"
stego_folder = "D:/stegoproject/dataset/stego"
os.makedirs(stego_folder, exist_ok=True)

secret = "ThisIsHiddenData1234"
failed = 0

for filename in os.listdir(clean_folder):
    if filename.endswith(".jpg"):
        clean_path = os.path.join(clean_folder, filename)
        stego_path = os.path.join(stego_folder, filename.replace(".jpg", ".png"))
        try:
            lsb.hide(clean_path, secret).save(stego_path)
            print(f"Stego created: {filename}")
        except Exception as e:
            failed += 1
            print(f"Skipped {filename}: {e}")

print(f"\nDone! Failed: {failed}")
