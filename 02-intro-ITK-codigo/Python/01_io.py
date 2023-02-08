import itk
import sys
import os

print(os.getcwd())

# -------------------------------------------------------------------------
# Base image
Dimension = 2
TPixel = itk.UC  # [0,255]

# TPixel = itk.US  # [0,65535]
# TPixel = itk.UI  # [0,4294967295]
# TPixel = itk.UL  # [0,18446744073709551615]
# TPixel = itk.C   # [-128,127]
# TPixel = itk.S   # [-32768, 32767]
# TPixel = itk.I   # [-2147483648, 2147483647]
# TPixel = itk.L   # [-9223372036854775808, 9223372036854775807]
# TPixel = itk.F   # [1.17549e-38, 3.40282e+38]
# TPixel = itk.D   # [2.22507e-308, 1.79769e+308]

TImage = itk.Image[TPixel, Dimension]

# -------------------------------------------------------------------------
if len(sys.argv) < 3 :
    print("Usage: " , sys.argv[0], " input output")
    sys.exit( )

reader = itk.ImageFileReader[TImage].New( )
reader.SetFileName( sys.argv[1] )

writer = itk.ImageFileWriter[TImage].New( )
writer.SetFileName( sys.argv[2] )
writer.SetInput( reader.GetOutput( ) )
writer.Update()

# eof - 01_io.py
