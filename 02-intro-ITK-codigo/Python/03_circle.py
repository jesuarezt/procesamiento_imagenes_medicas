import itk
import sys
import math

# Base image type: 2-dimensional 2-byte image
Dim = 2
TPixel = itk.US
TImage = itk.Image[TPixel, Dim]

# -------------------------------------------------------------------------
print("-------------------------")
for a in range( 0, len(sys.argv)) :
  print( sys.argv[a])
print("-------------------------")

# Check if all parameters are given
if len(sys.argv) < 11 :
  print("Usage: ", sys.argv[0], 
        " radius center_x center_y", 
        " pixel_x pixel_y", 
        " origin_x origin_y", 
        " width height", 
        " filename")
  sys.exit()

radius = float(sys.argv[ 1 ])
center_x = float(sys.argv[ 2 ])
center_y = float(sys.argv[ 3 ])
pixel_x = float(sys.argv[ 4 ])
pixel_y = float(sys.argv[ 5 ])
origin_x = float(sys.argv[ 6 ])
origin_y = float(sys.argv[ 7 ])
width = int(sys.argv[ 8 ])
height = int(sys.argv[ 9 ])
filename = sys.argv[ 10 ]
  
# Create image
image = TImage.New( )

# Image size
idx = itk.Index[Dim]()
idx = [ 0, 0 ]

size = itk.Size[Dim]()
size[0] = width
size[1] = height

region = itk.ImageRegion[Dim]()
region.SetIndex( idx )
region.SetSize( size )

image.SetLargestPossibleRegion( region )
image.SetBufferedRegion( region )
image.SetRequestedRegion( region )

# Pixel size
spacing = itk.Vector[itk.F,Dim]()
spacing[ 0 ] = pixel_x
spacing[ 1 ] = pixel_y

image.SetSpacing( spacing )

# Image origin
origin = itk.Point[itk.F,Dim]()
origin[ 0 ] = origin_x
origin[ 1 ] = origin_y

image.SetOrigin( origin )

# Allocate memory
image.Allocate( );

# Count pixels having "value"
for x in range(idx[ 0 ], idx[ 0 ] + size[ 0 ]) :
  for y in range(idx[ 1 ], idx[ 1 ] + size[ 1 ]) :
    nIdx = itk.Index[Dim]()
    nIdx[ 0 ] = x
    nIdx[ 1 ] = y

    nPnt = itk.Point[itk.F,Dim]()
    nPnt[ 0 ] = ( float( nIdx[ 0 ] ) * pixel_x ) + origin_x
    nPnt[ 1 ] = ( float( nIdx[ 1 ] ) * pixel_y ) + origin_y

    dist = math.sqrt(
      math.pow( nPnt[ 0 ] - center_x, 2 ) + 
      math.pow( nPnt[ 1 ] - center_y, 2 )
      )

    if dist <= radius :
      image.SetPixel( nIdx, itk.NumericTraits[TPixel].max( ) )
    else :
      image.SetPixel( nIdx, itk.NumericTraits[TPixel].min( ) )

# Write result
writer = itk.ImageFileWriter[TImage].New( )
writer.SetInput( image )
writer.SetFileName( filename )
writer.Update()

# eof - 03_circle.py
