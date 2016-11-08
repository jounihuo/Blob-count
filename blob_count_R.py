import sys
#For plotting
# matplotlib
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
#For math and image analysis
# numpy
# opencv
# scikit-image
import numpy as np
from cv2 import *
from skimage.io import imread, imsave 
from skimage import color
from skimage.feature import blob_dog
from skimage.color import rgb2gray
from skimage.draw import circle
#For UI
# Tkinter
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

'''
Original example from: 
http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html#sphx-glr-auto-examples-features-detection-plot-blob-py
Difference of Gaussian (DoG) method is used to detetec the blobs. Blobs are assumed to be bright on dark.
'''

#Initialise the Tkinter
root = Tk.Tk()
root.wm_title("Counting things")

#Capture an image from webcam
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:
    imsave('snap.jpg',img)

#Read image
image = imread('snap.jpg')
#Plot image
f = Figure(figsize=(6, 3), dpi=100)
ax = f.add_subplot(111)
ax.imshow(image)
ax.set_axis_off()

#UI with Tkinter
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

#Take a picture and count the blobs
def _snap():
    cam = VideoCapture(2)   # 0 -> index of camera
    s, img = cam.read()
    if s:
        imsave('snap.jpg',img)
        ax.clear()
    image = imread('snap.jpg')
    ax.imshow(image)
	#Inverse the grayscale image
    #image_gray = rgb2gray(image)
    image_gray = cvtColor(image, COLOR_BGR2GRAY)
    image_gray = 1 - (rgb2gray(image))
    #Compute the blobs and estimate size
    blobs_dog = blob_dog(image_gray, max_sigma=w2.get()/1., threshold=w.get()/200.)
    blobs_dog[:, 2] = blobs_dog[:, 2] * np.sqrt(2)
	#Plot circles
    i=0
    for row in blobs_dog:
        y, x, r = row
        c = plt.Circle((x, y), r, color='lime', linewidth=2, fill=False)
        ax.add_patch(c)
        i=i+1
        ax.annotate(str(i), xy=(2, 2), xytext=(x, y), color=(0.9,0,0.9))
    ax.annotate('Number of blobs = '+(str(i)), xy=(2, 2), xytext=(20, 40), color=(0.1,0.1,0.1), backgroundcolor='white')	
    ax.set_axis_off()  
    canvas.show()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

#Buttons for the interface
button_1 = Tk.Button(master=root, text='Quit', command=_quit)
button_1.pack(side=Tk.BOTTOM)
button_2 = Tk.Button(master=root, text='Take a picture', command=_snap)
button_2.pack(side=Tk.BOTTOM)
#Slider for threshold
w = Tk.Scale(master=root, from_=1, to=100, label='Thershold')
w.pack(side=Tk.BOTTOM)
w.set(34)
w2 = Tk.Scale(master=root, from_=1, to=50, label='sigma')
w2.pack(side=Tk.BOTTOM)
w2.set(7)

Tk.mainloop()