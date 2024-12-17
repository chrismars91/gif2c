import cv2
import os
import re


def image_to_rgb565_array(image, output_path_name):
    # Open the image and convert to RGB
    # image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    height, width, _ = image.shape
    print(f"Image size: {width}x{height}")

    # Convert image to a NumPy array
    pixel_data = image

    # Convert each pixel to 16-bit RGB565 format
    rgb565_array = []
    for row in pixel_data:
        for pixel in row:
            r = pixel[0] >> 3  # 5 bits for red
            g = pixel[1] >> 2  # 6 bits for green
            b = pixel[2] >> 3  # 5 bits for blue
            rgb565 = (r << 11) | (g << 5) | b  # Combine into 16-bit value
            rgb565_array.append(rgb565)

    # Save the array to a file in C-style format
    with open(f"{output_path_name}.h", "w") as f:
        f.write("const uint16_t imageArray[] PROGMEM = {\n")
        for i, value in enumerate(rgb565_array):
            f.write(f"0x{value:04X}")  # Write as hexadecimal
            if i != len(rgb565_array) - 1:
                f.write(", ")
            if (i + 1) % width == 0:  # Wrap lines for readability
                f.write("\n")
        f.write("\n};\n")

    h_to_bin(f"{output_path_name}.h", f"{output_path_name}.bin")

    # with open(f"{output_path_name}.h", "rb") as f:
    #     header_data = f.read()
    #
    # with open(f"{output_path_name}.bin", "wb") as f:
    #
    #     f.write(header_data)

    print(f"RGB565 array saved to {output_path_name}")
    os.remove(f"{output_path_name}.h")


def h_to_bin(input_header, output_bin):
    """
    Convert a .h PROGMEM array to a binary file with 16-bit values (little-endian format).

    Parameters:
        input_header (str): Path to the input .h file.
        output_bin (str): Path to the output .bin file.
    """
    with open(input_header, 'r') as infile:
        content = infile.read()

    # Use regex to extract all hex values from the array
    hex_values = re.findall(r'0x[0-9A-Fa-f]{2}', content)

    if not hex_values:
        print("No hex values found in the header file!")
        return

    # Convert the hex values to bytes and write to binary file
    with open(output_bin, 'wb') as bin_file:
        for i in range(0, len(hex_values), 2):
            # Read two consecutive bytes (little-endian)
            low_byte = int(hex_values[i], 16)
            high_byte = int(hex_values[i + 1], 16)
            bin_file.write(bytes([low_byte, high_byte]))  # Write as two bytes

    # print(f"Successfully converted to binary file: {output_bin}")


def convert_gif_to_bin_folder(gif_path: str, image_name=None, image_width=None, image_height=None):
    # create folder
    if image_name is None:
        image_name = os.path.basename(gif_path).replace(".GIF", "_frames")
    os.makedirs(image_name, exist_ok=True)

    # set dims
    WIDTH = 0
    HEIGHT = 0
    cap = cv2.VideoCapture(gif_path)
    if not cap.isOpened():
        print("Error opening video file")
        exit()
    ret, frame = cap.read()
    cap.release()
    height, width = frame.shape[:2]

    if image_height is None and image_width is None:
        WIDTH = width
        HEIGHT = height
    else:
        if image_height is not None and image_width is not None:
            WIDTH = image_width
            HEIGHT = image_height

        if image_height is not None and image_width is None:
            WIDTH = int(width * image_height / height)
            HEIGHT = image_height

        if image_height is None and image_width is not None:
            WIDTH = image_width
            HEIGHT = int(height * image_width / width)

    # fill folder
    gif = cv2.VideoCapture(gif_path)
    idx = 0
    while True:
        ret, frame = gif.read()
        if not ret:
            print("Video ended.")
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        image_to_rgb565_array(frame, f"{image_name}/{image_name}_{idx}")

        # cv2.imwrite(f"{image_name}/{image_name}_{idx}.png", frame)

        idx += 1

    gif.release()

    print("OG Width:", width)
    print("OG Height:", height)
    print("New Width:", WIDTH)
    print("New Height:", HEIGHT)


convert_gif_to_bin_folder(
    "/Users/chrisbolig/Documents/code/gif_python/GIFS/IMG_5777.GIF",
    "do",
    image_width=160
)
# # Example usage
# image_path = "/Users/chrisbolig/Documents/code/gif_python/dwight_office/dwight_office_0.png"  # Path to input image file
# output_file = "image_rgb565_array.h"  # Output file to save the C array
# image_to_rgb565_array(image_path, output_file)
