from PIL import Image
import numpy as np

# Open the image
img = Image.open('Miku.png')
image_array = np.array(img)

# Iterate through each pixel
height, width = image_array.shape[:2]

msg = "you're gay"
encoded = msg.encode('utf-8')

i = 0
j = 0
for byte in encoded:
    bits = format(byte, '08b')
    for bit in bits:
        pos = 8*j + i
        pixel_x = pos % width
        pixel_y = pos // width 

        pixel = image_array[pixel_x, pixel_y]

        pixel_red_binary = format(pixel[0], '08b')
        new_pixel = pixel_red_binary[:-1] + bit

        image_array[pixel_x, pixel_y, 0] = new_pixel
        j += 1
    i += 1




for y in range(height):
    for x in range(width):
        pixel_value = image_array[y, x]
        if img.mode == 'L':  # Grayscale image
            binary_value = format(pixel_value, '08b')
            print(f"Pixel at ({x}, {y}): {pixel_value} (Binary: {binary_value})")
        elif img.mode in ('RGB', 'RGBA'):  # Color image
            red, green, blue, *alpha = pixel_value  # Unpack color channels
            binary_red = format(red, '08b')
            binary_green = format(green, '08b')
            binary_blue = format(blue, '08b')
            print(f"Pixel at ({x}, {y}): RGB({red}, {green}, {blue}) (Binary: R:{binary_red}, G:{binary_green}, B:{binary_blue})")
        else:
            print(f"Pixel at ({x}, {y}): Value {pixel_value} (Mode: {img.mode}) - Handling for this mode might be needed")