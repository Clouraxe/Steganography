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
    j = 0 # keeps track of bit number
    for i, byte in enumerate(encoded): #for byte number i of utf encoding
        bits = format(byte, '08b')
        for bit in bits: #for bit number j of byte
            pos = j // 3  # same pos for each 3 bits, goes by 8 bits per byte
            chan = j % 3       # channel to place the bit in
            pixel_x = pos % width  #where in x
            pixel_y = pos // width #where in y

            pixel_val = image_array[pixel_x, pixel_y, chan] #value of pixel in decimal

            pixel_binary = format(pixel_val, '08b')     #pixel val in bits

            new_pixel = pixel_binary[:-1] + bit       #edit the last bit

            dec_val = int(new_pixel, 2)                 # turn back to decimal

            image_array[pixel_x, pixel_y, chan] = dec_val  # set the new value
            j += 1 #next bit
    print("encoded " + str(j) + " bits successfully")
    Image.fromarray(image_array).save(save_path)


def decrypt(image_path):
    decoded = ''
    img = Image.open(image_path)
    img_arr = np.array(img)

    width, height = img_arr.shape[:2]

    pixels = width * height

    j = 0 #bit index

    while pixels * 3 > j + 8:  #while there's room for another byte (utf character)
        byte_str = ''
        for i in range(8):
            pos = j // 3              #pix number
            chan = j % 3              #channel
            posx = pos % width
            posy = pos // width

            pixel = img_arr[posx, posy, chan] #get the pixel
            pixel_byte = format(pixel, '08b')

            lsb = pixel_byte[-1]
            byte_str += lsb

            j += 1

        letter = int(byte_str, 2).to_bytes().decode()

        if letter == STRING_END:
            break

        decoded += letter

    decoded = decoded.strip() #Remove clear char
    print("decoded " + str(j) + " bits successfully")

    return decoded

if __name__=="__main__":
    main()
