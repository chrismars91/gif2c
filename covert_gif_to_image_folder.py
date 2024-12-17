import cv2
import os


# image_name = "dwight_office"
# image_width = 240
# image_height = None
# gif_path = "/Users/chrisbolig/Documents/code/gif_python/GIFS/IMG_5777.GIF"


def convert_gif_to_img_folder(gif_path: str, image_name=None, image_width=None, image_height=None):
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

        cv2.imwrite(f"{image_name}/{image_name}_{idx}.png", frame)
        idx += 1

    gif.release()

    print("OG Width:", width)
    print("OG Height:", height)
    print("New Width:", WIDTH)
    print("New Height:", HEIGHT)

# # create folder
# if image_name is None:
#     image_name = os.path.basename(gif_path).replace(".GIF", "_frames")
# os.makedirs(image_name, exist_ok=True)
#
# # set dims
# WIDTH = 0
# HEIGHT = 0
# cap = cv2.VideoCapture(gif_path)
# if not cap.isOpened():
#     print("Error opening video file")
#     exit()
# ret, frame = cap.read()
# cap.release()
# height, width = frame.shape[:2]
#
# if image_height is None and image_width is None:
#     WIDTH = width
#     HEIGHT = height
# else:
#     if image_height is not None and image_width is not None:
#         frame = cv2.resize(frame, (image_width, image_height))
#         WIDTH = image_width
#         HEIGHT = image_height
#
#     if image_height is not None and image_width is None:
#         WIDTH = int(width * image_height / height)
#         HEIGHT = image_height
#
#     if image_height is None and image_width is not None:
#         WIDTH = image_width
#         HEIGHT = int(height * image_width / width)
#
#
# gif = cv2.VideoCapture(gif_path)
# idx = 0
# while True:
#     ret, frame = gif.read()
#     if not ret:
#         print("Video ended.")
#         break
#
#     frame = cv2.resize(frame, (WIDTH, HEIGHT))
#
#     cv2.imwrite(f"{image_name}/{image_name}_{idx}.png", frame)
#     idx += 1
#
# gif.release()
#
# print("OG Width:", width)
# print("OG Height:", height)
# print("New Width:", WIDTH)
# print("New Height:", HEIGHT)

# length = int(gif.get(cv2.CAP_PROP_FRAME_COUNT))
# print(f"GIF has {length} frames")
# frame_number = 3
# gif.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
# ret, frame = gif.read()
# gif.release()
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# plt.imshow(frame)
