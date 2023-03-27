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



##### median adaptive filter algorithm 
def get_sxy( data, filter_size, i , j):
    s_xy = list()
   
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
                else:
                    s_xy.append(data[i + r ][j + k ])

    return s_xy

def conditions(data, filter_size, i , j):
    s_xy = get_sxy( data=data, filter_size=filter_size, i=i , j=j)

    

    # Adaptive conditions
    
    l11  = np.average(s_xy) - np.min(s_xy)
    l12  = np.average(s_xy) - np.max(s_xy)

    if (l11 >0) and (l12 < 0):
        #level 2
        
        gray_level = data[i,j]   
        l21  =gray_level- np.min(s_xy)
        l22  =gray_level- np.max(s_xy)  
        if (l21 >0) and (l22 < 0):
            result = gray_level
        else:
            result = round(np.average(s_xy),2)


    else: 
        if (filter_size>= len(data)) or (filter_size>= len(data[0])):
            # add condition vecause repeat level 1 is redundant
            result = 0
        else:
            result = conditions(data=data, filter_size=filter_size+1, i=i , j=j)
        
    return result


def median_adaptive_filter(data_, filter_size):
    data = data_
    
    data_final = np.zeros((len(data),len(data[0])))

     # Scroll rows
    for i in range(len(data)):
        # scroll columns
        for j in range(len(data[0])):
            
            data_final[i,j] = conditions(data=data, filter_size=filter_size, i=i , j=j)
    
    #return data_final
    return itk.image_view_from_array(data_final)


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
    data_final[:,:,k] = median_adaptive_filter(data_array[:,:,k], filter_size=1)

median_adaptive_filter_imgae = itk.GetImageFromArray(data_final)


#plot_image(median_adaptive_filter_imgae,k_level=100)
output_path = output_path
itk.imwrite(median_adaptive_filter_imgae, output_path)

#median_adaptive_filter
## example run 
## python median_adaptive_filter.py  data/t1_icbm_normal_1mm_pn0_rf20.mnc.gz  output_data/median_adaptive_filer_t1_icbm_normal_1mm_pn0_rf20.nii 
## python median_adaptive_filter.py  data/t1_icbm_normal_1mm_pn1_rf20.mnc.gz  output_data/median_adaptive_filer_t1_icbm_normal_1mm_pn1_rf20.nii 
## python median_adaptive_filter.py  data/t1_icbm_normal_1mm_pn3_rf20.mnc.gz  output_data/median_adaptive_filer_t1_icbm_normal_1mm_pn3_rf20.nii 
## python median_adaptive_filter.py  data/t1_icbm_normal_1mm_pn5_rf20.mnc.gz  output_data/median_adaptive_filer_t1_icbm_normal_1mm_pn5_rf20.nii 
## python median_adaptive_filter.py  data/t1_icbm_normal_1mm_pn7_rf20.mnc.gz  output_data/median_adaptive_filer_t1_icbm_normal_1mm_pn7_rf20.nii 
## python median_adaptive_filter.py  data/t1_icbm_normal_1mm_pn9_rf20.mnc.gz  output_data/median_adaptive_filer_t1_icbm_normal_1mm_pn9_rf20.nii 





