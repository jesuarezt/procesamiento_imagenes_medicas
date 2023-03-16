#/*=========================================================================
# *
# *  Copyright Insight Software Consortium
# *
# *  Licensed under the Apache License, Version 2.0 (the "License");
# *  you may not use this file except in compliance with the License.
# *  You may obtain a copy of the License at
# *
# *         http://www.apache.org/licenses/LICENSE-2.0.txt
# *
# *  Unless required by applicable law or agreed to in writing, software
# *  distributed under the License is distributed on an "AS IS" BASIS,
# *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# *  See the License for the specific language governing permissions and
# *  limitations under the License.
# *
# *=========================================================================*/

import itk
import sys

if len(sys.argv) != 3 :
  print("Usage: ", sys.argv[0], " <InputFileName> <OutputFileName>")
  sys.exit( )

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
  
Dimension = 2
PixelType = itk.F                                  
RealImageType = itk.Image[PixelType, Dimension]     
IntPixelType = itk.US                         
IntImageType = itk.Image[IntPixelType, Dimension] 
ComplexImageType = itk.Image[itk.complex[PixelType], Dimension]

ReaderType = itk.ImageFileReader[RealImageType]
reader = ReaderType.New()
reader.SetFileName( inputFileName )
reader.Update()

ForwardFFTFilterType = itk.ForwardFFTImageFilter[RealImageType, ComplexImageType]
forwardFFTFilter = ForwardFFTFilterType.New()
forwardFFTFilter.SetInput( reader.GetOutput() )
forwardFFTFilter.Update()
  
ComplexToModulusFilterType = itk.ComplexToModulusImageFilter[ComplexImageType, RealImageType]
complexToModulusFilter = ComplexToModulusFilterType.New()
complexToModulusFilter.SetInput( forwardFFTFilter.GetOutput() )
complexToModulusFilter.Update()
  
WindowingFilterType = itk.IntensityWindowingImageFilter[RealImageType, IntImageType]
windowingFilter = WindowingFilterType.New()
windowingFilter.SetInput( complexToModulusFilter.GetOutput() )
windowingFilter.SetWindowMinimum( 0 )
windowingFilter.SetWindowMaximum( 20000 )
windowingFilter.Update()

FFTShiftFilterType = itk.FFTShiftImageFilter[IntImageType, IntImageType]
fftShiftFilter = FFTShiftFilterType.New()
fftShiftFilter.SetInput( windowingFilter.GetOutput() )
fftShiftFilter.Update()
  
WriterType = itk.ImageFileWriter[IntImageType]
writer = WriterType.New()
writer.SetFileName( outputFileName )
writer.SetInput( fftShiftFilter.GetOutput() )
writer.Update()
