# https://www.python-engineer.com/posts/image-thresholding/

import numpy as np
from PIL import Image


# threshold = 100

# this works
# img = Image.open('ranxbomberinverse.jpg') 
# # Note, if you load a color image, also apply img.convert('L')
# img = img.convert('L')
# img_np = np.array(img)
# img_np = np.where(img_np > threshold, 255, 0)

# img.putdata(img_np.flatten())

# # img.save('ranxbomberinverse_thresholded.png')
# img.show()



# img = Image.open('ranxbomberinverse.jpg') 
# img = img.convert('L')
# img.show()


# REMINDER:  #0 is black, 255 is white
# img = Image.open('ranxbomber.jpg') 
# img_np = np.array(img)
# # https://stackoverflow.com/a/21460603
# # img_np = np.clip(img_np[..., 0], 0, threshold, out=img_np[..., 0])
# # img_np = np.zeros(img_np.shape, dtype = np.uint8) #0 is black, 255 is white??
# img_np = np.full((img_np.shape[0],img_np.shape[1], img_np.shape[2]), 255, dtype = np.uint8) #0 is black, 255 is white??

# print(img_np)
# # https://stackoverflow.com/a/47598847
# # Creates PIL image
# # img = Image.fromarray(np.uint8(mat * 255) , 'L')
# img = Image.fromarray(img_np)
# img.show()

# threshold =  #(white)
# #make mask > 
# img = Image.open('ranxbomber.jpg') 
# img_np = np.array(img)
# # https://stackoverflow.com/a/21460603
# img_np = np.clip(img_np[..., 0], 0, threshold, out=img_np[..., 0])
# # grayscale, no pillow
# # https://stackoverflow.com/a/51287214

# https://stackoverflow.com/questions/51285593/converting-an-image-to-grayscale-using-numpy
img = Image.open('sportspersonMASK.jpg') 
img_np = np.array(img)
def grayConversion(image):
    grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
    gray_img = grayValue.astype(np.uint8)
    return gray_img
img_np = grayConversion(img_np)
img = Image.fromarray(img_np, 'L')
img.show()
#now to B&W from grayscale:
# https://stackoverflow.com/a/18778280
# Pixel range is 0...255, 256/2 = 128
bw = img_np.copy()

# bw[bw < 128] = 0    # Black
# bw[bw >= 128] = 255 # White
#white is background, so anything less than 255 should be set to 0 (black)
bw[bw < 255] = 0
img = Image.fromarray(bw, 'L')
img.show()





