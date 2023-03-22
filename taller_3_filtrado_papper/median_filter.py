import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
import itk
import os
import sys

# inspect source code
import inspect


def load_imagen_to_itk(path_):
    """ Lectura de la imagen en formato .mcc y formateando a itk format"""

    # Read the MNC file using nibabel
    mnc_img = nib.load(path_)

    # Get the image data as a numpy array
    data = mnc_img.get_fdata()

    # Convert the numpy array to an ITK object
    itk_img = itk.image_view_from_array(data)
    
    return itk_img

def plot_image(image_, k_level= 25):
    """ Ploteamos la imagen con respecto a la capa k para visualizar en python"""
    array = itk.array_view_from_image(image_)[:,:,k_level]

    # Plot the image using Matplotlib
    plt.imshow(array, cmap="gray")
    plt.show()
    return None

def median_filter(data, filter_size):
    """Algoritmo de logica de mediana con la variación del papper sin los centros
    Asumimos que la entraada es un array numpy previamente editado"""
    
    temp = list()
    # border of the region to calculate median filter
    data_final = np.zeros((len(data),len(data[0])))
    # Scroll rows
    for i in range(len(data)):
        # scroll columns
        for j in range(len(data[0])):
            # scroll acording to size circle (in this case it's a rectangule neighborhuts)
            for r in range(-1*filter_size,  filter_size+1):
                # validate if the point is not between the imagen coordinates
                if (i + r < 0) or (i+r ) > (len(data)-1):
                    pass
                #validate if the point in y coordinate
                elif (j + r  < 0) or (j+r ) > (len(data[0])-1): 
                    pass  
                else:
                    # get all elements in the border and we are including the center
                    for k in range(-1*filter_size,  filter_size+1):
                        # validate if the point is not between the imagen coordinates
                        if (i + k < 0) or (i+k ) > (len(data)-1):
                            pass
                        #validate if the point in y coordinate
                        elif (j + k  < 0) or (j+k ) > (len(data[0])-1): 
                            pass  
                        # Article no include center circle
                        elif (r==0) and (j==0):
                            pass
                        else:
                            temp.append(data[i + r ][j + k ])
            
            temp.sort()
            #print(temp)
            if len(temp) > 0:
                data_final[i][j] = temp[len(temp) // 2]
            temp = list()
    return data_final
    #return itk.image_view_from_array(data_final)

###########################################################

# read parameters

##########################################################
print("-------------------------")
for a in range( 0, len(sys.argv)) :
  print( sys.argv[a])
print("-------------------------")

# Check if all parameters are given
if len(sys.argv) != 3 :
  print("Usage: ", sys.argv[0], 
        "path input image  .mnc.gz\n", 
        "path output image .nii\n",
        " usar solo estos parametros ")
  sys.exit()

input_path = sys.argv[ 1 ]
output_path = sys.argv[ 2 ]

  

###########################################################

# corpus code

##########################################################
path_ = input_path
reader = load_imagen_to_itk(path_)
#plot_image(reader, k_level=100)

data_array = itk.GetArrayViewFromImage(reader)
data_final = np.zeros((len(data_array), len(data_array[0]), len(data_array[0, 0])))
#print(data_array.shape)
#print(data_final.shape)

for k in range(len(data_array[0,0])):
    data_final[:,:,k] = median_filter(data_array[:,:,k], filter_size=1)

median_filter_image = itk.GetImageFromArray(data_final)

#plot_image(median_filter_image,k_level=100)
output_path = output_path
itk.imwrite(median_filter_image, output_path)


## example run 
## python median_filter.py  data/t1_icbm_normal_1mm_pn0_rf20.mnc.gz  output_data/median_filer_t1_icbm_normal_1mm_pn0_rf20.nii 
## python median_filter.py  data/t1_icbm_normal_1mm_pn1_rf20.mnc.gz  output_data/median_filer_t1_icbm_normal_1mm_pn1_rf20.nii 
## python median_filter.py  data/t1_icbm_normal_1mm_pn3_rf20.mnc.gz  output_data/median_filer_t1_icbm_normal_1mm_pn3_rf20.nii 
## python median_filter.py  data/t1_icbm_normal_1mm_pn5_rf20.mnc.gz  output_data/median_filer_t1_icbm_normal_1mm_pn5_rf20.nii 
## python median_filter.py  data/t1_icbm_normal_1mm_pn7_rf20.mnc.gz  output_data/median_filer_t1_icbm_normal_1mm_pn7_rf20.nii 
## python median_filter.py  data/t1_icbm_normal_1mm_pn9_rf20.mnc.gz  output_data/median_filer_t1_icbm_normal_1mm_pn9_rf20.nii 


