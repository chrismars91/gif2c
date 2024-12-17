import cv2
import os


def image_to_c_bin(image, bin_output_file):
    """
    Converts an image to a 16-bit RGB565 little-endian a binary file.

    Parameters:
        image (np:array): Image array.
        bin_output_file (str): Path to the output binary file.
    """
    # Open the image and convert it to RGB
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    height, width, _ = image.shape
    print(f"Image size: {width}x{height}")

    # Prepare binary file and C file
    with open(bin_output_file, 'wb') as bin_file:
        # Write the header of the C array

        # Process each pixel
        for row in image:
            for pixel in row:
                r = pixel[0] >> 3  # 5 bits for red
                g = pixel[1] >> 2  # 6 bits for green
                b = pixel[2] >> 3  # 5 bits for blue
                rgb565 = (r << 11) | (g << 5) | b  # Combine into 16-bit value

                print(rgb565)

                # Split into little-endian bytes
                low_byte = rgb565 & 0xFF
                high_byte = (rgb565 >> 8) & 0xFF

                # Write to the binary file
                bin_file.write(bytes([low_byte, high_byte]))

    print(f"Binary file saved to: {bin_output_file}")


def gif_to_c_bin(gif_path: str, image_name=None, image_width=None, image_height=None):
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
        image_to_c_bin(frame, f"{image_name}/{image_name}_{idx}.bin")

        # cv2.imwrite(f"{image_name}/{image_name}_{idx}.png", frame)
        idx += 1

    gif.release()

    print("OG Width:", width)
    print("OG Height:", height)
    print("New Width:", WIDTH)
    print("New Height:", HEIGHT)


# # Example usage
# image_path = "/Users/chrisbolig/Documents/code/gif_python/dwight_office/dwight_office_0.png"  # Input image file
# c_output_file = "output_image.h"  # Output C header file
# bin_output_file = "output_image.bin"  # Output binary file
# image_to_c_bin(image_path, bin_output_file)


gif_to_c_bin(
    "/Users/chrisbolig/Documents/code/gif_python/GIFS/IMG_5777.GIF",
    "do",
    image_width=160
)
