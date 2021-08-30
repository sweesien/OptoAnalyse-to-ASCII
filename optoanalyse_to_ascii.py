# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 08:26:35 2021

@author: sweesien

"""

import pandas as pd
import numpy as np
from pathlib import Path

def optoanalyse_to_ascii(filename, savetofile = False, fileext = 'csv'):
    """
    This function takes in the full file path (directory/filename.ext) of the 
    OptoAnalyse binary file and extracts intensity data. Returns as a 
    DataFrame, optional to save as ASCII with the same filename.
    
    Note: if the ASCII file already exists, running the function again will
    overwrite it without warning.
    
    Parameters
    ----------
    filename : path (preferred) or string
        Full path of binary file, if it is passed as a string,
        it will be formatted using the pathlib module.
    savetofile : bool, optional
        If True, also save output as ASCII file. The default is False.
    fileext : string, optional
        File extension of ASCII file. The default is 'csv'.

    Raises
    ------
    FileNotFoundError
        Returns error message if file is not found.

    Returns
    -------
    ascii_df : DataFrame
        Returns the extracted intensity values as a DataFrame with shape 
        (image width * image height).
    
    Details
    -------
    Byte counting follows Python 0-indexing
    
    File structure of OptoAnalyse binary files
    BINARY FILE VERSION 256:
        Little Endian
        Binary file version in first Unsigned INT16
        Intensity data pointer in 5th byte (4th byte, 0-index), Unsigned INT16
        ROI information, Unsigned INT32
        Brightness scale, Signed INT16
        Image width and height (rows and columns), Unsigned INT16
            -> width pixels first, then vertical pixels
        Intensity data starts after image info, Unsigned INT16
        
        Previous version does not work for truncated metadata (85 vs 87).
        This updated Python script reads the byte pointer to directly obtain 
        the position of intensity data.
        Index backwards to obtain number of horizontal and vertical pixels.
    
    BINARY FILE VERSION 257:
       Little Endian
       Binary file version in first Unsigned INT16
       Image width and height (rows and columns), Unsigned INT16
           -> width pixels first, then vertical pixels
       Intensity data starts after, Signed INT32
       
    Examples
    --------
    Save intensity data to DataFrame, df, and export the DataFrame as ASCII
    file with extension .asc
    
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

    """
    if type(filename) != 'pathlib.WindowsPath':
        filename = Path(rf'{filename}')
    
    try:
        f = open(fr'{filename}','rb')
        content = f.read()
        f.close()
    except:
        raise FileNotFoundError(f'No such file or directory: "{filename}" ')
    
    # read version of OptoAnalyse binary file
    version = int.from_bytes(content[0:2], byteorder='little')
    
    ascii_data = []
    
    if version == 256:
        # ignore specified bytes (probably header)
        metadata_length_position = 4
        
        # Data is UINT16, which takes 2 bytes. Thus, extract 2 bytes worth and obtain int
        # Python3 method: (Python2 method uses struct)
        intensity_data_position = int.from_bytes(content[metadata_length_position:metadata_length_position+2],
                                                 byteorder='little')
        
        # Jump to horizontal pixel count
        byte_ptr = intensity_data_position + metadata_length_position - 4
        img_width = int.from_bytes(content[byte_ptr:byte_ptr+2], 
                                   byteorder='little')
        # Go to next UINT16
        byte_ptr = intensity_data_position + metadata_length_position - 2
        img_height = int.from_bytes(content[byte_ptr:byte_ptr+2], 
                                    byteorder='little')
        
        # Go to start of intensity data, i.e. first value of the ASCII export
        byte_ptr = intensity_data_position + metadata_length_position
        
        while byte_ptr <= len(content) - 2: # 2 because 16bit data
            ascii_data.append(int.from_bytes(content[byte_ptr:byte_ptr+2], 
                                             byteorder='little'))
            
            # Advance to the next UINT16, while loop stops when byte_ptr reaches the length of the byte stream
            byte_ptr += 2
            
        ascii_data = np.reshape(ascii_data,(img_height,img_width))
    
    elif version == 257:
        byte_ptr = 2
        img_width = int.from_bytes(content[byte_ptr:byte_ptr+2],
                                   byteorder='little')
        byte_ptr = 4
        img_height = int.from_bytes(content[byte_ptr:byte_ptr+2],
                                    byteorder='little')
        
        byte_ptr = 6
        while byte_ptr <= len(content) - 4: # 4 because 32bit data
            ascii_data.append(int.from_bytes(content[byte_ptr:byte_ptr+4],
                                                     byteorder='little', 
                                                     signed=True))
            
            # Advance to the next SINT32, while loop stops when byte_ptr reaches the length of the byte stream
            byte_ptr += 4
    
        ascii_data = np.reshape(ascii_data,(img_height,img_width))/1000
    
    ascii_df = pd.DataFrame(ascii_data)
    
    if savetofile == True:
        # Reverse find last period, assumes file extension and strip it.
        ascii_df.to_csv(rf'{filename}'.rsplit('.',1)[0] + rf'.{fileext}',
                        sep='\t', header=False, index=False)
    
    return ascii_df

if __name__ == '__main__':
    test = optoanalyse_to_ascii(filename,True)
