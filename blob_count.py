import numpy as np
import matplotlib.pyplot as plt
from cv2 import *
from skimage.io import imread, imsave 
from skimage import color
from skimage.feature import blob_dog
from skimage.color import rgb2gray
from skimage.draw import circle

'''
Original example from: 
http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html#sphx-glr-auto-examples-features-detection-plot-blob-py
Difference of Gaussian (DoG) method is used to detetec the blobs. Blobs are assumed to be bright on dark.
'''
#Capture an image from webcam
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:
    imsave('barley.jpg',img)

#Read image
image = imread('barley.jpg')
#Inverse the grayscale image
image_gray = 1 - (rgb2gray(image))

# Compute the blobs and estimate size
blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
blobs_dog[:, 2] = blobs_dog[:, 2] * np.sqrt(2)

#Plot image
fig, ax = plt.subplots()
ax.imshow(image)

#Plot circles
i=0
for row in blobs_dog:
    y, x, r = row
    c = plt.Circle((x, y), r, color='lime', linewidth=2, fill=False)
    ax.add_patch(c)
    i=i+1
    ax.annotate(str(i), xy=(2, 2), xytext=(x, y), color=(0.9,0,0.9))


ax.annotate('Number of kernels = '+(str(i)), xy=(2, 2), xytext=(20, 40), color=(0.9,0,0.9))	
ax.set_axis_off()
plt.tight_layout()
plt.show()
