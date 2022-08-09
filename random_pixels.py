# choose random pixels and change them to be black
import cv2 
import os
import numpy as np

# blur training robot images 
#image has 225 rows and 300 columns

count = 0
for image in os.listdir('/home/audrey/random_pixels_changed/test/robot/'):
    count += 1
    image_path = '/home/audrey/data_with_blurred_imgs/test/robot/' + image
    img = cv2.imread(image_path)
    new_img = img.copy()
    
    height, width = new_img.shape[:2]
    
    def change_pixels(nb_pixels):
        i = 0
        while i <= nb_pixels:
            i += 1
            row = np.random.randint(height, size=nb_pixels)
            col = np.random.randint(width, size=nb_pixels)
            new_img[row, col, :] = 0
            print(new_img)
        return new_img

    change_pixels(100)
    changed_path = os.path.abspath(f'/home/audrey/rand_test/test2_robot10{str(count)}.jpg')
    cv2.imwrite(changed_path, new_img)
    # cv2.imshow('changed image', new_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
