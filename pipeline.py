import aug_util as aug
import wv_util as wv
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
from tqdm import tqdm
# %matplotlib inline


class Outline_boxes:

    def __init__(self, image_number_as_int):

        #Take in the image number and convert to readable tif files
        self.image_number = str(image_number_as_int)
        self.file_name = '../../val_images/'+self.image_number+'.tif'
        self.chip_name = self.image_number+'.tif'
        self.arr = wv.get_image(self.file_name)


        #Loading our labels to use later from geojson
        self._load_labels()

        #Load the class number -> class string label map
        self._make_labels()
        #Chip images
        self._chip_images()


    def _load_labels(self):
        #Loading our labels to use later from geojson
        self.coords, self.chips, self.classes = wv.get_labels('../../xView_train.geojson')

        #We only want coordinates and classes that are within our chip
        self.coords = self.coords[self.chips==self.chip_name]
        self.classes = self.classes[self.chips==self.chip_name].astype(np.int64)


    #Load the class number -> class string label map
    def _make_labels(self):
        self.labels = {}
        with open('xview_class_labels.txt') as f:
            for row in csv.reader(f):
                self.labels[int(row[0].split(":")[0])] = row[0].split(":")[1]

    #If you want to show the image
    def load_image(self):
        plt.figure(figsize=(10,10))
        plt.axis('on')
        plt.imshow(self.arr)

    def show_classes(self):
        #We can find which classes are present in this image
        print([self.labels[i] for i in np.unique(self.classes)])


    def _chip_images(self):
        #We can chip the image into 500x500 chips and print amount of chips
        self.c_img, self.c_box, self.c_cls = wv.chip_image(img = self.arr, coords= self.coords, classes=self.classes, shape=(500,500))
        self.num_chips = self.c_img.shape[0]
        print("Num Chips: %d" % self.c_img.shape[0])

    def plot_chips(self,num):
        #We can plot some of the chips
        fig,ax = plt.subplots(3)
        fig.set_figheight(5)
        fig.set_figwidth(5)

        sqrt_num = num ** (1/2)

        for k in range(num):
            plt.subplot(sqrt_num,sqrt_num,k+1)
            plt.axis('off')
            plt.imshow(self.c_img[np.random.choice(range(self.c_img.shape[0]))])

        plt.show()


    def plot_chips_and_label(self,chip_number,labels):
        #We can visualize the chips with their labels
        # ind = np.random.choice(range(c_img.shape[0]))
        ind = chip_number
        labelled = aug.draw_bboxes(self.c_img[ind],self.c_box[ind],self.labels)
        plt.figure(figsize=(5,5))
        plt.axis('off')
        plt.imshow(labelled)

    def shift_chips(self, chip_number):
        #We can shift the chips
        i1,b1 = aug.shift_image(self.c_img[ind],self.c_box[ind])
        a1 = aug.draw_bboxes(i1,b1,self.labels)
        plt.figure(figsize=(5,5))
        plt.axis('off')
        plt.imshow(a1)


    def rotate_chips(self, chip_number):
        #We can rotate the chips
        center = (int(self.c_img[ind].shape[0]/2),int(self.c_img[ind].shape[1]/2))
        i2,b2 = aug.rotate_image_and_boxes(self.c_img[ind],10, center, self.c_box[ind])
        a2 = aug.draw_bboxes(i2,b2,self.labels)
        plt.figure(figsize=(5,5))
        plt.axis('off')
        plt.imshow(a2)


    def plot_all_chips_and_label(self):
        for i in range(self.c_img.shape[0]):
            #We can visualize the chips with their labels
            ind = i
            labelled = aug.draw_bboxes(self.c_img[ind],self.c_box[ind],self.labels)
            plt.figure(figsize=(5,5))
            plt.axis('off')
            plt.imshow(labelled)
