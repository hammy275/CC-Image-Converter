import pygame
import os
import sys
from time import sleep


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


# Flipped version of COLORS_RAW
COLORS = {}

for col in COLORS_RAW.keys():
    COLORS[COLORS_RAW[col]] = col


def draw_image(screen, data_lines):
    for i in range(640):
        for j in range(324):
            screen.set_at((i, j), COLORS[data_lines[int(j / 4)][int(i / 4)]])
    pygame.display.flip()


def ask_for_image():
    path = None
    while path is None or (not os.path.isfile(path) and not os.path.isfile(path + ".nfp")):
        if path is not None:
            print("Path does not exist!")
        path = input("Please enter the path to a .nfp file: ")
    if not os.path.isfile(path):
        path = path + ".nfp"
    return path


def get_paths(mode):
    if mode == "single":
        paths = [ask_for_image()]
    elif mode.startswith("video"):
        paths_raw = os.listdir()
        paths = []
        for path in paths_raw:
            if path.endswith(".nfp"):
                paths.append(path)
    elif mode == "arg":
        paths = [sys.argv[1]]
    else:
        print("Bad option!")
        sys.exit(1)
    return paths


def print_video_help():
    instructions = """Key Functions:
    SPACE - Play/pause
    LEFT - Back 1 frame
    RIGHT - Forward 1 frame
    s - Return to beginning of video
    """
    print(instructions)


def main(mode):
    paths = get_paths(mode)

    data_lines = []
    for path in paths:
        with open(path, "r") as f:
            data_lines.append(f.readlines())

    pygame.init()
    screen = pygame.display.set_mode((640, 324))

    # Video Player Status
    paused = False
    frame_num = 0

    if mode == "video":
        print_video_help()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_LEFT:
                    if frame_num > 1:
                        frame_num -= 1
                        draw_image(screen, data_lines[frame_num])
                elif event.key == pygame.K_RIGHT:
                    if frame_num < len(data_lines) - 1:
                        frame_num += 1
                        draw_image(screen, data_lines[frame_num])
                elif event.key == pygame.K_s:
                    frame_num = 0
                    draw_image(screen, data_lines[frame_num])
        if frame_num >= len(data_lines):
            paused = True
        elif not paused:
            draw_image(screen, data_lines[frame_num])
            frame_num += 1
        if mode == "video_60fps":
            sleep(1/60)
        else:
            sleep(0.1)


if __name__ == "__main__":
    """
    Modes:
    
    single - Asks for, then displays a single image
    video - Plays back a video of .nfp files like how videoplayer.lua would
    video_60fps* - Plays back a video assuming each .nfp is a frame in a 60fps video
    arg** - Opens sys.argv[1] as a .nfp. Used so someone can drag a file onto this .py to open it.
    
    *: Currently hidden from the input() prompt
    **: Impossible to enter and hidden from the user
    """
    if len(sys.argv) > 1:
        main("arg")
    ans = None
    answers = ["single", "video", "video_60fps"]
    while ans is None or ans not in answers:
        ans = input("Would you like to view a single image, or play them back as video? [single/video]: ")
    main(ans)
