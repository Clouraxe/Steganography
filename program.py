from PIL import Image
import numpy as np

STRING_END = '\0'




def main():
    encrypt("you're gay", "Miku.png", "Mikuded.png")
    print(decrypt("Mikuded.png"))



def encrypt(msg, image_path, save_path):
    # Open the image
    img = Image.open(image_path)
    image_array = np.array(img)

    # Image dimensions
    height, width = image_array.shape[:2]

    msg += STRING_END
    encoded = msg.encode('utf-8')
    # encoded += STRING_END #Line Feed char (end of string)

    for i, byte in enumerate(encoded):
        bits = format(byte, '08b')
        for j, bit in enumerate(bits):
            pos = j + i*8
            pixel_x = pos % width
            pixel_y = pos // width

            pixel_val = image_array[pixel_x, pixel_y, 0]

            pixel_red_binary = format(pixel_val, '08b')

            new_pixel = pixel_red_binary[:-1] + bit

            dec_val = int(new_pixel, 2)

            image_array[pixel_x, pixel_y, 0] = dec_val

    Image.fromarray(image_array).save(save_path)


def decrypt(image_path):
    decoded = ''
    img = Image.open(image_path)
    img_arr = np.array(img)

    width, height = img_arr.shape[:2]

    pixels = width * height

    for byteGroup in range(pixels // 8):
        byte_str = ''
        for i in range(8):
            byteNum = byteGroup * 8 + i
            posx = byteNum % width
            posy = byteNum // width

            pixel = img_arr[posx, posy, 0] #get the pixel
            pixel_byte = format(pixel, '08b')
            
            lsb = pixel_byte[-1]

            byte_str += lsb
        
        letter = int(byte_str, 2).to_bytes().decode()

        if letter == STRING_END:
            break

        decoded += letter

    decoded = decoded.strip() #Remove clear char

    return decoded

if __name__=="__main__":
    main()
