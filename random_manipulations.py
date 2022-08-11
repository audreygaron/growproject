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

#data augmentation (makes data set bigger by vertically flipping each original image)
count1 = 100
for robot_image in os.listdir("/home/audrey/data/changed_images/"):
    count1 += 1
    vertical_image_path = "/home/audrey/data/changed_images/" + robot_image
    image = cv2.imread(vertical_image_path)
    copy_of_image = image.copy()
    vertical_image = cv2.flip(copy_of_image, 1)
    
    vertical_image_path = os.path.abspath(f"/home/audrey/data/flipped/{str(count1)}.jpg")
    cv2.imwrite(vertical_image_path, vertical_image)

# vertically flip not-robot images
count1 = 100
for robot_image in os.listdir("/home/audrey/manipulated_dataset/not-robot/"):
    count1 += 1
    vertical_image_path = "/home/audrey/manipulated_dataset/not-robot/" + robot_image
    image = cv2.imread(vertical_image_path)
    copy_of_image = image.copy()
    vertical_image = cv2.flip(copy_of_image, 1)
    
    vertical_image_path = os.path.abspath(f"/home/audrey/manipulated_dataset/{str(count1)}.jpg")
    cv2.imwrite(vertical_image_path, vertical_image)

# mix images with background images (get rid of green and black pixels)
def mix_images(my_image, background_image):
    # Read an image. IMAGE_PATH should be the path to your image (e.g.: /home/audrey/dataset_images/image_1.jpg)
    # NOTE: If the path of the image is wrong, the output of cv2.imread will make my_image have the value "None". 
    # The following lines raise an error if the image path doesn't exist:
    if my_image is None:
        raise AssertionError("The image path you provided doesn't exist!")
    if background_image is None:
        raise AssertionError("The new backround image path you provided doesn't exist!")

    print("Image type:", type(my_image)) 
    print("New background type", type(background_image))

    print("Image shape:",my_image.shape)
    print("Background image shape: ", background_image.shape)

    new_width = 300
    new_size = (new_width, int(my_image.shape[0]/my_image.shape[1] * new_width))
    resized_image = cv2.resize(my_image, new_size)
    print(resized_image.shape)
    resized_background_image = cv2.resize(background_image, new_size)
    print(resized_background_image.shape)

    ### Image modification
    new_image = resized_image.copy()

    new_background_image = resized_background_image.copy()

    #finds index for BGR values within specific range
    location = cv2.inRange(new_image,(10,115,25),(145,230,155))
    #adds another dimension to location
    location = np.reshape(location,(location.shape[0],location.shape[1],1))
    # within tile function, first parameter is what you want to repeat and second is saying that there are two rows, two cols and within it place the third axis (the channel --> so GRB)
    location = np.tile(location,(1,1,3))

    # BLACK PIXELS
    location2 = cv2.inRange(new_image, (0,0,0),(0,0,0))
    location2 = np.reshape(location2,(location2.shape[0],location2.shape[1],1))
    location2 = np.tile(location2,(1,1,3))

    # shows which pixels fall within range specified above
    mask = np.where(location)
    mask2 = np.where(location2)
    final_image = new_image.copy()
    # the masked pixels are now replaced by the same indexed pixels from the background image
    final_image[mask] = new_background_image[mask]
    final_image[mask2] = new_background_image[mask2]
    return final_image

count2 = 0
for my_file in os.listdir("/home/audrey/data/images/"):
    for background_file in os.listdir("/home/audrey/data/bg/"):
        count2 += 1
        image_file_path = "/home/audrey/data/images/" + my_file
        background_file_path = "/home/audrey/data/bg/" + background_file
        robot_image = cv2.imread(image_file_path)
        background_image = cv2.imread(background_file_path)
        # same thing for background_file
        mixed_image = mix_images(robot_image, background_image)
        #this generates names for the new files
        final_file_path = os.path.abspath(f"/home/audrey/data/mixed/{str(count2)}.jpg")
        print(final_file_path)
        #save final_image to final_file using cv2.imwrite
        cv2.imwrite(final_file_path, mixed_image)
