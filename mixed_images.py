#!/usr/bin/env python

from __future__ import print_function # This is just for better "prints"
import numpy as np
import os

# Import OpenCV (library to read, write and show images)
import cv2

#takes image and background image as inputs; output is new image that combines the two (gets rid of green pixels)
def mix_images(my_image, background_image):
    # Read an image. IMAGE_PATH should be the path to your image (e.g.: /home/audrey/dataset_images/image_1.jpg)
    # NOTE: If the path of the image is wrong, the output of cv2.imread will make my_image have the value "None". 
    # The following lines raise an error if the image path doesn't exist:
    if my_image is None:
        raise AssertionError("The image path you provided doesn't exist!")
    if background_image is None:
        raise AssertionError("The new backround image path you provided doesn't exist!")

    # This image is a 3-D Numpy array already:
    print("Image type:", type(my_image)) # The output should be "numpy.ndarray"
    print("New background type", type(background_image))

    # Its shape should be (height,width,3)
    print("Image shape:",my_image.shape)
    print("Background image shape: ", background_image.shape)

    # cv2.imshow('background_image', background_image)

    new_width = 300
    new_size = (new_width, int(my_image.shape[0]/my_image.shape[1] * new_width))
    resized_image = cv2.resize(my_image, new_size)
    print(resized_image.shape)
    # new_background_image_size = (new_width, int(background_image.shape[0]/background_image.shape[1] * new_width))
    resized_background_image = cv2.resize(background_image, new_size)
    print(resized_background_image.shape)
    # Now we can show the new image onscreen:
    # cv2.imshow('resized_image',resized_image)
    # cv2.imshow('resized background image', resized_background_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ### Image modification
    # The 3rd axis on the image (of size 3) corresponds to the Blue, Green and Red values (also called "channels"), and they fall between 0 and 255. 
    # Therefore, if a pixel has a BGR value of [0,0,255], it will be saturated red. All the possible combination of values creates the whole color spectrum.
    new_image = resized_image.copy()

    new_background_image = resized_background_image.copy()

    #finds index for BGR values within specific range
    location = cv2.inRange(new_image,(10,115,25),(145,230,155))
    #adds another dimension to location
    location = np.reshape(location,(location.shape[0],location.shape[1],1))
    # within tile function, first parameter is what you want to repeat and second is saying that there are two rows, two cols and within it place the third axis (the channel --> so GRB)
    location = np.tile(location,(1,1,3))

    # shows which pixels fall within range specified above
    # cv2.imshow('location',location)
    # we then get rid of those pixels (that are within the range) --> so essentially we're getting rid of the green pixels
    mask = np.where(location)
    final_image = new_image.copy()
    # the masked pixels are now replaced by the same indexed pixels from the background image
    final_image[mask] = new_background_image[mask]
    # cv2.imshow('final image', final_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return final_image

#data augmentation (makes data set bigger by vertically flipping each original image)
count1 = 38
for robot_image in os.listdir("/home/audrey/dataset_images/robot/"):
    count1 += 1
    vertical_image_path = "/home/audrey/dataset_images/robot/" + robot_image
    image = cv2.imread(vertical_image_path)
    copy_of_image = image.copy()
    vertical_image = cv2.flip(copy_of_image, 1)
    
    vertical_image_path = os.path.abspath(f"/home/audrey/dataset_images/robot/{str(count1)}.jpg")
    cv2.imwrite(vertical_image_path, vertical_image)

count2 = 0
for my_file in os.listdir("/home/audrey/dataset_images/robot/"):
    for background_file in os.listdir("/home/audrey/dataset_images/bg/"):# make sure directory exists
        count2 += 1
        #need to do this because os.listdir returns the name of the file, not the whole filepath, which we need
        image_file_path = "/home/audrey/dataset_images/robot/" + my_file
        background_file_path = "/home/audrey/dataset_images/bg/" + background_file
        robot_image = cv2.imread(image_file_path)
        background_image = cv2.imread(background_file_path)
        # same thing for background_file
        mixed_image = mix_images(robot_image, background_image)
        #this generates names for the new files
        final_file_path = os.path.abspath(f"/home/audrey/dataset_images/mixed/{str(count2)}.jpg")
        print(final_file_path)
        #save final_image to final_file using cv2.imwrite
        cv2.imwrite(final_file_path, mixed_image)