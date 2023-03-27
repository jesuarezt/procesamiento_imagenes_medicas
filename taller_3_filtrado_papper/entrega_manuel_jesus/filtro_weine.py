#!/usr/bin/env python
# coding: utf-8

# In[2]:


import itk
import numpy as np

def WeinAd(image, kernel_size):
    
    """Programa que aplica  mean and standard deviation normalization a imagen .nii"""
   
    # Padding a la imagen
    image_padded = np.pad(image, [(kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0,0)], mode='constant')
    
    # Imagen de salida
    filtered_image = np.zeros_like(image)
    
    # Recorrido de los pixels
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            
            # Establece el centro del Kernel
            patch = image_padded[i:i+kernel_size, j:j+kernel_size, :]
            
            # Calcula Media y Desv Standard
            patch_mean = np.mean(patch)
            patch_std = np.std(patch)
            
            # Normaliza el proceso del kernel
            patch_norm = (patch - patch_mean) / patch_std
            
            # Aplica el Kernel a cada pixel en la imagen de salida
            filtered_image[i, j, :] = patch_norm[kernel_size//2, kernel_size//2, :]
    
    return filtered_image

# Imagen de entrada
input_path = input("Nombre de la Imagen a tratar en formato NIfTI: ")

# Load the input image
input_image = itk.imread(input_path)

# Get the kernel size from the user
kernel_size = int(input("Tamaño deseado del Kernel: "))

# Get the numpy array from the input image
img_data = itk.array_view_from_image(input_image)

# Apply the mean and standard deviation filter
filtered_data = WeinAd(img_data, kernel_size)

# Get the output file name from the user
output_path = input("Imagen de salida por favor agregar extensión +.nii: ")

# Create an ITK image from the filtered numpy array
filtered_image = itk.image_from_array(filtered_data)

# Copy the metadata from the input image to the output image
filtered_image.CopyInformation(input_image)

# Save the filtered image to a file
itk.imwrite(filtered_image, output_path)


# In[ ]:




