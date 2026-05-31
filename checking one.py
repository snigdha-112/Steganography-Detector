import os

clean_folder = "D:/stegoproject/dataset/clean"
stego_folder = "D:/stegoproject/dataset/stego"

clean_count = len(os.listdir(clean_folder))
stego_count = len(os.listdir(stego_folder))

print(f"Clean images:  {clean_count}")
print(f"Stego images:  {stego_count}")
print(f"Total samples: {clean_count + stego_count}")

if clean_count == stego_count:
    print("\nPerfect! Dataset is balanced and ready to train.")
else:
    print(f"\nMismatch! {abs(clean_count - stego_count)} images didn't generate stego — still fine to train.")
