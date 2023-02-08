import itk
import sys

# -------------------------------------------------------------------------
# Base image
Dimension = 3 
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
# Read series
reader = itk.ImageSeriesReader[TImage].New( )
for i in range(1, len(sys.argv) - 1) :
    reader.AddFileName( sys.argv[i] )

# Write single image
writer = itk.ImageFileWriter[TImage].New( )
writer.SetInput( reader.GetOutput( ) )
writer.SetFileName( sys.argv[ len(sys.argv) - 1 ] )
writer.Update()

# eof - 02_multi_io.py
