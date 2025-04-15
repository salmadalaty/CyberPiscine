import sys
import os
from PIL import Image #to open image
from PIL.ExifTags import TAGS

def metadata(imgpath):
    if not os.path.isfile(imgpath):
        print("Path not found:", imgpath)
        return

    try:
        img = Image.open(imgpath)
        print("Path:", imgpath)
        print("Format:", img.format)
        print("Size:", img.size)
        print("Mode:", img.mode)

        exif = img.getexif()

        if not exif:
            print("No EXIF data found.")
            return

        print("EXIF Data:")
        for tid, value in exif.items():
            tag = TAGS.get(tid, tid)
            print(f"{tag}: {value}")
        print(" ")

    except Exception as e:
        print(f"Error: {e}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scorpion.py <image1> <image2> ...")
        sys.exit(1)

    for path in sys.argv[1:]:
        metadata(path)

if __name__ == "__main__":
    main()
