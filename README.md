# OptoAnalyse to ASCII Conversion
Python script to convert OptoAnalyse binary data (.img, .imd) to ASCII

This Python script accepts binary data from OptoAnalyse streak cameras and extracts intensity data to a DataFrame and optionally output to human-readable ASCII files.

## Requirements
- Python 3
Tested on Python 3.8 on Windows 10, Anaconda + Spyder 5.0.3

## Binary Data File Structure
Little Endian
Only interested in the [data] byte stream, other irrelevant bytes will not be saved in the ASCII file.

### Version 256 (up to OptoAnalyse 1.4)
Structure: [version] [????] [data start byte] [????] [Comment length] [Comment] [ROI information] [image width] [image height] [data]
+ Version: Unsigned 16-bit integer
+ [????]: Unknown data, possibly headers
+ [data start byte]: Located at 4th byte (0-index), describes ith byte from start of file's byte stream where [data] starts from, offsetted by the preceding 4 bytes. This can vary depending on the data fields present, Unsigned 16-bit integer
+ [Comment length]: Located at 32nd byte (0-index), Unsigned 8-bit integer
+ [Comment]: 4-bit char per character
+ [ROI information]: Appears to be Unsigned 32-bit integer
+ Width, Height: Unsigned 16-bit integer
+ Data: Unsigned 16-bit integer

### Version 257 (OptoAnalyse 3.0 and higher)
Note: ROI and scaling information is in the .imi metadata file.  
Structure: [version] [image width] [image height] [data]
+ Version: Unsigned 16-bit integer
+ Width, Height: Unsigned 16-bit integer
+ Data: Signed 32-bit integer (values multiplied by 1000)

## Example
Save intensity data to DataFrame, df, and export the DataFrame as ASCII
file with extension .asc
```
>>> df = optoanalyse_to_ascii(filename,True,'asc')
Out:
      0     1     2     3     4     5     ...  1370  1371  1372  1373  1374  1375
0       22    14     5     0    27     0  ...     0    10     8     0     0    22
1        0     0     0     0     0     0  ...     8    15     6     0     0     0
2        5     5     0     0     9     0  ...     0     0     0     0     0     0
3       35    12     0     6    17    12  ...     0     0     0     0     0     0
4        6    22     0     7    31    14  ...     0     0     7    13     4     0
   ...   ...   ...   ...   ...   ...  ...   ...   ...   ...   ...   ...   ...
1019     0     9     6     0     0     1  ...     0     3    16     2     0     0
1020     0    33    20    10     0     2  ...     0    20     0     0     8     0
1021    26     8     7     0     3    10  ...     0     8     6     1     0     0
1022     0     0     0    10     0     2  ...     0    10     0     0     0     2
1023     0     0     1     0     0     4  ...     0    18     0    20    12     0

[1024 rows x 1376 columns]
```
## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A copy of the GNU General Public License is included in the file LICENSE.  If not, see <https://www.gnu.org/licenses/>.
