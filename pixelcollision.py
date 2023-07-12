from PIL import Image
import numpy as np
from kivy.uix.button import Button

image1 = Image.open("character_up.png")
image2 = Image.open("current_position.png")

image1_binary = image1.convert("1")  # Convert to binary (black and white)
image2_binary = image2.convert("1")

# Convert the images to NumPy arrays:
array1 = np.array(image1_binary)
array2 = np.array(image2_binary)

# Perform image subtraction:
subtraction_array = np.abs(array1 - array2)

# Check for non-zero pixels:
intersection_pixels = np.count_nonzero(subtraction_array)

# Determine if there is an intersection:
if intersection_pixels > 0:
    print("There is an intersection between the images.")
else:
    print("There is no intersection between the images.")