# OptoAnalyse to ASCII Conversion
Python script to convert OptoAnalyse binary data (.img, .imd) to ASCII

This Python script converts binary data from OptoAnalyse streak cameras to human-readable ASCII files.

## Requirements
- Python 3
Tested on Python 3.8 on Windows 10, Anaconda + Spyder 5.0.3

## Binary Data File Structure
Little Endian
Only interested in the [data] byte stream, other irrelevant bytes will not be saved in the ASCII file.

### Version 256 (up to OptoAnalyse 1.4)
Structure: [version] [????] [data start byte] [????] [ROI information] [image width] [image height] [data]
+ Version: Unsigned 16-bit integer
+ [????]: Unknown/useless data
+ [data start byte]: ith byte from start of file's byte stream where [data] starts from. This can vary; I have seen values of 192 and 194.
+ [ROI information]: Appears to be Unsigned 32-bit integer
+ Width, Height: Unsigned 16-bit integer
+ Data: Unsigned 16-bit integer

### Version 257 (OptoAnalyse 3.0 and higher)
Note: ROI and scaling information is in the .imi metadata file.
Structure: [version] [image width] [image height] [data]
+ Version: Unsigned 16-bit integer
+ Width, Height: Unsigned 16-bit integer
+ Data: Signed 32-bit integer (values multiplied by 1000)

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A copy of the GNU General Public License is included in the file LICENSE.  If not, see <https://www.gnu.org/licenses/>.
