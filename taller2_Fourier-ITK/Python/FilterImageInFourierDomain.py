#*=========================================================================
#*
#*  Copyright Insight Software Consortium
#*
#*  Licensed under the Apache License, Version 2.0 (the "License");
#*  you may not use this file except in compliance with the License.
#*  You may obtain a copy of the License at
#*
#*         http://www.apache.org/licenses/LICENSE-2.0.txt
#*
#*  Unless required by applicable law or agreed to in writing, software
#*  distributed under the License is distributed on an "AS IS" BASIS,
#*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#*  See the License for the specific language governing permissions and
#*  limitations under the License.
#*
#*=========================================================================*/

import itk
import sys

if len(sys.argv) != 4 :
  print("Usage: ", sys.argv[0], "<InputFileName> <MaskFileName> <OutputFileName>")
  sys.exit( )
  
inputFileName = sys.argv[1]
maskFileName = sys.argv[2]
outputFileName = sys.argv[3]
  
Dimension = 2
PixelType = itk.F
RealImageType = itk.Image[PixelType, Dimension]
CharPixelType = itk.UC
CharImageType = itk.Image[CharPixelType, Dimension]
ComplexImageType = itk.Image[itk.complex[PixelType], Dimension]
  
inputReader = itk.ImageFileReader[RealImageType].New( )
inputReader.SetFileName( inputFileName )
inputReader.Update()
  
maskReader = itk.ImageFileReader[CharImageType].New( )
maskReader.SetFileName( maskFileName )
maskReader.Update()

ForwardFFTFilterType = itk.ForwardFFTImageFilter[RealImageType, ComplexImageType]
forwardFFTFilter = ForwardFFTFilterType.New( )
forwardFFTFilter.SetInput( inputReader.GetOutput() )
forwardFFTFilter.UpdateOutputInformation()

FFTShiftFilterType = itk.FFTShiftImageFilter[CharImageType, CharImageType]
fftShiftFilter = FFTShiftFilterType.New( )
fftShiftFilter.SetInput( maskReader.GetOutput() )
fftShiftFilter.Update()
    
MaskFilterType = itk.MaskImageFilter[ComplexImageType, CharImageType, ComplexImageType] 
maskFilter = MaskFilterType.New( )
maskFilter.SetInput1( forwardFFTFilter.GetOutput() )
maskFilter.SetInput2( fftShiftFilter.GetOutput() )
maskFilter.Update()

InverseFilterType = itk.InverseFFTImageFilter[ComplexImageType, RealImageType]
inverseFFTFilter = InverseFilterType.New()
inverseFFTFilter.SetInput( maskFilter.GetOutput() )
inverseFFTFilter.Update()
  
MinMaxFilterType = itk.MinimumMaximumImageFilter[RealImageType]
minMaxFilter = MinMaxFilterType.New()
minMaxFilter.SetInput( inverseFFTFilter.GetOutput() )
minMaxFilter.Update()

min_int = minMaxFilter.GetMinimum()
max_int = minMaxFilter.GetMaximum()
int_range = max_int - min_int

IntShiftFilterType = itk.ShiftScaleImageFilter[RealImageType, RealImageType]
intShiftFilter = IntShiftFilterType.New()
intShiftFilter.SetInput( inverseFFTFilter.GetOutput() )
intShiftFilter.SetShift( - min_int )
intShiftFilter.Update()

RescaleFilterType = itk.RescaleIntensityImageFilter[RealImageType, RealImageType]
rescaleFilter = RescaleFilterType.New( )
if int_range > 255 and min_int < 0 :
  rescaleFilter.SetInput( intShiftFilter.GetOutput() )
else :
  rescaleFilter.SetInput( inverseFFTFilter.GetOutput() )
rescaleFilter.SetOutputMinimum( 0 )
rescaleFilter.SetOutputMaximum( 255 )
rescaleFilter.Update()

CastFilterType = itk.CastImageFilter[RealImageType, CharImageType]
castFilter = CastFilterType.New( )
if int_range > 255 :
  castFilter.SetInput( rescaleFilter.GetOutput() )
elif min_int < 0 :
  castFilter.SetInput( intShiftFilter.GetOutput() )
else :
  castFilter.SetInput( inverseFFTFilter.GetOutput() )
castFilter.Update()

WriterType = itk.ImageFileWriter[CharImageType]
writer = WriterType.New( )
writer.SetFileName( outputFileName )
writer.SetInput( castFilter.GetOutput() )
writer.Update()
