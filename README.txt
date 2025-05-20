# LSB Steganography Project

## 1. Project Description
This project implements Least Significant Bit (LSB) steganography for covert communication, allowing messages to be hidden imperceptibly within digital image (PNG) and audio (WAV) files. The embedded messages can then be extracted, enabling discreet data transmission[cite: 9, 10, 12].

## 2. Setup

Prerequisite: Have python 3.x installed on your system. Python can be downloaded from https://www.python.org/downloads/

Next, install the python dependancies for the main script. This can be achieved by running the code
```
python -m pip install -r {path/to/program/folder}/requirements.txt
```

## 3. Usage
You can run the script using the following 2 commands (encoding / decoding)

Encoding:
```
python program.py <file_to_embed> <output_file_path> <message>
```

`<file_to_embed>`: path to the host file that will be encoded (Must be a .wav or a .png file)
`<output_file_path>`: path including name to the output file (the extension gets added automatically)
`<message>`: message that will get encoded in the media file

Decoding:
```
python program.py <encoded_file>
```

`<encoded_file>`: path of the file that contains a hidden message (.png or .wav)

The hidden message will be outputted onto the screen.

## Notes
There are 2 provided sample files each with their encoded counterparts that can be used for testing.