#numpy
import numpy as np
#pandas
import pandas as pd
#skimage
import skimage.io as io
from skimage import data
from skimage.filters import sobel 
from skimage.morphology import watershed
from skimage import feature
from skimage.color import rgb2gray
from skimage.feature import corner_harris,corner_peaks
from skimage.exposure import equalize_hist
from skimage import measure
from skimage.draw import ellipse
from skimage.measure import label, regionprops
from skimage.transform import rotate
from skimage.feature import corner_orientations
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb
#matplotlib
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
#scipy
from scipy import ndimage as ndi
from scipy import ndimage
#other
import pylab
import math
from os import listdir
from os.path import isfile, join
import cv2
from ipywidgets import IntProgress


def line_width(mypath,savepath, thresh, pixtomm,background):
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    images = np.empty(len(onlyfiles), dtype=object)
    names = np.empty(len(onlyfiles), dtype=object)
    tosave = []
    output_test =[]    
    
    for n in range(0, len(onlyfiles)):
        images[n] = cv2.imread( join(mypath,onlyfiles[n]),cv2.IMREAD_GRAYSCALE )
        names[n]= (onlyfiles[n])
    img = np.empty(len(images), dtype=object)
    
    max_count=100
    tot_sum_progress = len(img)
    PROGRESSBAR = IntProgress(min=0, max=max_count,description='Progress')
    PROGRESSBAR.bar_style='info'
    display(PROGRESSBAR) # display the bar
    
    output_test=[]#numpy.empty(len(images),dtype=object)
    df= pd.DataFrame()
    for n in range(0,len(img)):
        PROGRESSBAR.value =  int(n/tot_sum_progress*100) # signal to increment the progress bar
        plt.ioff()
        img_grey = images[n]
        # threshold the image
        img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
        if background == 'Light':
            img_binary = np.invert(img_binary)
        name = names[n]
        ret, labels = cv2.connectedComponents(img_binary)
        label_hue = np.uint8(170 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        color_img = cv2.merge([label_hue, blank_ch, blank_ch])
        color_img = cv2.cvtColor(color_img, cv2.COLOR_HSV2BGR)
        #labeled_img =(labels == 1).astype("uint8") * 255#cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        color_img[label_hue == 0] = 0
        #color_img[label_hue==0] = 0
        plt.figure(figsize=(10, 10))
        plt.imshow(color_img)
        plt.title('Objects counted:'+ str(ret-1))
        plt.savefig(savepath+'Linecount_'+names[n]);
        #plt.show()

        #ret, labels = cv2.connectedComponents(img_binary)
        maxed = ret
        label_hue = np.uint8(180 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        for i in range(1,maxed):
            # select line to analyze
            labeled_img =(labels == i).astype("uint8") * 255
            #set column title number for later
            column_title =i
            #io.imshow(labeled_img)
            test = labeled_img
            A,B=test.shape #A= width(or number of rows), B= length (or number of columns )
            #print(A,B)
            results_1 = []
            for x in range(A):
                column = test[x-1,:]
                column_title=i
                m = np.where(column[:-1] != column[1:])[0]
                l = np.unique(m)
                odd = l[::2]
                even = l[1::2]
                C=odd.shape[0]
                D = even.shape[0]
                if C<1:
                    continue
                    print('test for C',C)
                for z in range(0,C):
                    if D<1:
                        x=0
                    else:
                        x= abs(even[z-1]-odd[z-1])
                        results_1.append(abs(x))
                results = np.asarray(results_1)
                column = "{}_line{}".format(name,column_title)
            df1 = pd.DataFrame({column:results}) 
            if n == (tot_sum_progress-1):
                PROGRESSBAR.value =  100 # signal to increment the progress bar
            if column_title==0 & n==0:
                df = df1
                #print(0)
            else:
                df = pd.concat([df,df1], ignore_index=False, axis=1)
        df= df.div(pixtomm)
        df.to_csv(savepath+'Linecount_saved_output.csv')