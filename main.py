import gif2c

########################################################################################
"""
    home alone you filthy animal
    Frames 16
    Width: 200
    Height: 85
"""
# arduino_array = gif2c.gif_to_bin_folder(
#     "GIFS/image0.gif",
#     project_name="hfa",
#     width=200
# )
# print(arduino_array)
########################################################################################

########################################################################################
"""
    charlie brown fail
    Frames 30
    Width: 200
    Height: 179
"""
# arduino_array = gif2c.gif_to_bin_folder(
#     "GIFS/image5.gif",
#     project_name="cbf",
#     width=200
# )
# print(arduino_array)
########################################################################################

########################################################################################
# """
#     merry chrysler
#     Frames 30
#     Width: 200
#     Height: 179
# """
# arduino_array = gif2c.gif_to_bin_folder(
#     "GIFS/image3.gif",
#     project_name="mch",
#     width=200
# )
# print(arduino_array)
########################################################################################

########################################################################################
"""
    will ferrell elf
    Frames 21
    Width: 165
    Height: 200
"""
# arduino_array = gif2c.gif_to_bin_folder(
#     "GIFS/IMG_5772.GIF",
#     project_name="wfe",
#     longest_length=200
# )
# print(arduino_array)
########################################################################################

########################################################################################
"""
    santa clause Tim Allen
    Frames 14
    Width: 182
    Height: 200
"""
# arduino_array = gif2c.gif_to_bin_folder(
#     "GIFS/IMG_5770.GIF",
#     project_name="sct",
#     longest_length=200
# )
# print(arduino_array)
########################################################################################

########################################################################################
"""
    dwight office elf
    Frames 18
    Width: 200
    Height: 166
"""
# arduino_array = gif2c.gif_to_bin_folder(
#     "GIFS/IMG_5777.GIF",
#     project_name="doe",
#     longest_length=200
# )
# print(arduino_array)
########################################################################################

########################################################################################
"""
    that's so fetch
    Frames 15
    Width: 200
    Height: 112
"""
arduino_array = gif2c.gif_to_bin_folder(
    "GIFS/IMG_5776.GIF",
    project_name="tsf",
    path_name="",
    longest_length=240,
    rbg2bgr=True  # flag to save in BGR format
)
print(arduino_array)
########################################################################################
