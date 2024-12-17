import cv2


def image_to_rgb565_array(image_path, output_file):
    # Open the image and convert to RGB
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
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
    with open(output_file, "w") as f:
        f.write("const uint16_t imageArray[] PROGMEM = {\n")
        for i, value in enumerate(rgb565_array):
            f.write(str(value))  # Write as hexadecimal
            # f.write(f"0x{value:04X}")  # Write as hexadecimal
            if i != len(rgb565_array) - 1:
                f.write(", ")
            if (i + 1) % width == 0:  # Wrap lines for readability
                f.write("\n")
        f.write("\n};\n")
    print(f"RGB565 array saved to {output_file}")


# Example usage
image_path = "/Users/chrisbolig/Documents/code/gif_python/dwight_office/dwight_office_0.png"  # Path to input image file
output_file = "image_rgb565_array.h"  # Output file to save the C array
image_to_rgb565_array(image_path, output_file)
