#include <iostream>

#include <itkImage.h>
#include <itkImageFileReader.h>
#include <itkImageFileWriter.h>

// -------------------------------------------------------------------------
// Base image
const unsigned int Dimension = 2;
typedef unsigned char TPixel;  // [0,255]
/*
  typedef unsigned short TPixel; // [0,65535]
  typedef unsigned int TPixel;   // [0,4294967295]
  typedef unsigned long TPixel;  // [0,18446744073709551615]
  typedef char TPixel;           // [-128,127]
  typedef short TPixel;          // [-32768, 32767]
  typedef int TPixel;            // [-2147483648, 2147483647]
  typedef long TPixel;           // [-9223372036854775808, 9223372036854775807]
  typedef float TPixel;          // [1.17549e-38, 3.40282e+38]
  typedef double TPixel;         // [2.22507e-308, 1.79769e+308]
*/
typedef itk::Image< TPixel, Dimension > TImage;

// Image IO classes
typedef itk::ImageFileReader< TImage > TReader;
typedef itk::ImageFileWriter< TImage > TWriter;

// -------------------------------------------------------------------------
int main( int argc, char* argv[] )
{
  if( argc < 3 )
  {
    std::cerr << "Usage: " << argv[ 0 ] << " input output" << std::endl;
    return( 1 );

  } // fi

  TReader::Pointer reader = TReader::New( );
  reader->SetFileName( argv[ 1 ] );

  TWriter::Pointer writer = TWriter::New( );
  writer->SetFileName( argv[ 2 ] );
  writer->SetInput( reader->GetOutput( ) );

  try
  {
    writer->Update( );
  }
  catch( itk::ExceptionObject& err )
  {
    std::cerr << "An error has occurred: " << err << std::endl;
    return( 1 );

  } // yrt
  return( 0 );
}

// eof - 01_io.cxx
