import cv2
import numpy as np
import os


def get_dims_from_user(image: np.ndarray, width=None, height=None):
    (orig_height, orig_width) = image.shape[:2]
    if width and height:
        new_width = width
        new_height = height
    elif width:
        aspect_ratio = orig_height / orig_width
        new_width = width
        new_height = int(new_width * aspect_ratio)
    elif height:
        aspect_ratio = orig_width / orig_height
        new_height = height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = orig_width
        new_height = orig_height
    return new_width, new_height


def get_gif_frame(gif_path: str, frame_number=0):
    cap = cv2.VideoCapture(gif_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    if not cap.isOpened():
        print("Error opening video file")
        exit()
    ret, frame = cap.read()
    cap.release()
    return frame


def image_to_rgb565_array_h(image: np.ndarray, output_file: str, save=True):
    height, width, _ = image.shape
    rgb565_array = []
    for row in image:
        for pixel in row:
            r = pixel[0] >> 3  # 5 bits for red
            g = pixel[1] >> 2  # 6 bits for green
            b = pixel[2] >> 3  # 5 bits for blue
            rgb565 = (r << 11) | (g << 5) | b  # Combine into 16-bit value
            rgb565_array.append(rgb565)
    if save:
        with open(output_file, "w") as f:
            f.write("const uint16_t imageArray[] PROGMEM = {\n")
            for i, value in enumerate(rgb565_array):
                f.write(str(value))
                if i != len(rgb565_array) - 1:
                    f.write(", ")
                if (i + 1) % width == 0:
                    f.write("\n")
            f.write("\n};\n")
        print(f"RGB565 array saved to {output_file}")
    else:
        r = "const uint16_t imageArray[] PROGMEM = {\n"
        for i, value in enumerate(rgb565_array):
            r += str(value)
            if i != len(rgb565_array) - 1:
                r += ", "
            if (i + 1) % width == 0:
                r += "\n"
        r += "\n};\n"
        return r


def image_to_rgb565_array_bin(image: np.ndarray, bin_output_file: str):
    height, width, _ = image.shape
    with open(bin_output_file, 'wb') as bin_file:
        for row in image:
            for pixel in row:
                r = pixel[0] >> 3  # 5 bits for red
                g = pixel[1] >> 2  # 6 bits for green
                b = pixel[2] >> 3  # 5 bits for blue
                rgb565 = (r << 11) | (g << 5) | b  # Combine into 16-bit value
                low_byte = rgb565 & 0xFF
                high_byte = (rgb565 >> 8) & 0xFF
                # Write to the binary file
                bin_file.write(bytes([low_byte, high_byte]))
    print(f"RGB565 array saved to {bin_output_file}")


def gif_to_bin_folder(gif_path: str, project_name=None, width=None, height=None):
    if project_name is None:
        project_name = os.path.basename(gif_path).replace(".GIF", "")
    os.makedirs(project_name, exist_ok=True)
    frame = get_gif_frame(gif_path)
    dims = get_dims_from_user(frame, width=width, height=height)
    gif = cv2.VideoCapture(gif_path)
    idx = 0
    cpp_str = ""
    str_break = 5
    while True:
        ret, frame = gif.read()
        if not ret:
            print("Video ended.")
            break
        frame = cv2.resize(frame, (dims[0], dims[1]))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cpp_str += f'''"/{project_name}/{project_name}_{idx}.bin", '''
        image_to_rgb565_array_bin(frame, f"{project_name}/{project_name}_{idx}.bin")
        idx += 1
        if idx % str_break == 0:
            cpp_str += "\n"
    gif.release()
    cpp_str = f"const char* {project_name}Frames[] = " + "{\n" + cpp_str[0:-2] + "\n};"
    text = f"width={dims[0]}\nheight={dims[1]}"
    filename = f"{project_name}/{project_name}_dims.txt"
    with open(filename, "w") as file:
        file.write(text)
    print(f"GIF as C array saved to folder {project_name}")
    print("Width:", dims[0])
    print("Height:", dims[1])
    return cpp_str


def img_to_h(image_path: str, img_name=None, width=None, height=None):
    image = cv2.imread(image_path)
    dims = get_dims_from_user(image, width=width, height=height)
    image = cv2.resize(image, (dims[0], dims[1]))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_to_rgb565_array_h(image, f"header_images/{img_name}.h")
    print("Width:", dims[0])
    print("Height:", dims[1])


# arduino_array = gif_to_bin_folder(
#     "/Users/chrisbolig/Documents/code/gif_python/GIFS/IMG_5766.GIF",
#     project_name="gr",
#     width=200
# )
#
# print(arduino_array)

img_to_h("IMAGES/ChristmasWrapping3.png", "bckgrnd", width=240)

# frameI = get_gif_frame("/Users/chrisbolig/Documents/code/gif_python/GIFS/IMG_5766.GIF")
# dimsI = get_dims_from_user(frameI, width=200)
# frameI = cv2.resize(frameI, (dims[0], dims[1]))
# image_to_rgb565_array_h(frameI, "tst.h")
# image_to_rgb565_array_bin(frameI, "tst.bin")
