from PIL import Image
import wave
import struct
import numpy as np
import sys

STRING_END = '\0'




def main():
    
    if len(sys.argv) != 4 and len(sys.argv) != 2:
        print("Usage: \nFor encoding: python program.py <file_to_encode> <output_file> <message>")
        print("For decoding: python program.py <encoded_file>")
        print("Error: please provide 1 or 3 arguments.")
        sys.exit(1) # Exit with a non-zero status to indicate an error
    
    if len(sys.argv) == 4: #for encoding
        file_to_encode = sys.argv[1]
        output_file = sys.argv[2]
        message = sys.argv[3]
        if file_to_encode.endswith('.png'):
            encrypt(message, file_to_encode, output_file)
        elif file_to_encode.endswith('.wav'):
            encryptAudio(message, file_to_encode, output_file)
        else:
            print("Unsupported file type. Please provide a .png or .wav file.")
            sys.exit(1)
    
    if len(sys.argv) == 2: #for decoding
        encoded_file = sys.argv[1]
        if encoded_file.endswith('.png'):
            print(decrypt(encoded_file))
        elif encoded_file.endswith('.wav'):
            print(decryptAudio(encoded_file))
        else:
            print("Unsupported file type. Please provide a .png or .wav file.")
            sys.exit(1)




def encrypt(msg, image_path, save_path):
    # Open the image
    img = Image.open(image_path)
    image_array = np.array(img)

    # Image dimensions
    _, width = image_array.shape[:2]

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

    return decoded

def encryptAudio(msg, wav_input, wav_output):
    with wave.open(wav_input, 'rb') as wav_file:
        params = wav_file.getparams()
        nchanl, sampwidth, _, nframes, _, _ = params

        if sampwidth != 2:
            print("Only support for 16-bit WAV")
            return

        sample_count = nframes * nchanl #total number of samples

        msg += STRING_END
        encoded = msg.encode('utf-8')

        #turn message into array of bits
        bits = []
        for byte in encoded:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        if len(encoded) > sample_count // 8:
            print("msg too big for audio file")
            return
        
        frames = wav_file.readframes(nframes)
        # Assumes 16-bit signed little-endian samples ('h')
        samples = list(struct.unpack(f"<{sample_count}h", frames))

        modified_samples = []
        bit_index = 0
        for sample in samples:
            if bit_index < len(bits):
                modified_sample = (sample & ~1) | bits[bit_index]
                modified_samples.append(modified_sample)
                bit_index += 1
            else:
                modified_samples.append(sample) # put the rest as original

        # Write the modified samples to the output file
        with wave.open(wav_output, 'wb') as wav_out:
            wav_out.setparams(params)
            packed_frames = struct.pack(f"<{sample_count}h", *modified_samples)
            wav_out.writeframes(packed_frames)

def decryptAudio(input_wav):
    with wave.open(input_wav, 'rb') as wav_file:
        nchanl, sampwidth, _, nframes, _, _ = wav_file.getparams()

        if sampwidth != 2:
            print("Only supports 16-bit WAV files.")
            return None

        total_samples = nchanl * nframes
        frames = wav_file.readframes(nframes)
        samples = struct.unpack(f"<{total_samples}h", frames)

        extracted_bits = [(sample & 1) for sample in samples] #extract bits off samples
        bit_string = "".join(map(str, extracted_bits)) #string of all lsb bits

        j = 0
        decoded = ''
        while j + 8 < len(bit_string):
            byte_str = ''
            for i in range(8):
                byte_str += bit_string[j]
                j += 1

            letter = int(byte_str, 2).to_bytes().decode()

            if letter == STRING_END:
                break

            decoded += letter

        decoded = decoded.strip() 

        return decoded
        
 

if __name__ == "__main__":
    main()
