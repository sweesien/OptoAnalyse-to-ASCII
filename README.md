# OptoAnalyse to ASCII Conversion
Python script to convert OptoAnalyse binary data (.img, .imd) to ASCII

This Python script converts binary data from OptoAnalyse streak cameras to human-readable ASCII files.

## Requirements
- Python 3
Tested on Python 3.8 on Windows 10, Anaconda + Spyder 5.0.3

# Binary Data File Structure
Little Endian

## Version 256 (up to OptoAnalyse 1.4)
Structure: [version] [????] [data start byte] [????] [ROI information] [image width] [image height] [data]
Version: Unsigned 16-bit integer
[????]: Unknown/useless data
[data start byte]: ith byte from start of file's byte stream where [data] starts from. This can vary; I have seen values of 192 and 194.
[ROI information]: Appears to be Unsigned 32-bit integer
Width, Height: Unsigned 16-bit integer
Data: Unsigned 16-bit integer (only interested in this byte stream)

## Version 257 (OptoAnalyse 3.0 and higher)
Note: ROI and scaling information is in the .imi metadata file.
Structure: [version] [image width] [image height] [data]

Version: Unsigned 16-bit integer
Width, Height: Unsigned 16-bit integer
Data: Signed 32-bit integer (values multiplied by 1000, only interested in this byte stream)
