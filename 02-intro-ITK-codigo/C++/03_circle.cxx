#include <cmath>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>

#include <itkImage.h>
#include <itkImageFileWriter.h>

// Base image type: 2-dimensional 2-byte image
const unsigned int Dim = 2;
typedef unsigned short            TPixel;
typedef itk::Image< TPixel, Dim > TImage;

// -------------------------------------------------------------------------
int main( int argc, char* argv[] )
{
  // argc? argv?
  std::cout << "-------------------------" << std::endl;
  for( int a = 0; a < argc; a++ )
    std::cout << argv[ a ] << std::endl;
  std::cout << "-------------------------" << std::endl;

  // Check if all parameters are given
  if( argc < 11 )
  {
    std::cerr << "Usage: " << argv[ 0 ]
              << " radius center_x center_y"
              << " pixel_x pixel_y"
              << " origin_x origin_y"
              << " width height"
              << " filename"
              << std::endl;
    return( 1 );

  } // fi

  double radius = std::atof( argv[ 1 ] );
  double center_x = std::atof( argv[ 2 ] );
  double center_y = std::atof( argv[ 3 ] );
  double pixel_x = std::atof( argv[ 4 ] );
  double pixel_y = std::atof( argv[ 5 ] );
  double origin_x = std::atof( argv[ 6 ] );
  double origin_y = std::atof( argv[ 7 ] );
  unsigned int width = std::atoi( argv[ 8 ] );
  unsigned int height = std::atoi( argv[ 9 ] );
  std::string filename = argv[ 10 ];
  
  // Create image
  TImage::Pointer image = TImage::New( );

  // Image size
  TImage::IndexType idx;
  idx[ 0 ] = 0;
  idx[ 1 ] = 0;

  TImage::SizeType size;
  size[ 0 ] = width;
  size[ 1 ] = height;

  TImage::RegionType region;
  region.SetIndex( idx );
  region.SetSize( size );

  image->SetLargestPossibleRegion( region );
  image->SetBufferedRegion( region );
  image->SetRequestedRegion( region );

  // Pixel size
  TImage::SpacingType spacing;
  spacing[ 0 ] = pixel_x;
  spacing[ 1 ] = pixel_y;

  image->SetSpacing( spacing );

  // Image origin
  TImage::PointType origin;
  origin[ 0 ] = origin_x;
  origin[ 1 ] = origin_y;

  image->SetOrigin( origin );

  // Allocate memory
  image->Allocate( );

  // Count pixels having "value"
  for( unsigned long x = idx[ 0 ]; x < idx[ 0 ] + size[ 0 ]; x++ )
  {
    for( unsigned long y = idx[ 1 ]; y < idx[ 1 ] + size[ 1 ]; y++ )
    {
      TImage::IndexType nIdx;
      nIdx[ 0 ] = x;
      nIdx[ 1 ] = y;

      TImage::PointType nPnt;

      nPnt[ 0 ] = ( double( nIdx[ 0 ] ) * pixel_x ) + origin_x;
      nPnt[ 1 ] = ( double( nIdx[ 1 ] ) * pixel_y ) + origin_y;

      double dist = std::sqrt(
        std::pow( nPnt[ 0 ] - center_x, 2 ) + 
        std::pow( nPnt[ 1 ] - center_y, 2 )
        );

      if( dist <= radius )
        image->SetPixel( nIdx, std::numeric_limits< TPixel >::max( ) );
      else
        image->SetPixel( nIdx, std::numeric_limits< TPixel >::min( ) );

    } // rof

  } // rof

  // Write result
  typedef itk::ImageFileWriter< TImage > TWriter;
  TWriter::Pointer writer = TWriter::New( );
  writer->SetInput( image );
  writer->SetFileName( filename );
  try
  {
    writer->Update( );
  }
  catch( itk::ExceptionObject& err )
  {
    std::cerr << "Error: " << err << std::endl;
    return( 1 );

  } // yrt

  return( 0 );
}

// eof - src_01.cxx
