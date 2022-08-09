import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

lower_bound = np.array([10,115,25])
upper_bound = np.array([145,230,155])

def get_rgb_values():
    count = 0
    while count < 5:
        for image in os.listdir('/home/audrey/data_for_project/robot_images/'):
            count += 1
            image_file_path = '/home/audrey/data_for_project/robot_images/' + image
            read_image = cv2.imread(image_file_path)
            for pixel in cv2.inRange(read_image,lower_bound, upper_bound):
                print(read_image)
                blue, green, red = read_image[:,:,2], read_image[:,:,1], read_image[:,:,0]
                return blue, green, red

blue, green, red = get_rgb_values()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(blue, green, red, c = 'g', marker='o')

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for m, zlow, zhigh in [('o', 25, 25), ('^', 155, 155)]:
    # blue
    xs = (10, 145)
    # green 
    ys = (115, 230)
    # red
    zs = (zlow, zhigh)
    ax.scatter(xs, ys, zs, marker=m)

ax.set_xlabel('Blue')
ax.set_ylabel('Green')
ax.set_zlabel('Red')

plt.show()
