from PIL import Image, ImageOps
import os
import sys

# Assume max monitor, and use 81 x 80 (162 x 80, but characters are twice as tall as they are wide)

# Supported CC colors table
COLORS_RAW = {
    0xF0F0F0: "0",
    0xF2B233: "1",
    0xE57FD8: "2",
    0x99B2F2: "3",
    0xDEDE6C: "4",
    0x7FCC19: "5",
    0xF2B2CC: "6",
    0x4C4C4C: "7",
    0x999999: "8",
    0x4C99B2: "9",
    0xB266E5: "a",
    0x3366CC: "b",
    0x7F664C: "c",
    0x57A64E: "d",
    0xCC4C4C: "e",
    0x191919: "f"
}

COLORS = {}

for col in COLORS_RAW.keys():
    b = col & 255
    g = (col >> 8) & 255
    r = (col >> 16) & 255
    COLORS[(r, g, b)] = COLORS_RAW[col]


def ask_image(image=None):
    while True:
        if not image:
            image = input("Please enter an image name or path: ")
        try:
            im = Image.open(image)
            if im.size[0] != 81 or im.size[1] != 80:
                raise Exception("Image must be 81x80!")
            else:
                name = os.path.split(os.path.splitext(im.filename)[0])[1]
                im = ImageOps.exif_transpose(im)
                im = im.rotate(90)  # IDK, it just works lol
                im = ImageOps.flip(im)  # See above comment xD
                return im, name
        except OSError:
            print("File does not exist or could not be opened!")


def get_closest_color(pixel):
    max_val = 0xFFFFFF + 1
    current = None
    for col in COLORS.keys():
        res = abs(col[0] - pixel[0]) + abs(col[1] - pixel[1]) + abs(col[2] - pixel[2])
        if res < max_val:
            current = COLORS[col]
            max_val = res
    return current


def assemble_image(image):
    pixels = image.load()
    final = ""
    for i in range(81):
        for j in range(80):
            final += get_closest_color(pixels[i, j])
            final += get_closest_color(pixels[i, j])
        if i != 80:
            final += "\n"
    return final


def assemble_and_write(image, name):
    out = assemble_image(image)
    with open(name + ".nfp", "w") as f:
        f.write(out)
    print("Wrote image " + name + " to disk!")


def main():
    if len(sys.argv) <= 1:
        image, name = ask_image()
        assemble_and_write(image, name)

    elif sys.argv[1] in ["-a", "--all", "all"]:
        for f in os.listdir():
            if f.endswith(".png"):
                image, name = ask_image(f)
                assemble_and_write(image, name)


if __name__ == "__main__":
    main()