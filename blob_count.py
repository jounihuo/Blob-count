import sys
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from cv2 import *
from skimage.io import imread, imsave 
from skimage import color
from skimage.feature import blob_dog
from skimage.color import rgb2gray
from skimage.draw import circle
from matplotlib.figure import Figure

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Counting things")
	
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
    imsave('snap.jpg',img)

#Read image
image = imread('snap.jpg')
#Inverse the grayscale image
image_gray = 1 - (rgb2gray(image))

# Compute the blobs and estimate size
blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.5)
blobs_dog[:, 2] = blobs_dog[:, 2] * np.sqrt(2)

#Plot image
f = Figure(figsize=(6, 4), dpi=100)
ax = f.add_subplot(111)
ax.imshow(image)

#Plot circles
i=0
for row in blobs_dog:
    y, x, r = row
    c = plt.Circle((x, y), r, color='lime', linewidth=2, fill=False)
    ax.add_patch(c)
    i=i+1
    ax.annotate(str(i), xy=(2, 2), xytext=(x, y), color=(0.9,0,0.9))
ax.annotate('Number of blobs = '+(str(i)), xy=(2, 2), xytext=(20, 40), color=(0.9,0,0.9))	
ax.set_axis_off()

#Plotting with Tkinter
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def _snap():
    print('Button snap presssed')
    cam = VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:
        imsave('snap.jpg',img)
        ax.clear()
    image = imread('snap.jpg')
    ax.imshow(image)
	#Inverse the grayscale image
    image_gray = 1 - (rgb2gray(image))
    # Compute the blobs and estimate size
    blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.5)
    blobs_dog[:, 2] = blobs_dog[:, 2] * np.sqrt(2)
	#Plot circles
    i=0
    for row in blobs_dog:
        y, x, r = row
        c = plt.Circle((x, y), r, color='lime', linewidth=2, fill=False)
        ax.add_patch(c)
        i=i+1
        ax.annotate(str(i), xy=(2, 2), xytext=(x, y), color=(0.9,0,0.9))
    ax.annotate('Number of blobs = '+(str(i)), xy=(2, 2), xytext=(20, 40), color=(0.9,0,0.9))	
    ax.set_axis_off()  
    canvas.show()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button_1 = Tk.Button(master=root, text='Quit', command=_quit)
button_1.pack(side=Tk.BOTTOM)
button_2 = Tk.Button(master=root, text='Take a picture', command=_snap)
button_2.pack(side=Tk.BOTTOM)

#w2 = Tk.Scale(master=root, from_=0, to=200, orient=HORIZONTAL)
#w2.pack()

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.













