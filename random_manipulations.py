import os
import cv2
import numpy as np

count = 0
for image in os.listdir('/home/audrey/data/robot_images/'):
    count += 1
    image_path = '/home/audrey/data/robot_images/' + image
    img = cv2.imread(image_path)
    new_img = img.copy()

    height, width = new_img.shape[:2]

    def translate(new_img):
        x_direction = np.random.randint(0, height/3)
        y_direction = np.random.randint(0, width/3)
        shift = np.float32([
        [1, 0, x_direction],
        [0, 1, y_direction]
        ])
        shifted = cv2.warpAffine(new_img, shift, (new_img.shape[1], new_img.shape[0]))
        return shifted

    def rotate(new_img):
        angle = np.random.randint(low=0, high=180)
        center = (width/2, height/2)
        rotation_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
        rotated = cv2.warpAffine(src=new_img, M=rotation_matrix, dsize=(width,height))
        return rotated

    def scale(new_img):
        scale_percent = np.random.randint(100, 350)
        width = int(new_img.shape[1] * scale_percent / 100)
        height = int(new_img.shape[0] * scale_percent / 100)
        dim = (width, height)
        scaled = cv2.resize(src=new_img, dsize=dim)
        return scaled
    count2 = 0    
    for i in range(0,20):
        count2 += 1
        print(count2)
        print('yep')
        shifted = translate(img)
        rotated = rotate(shifted)
        scaled = scale(rotated)
        changed_path = os.path.abspath(f'/home/audrey/data/changed_images/{str(count2)+image}.jpg')
        cv2.imwrite(changed_path, scaled)



