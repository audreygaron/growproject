# Focus of project
I built a convolutional neural network that labeled images based on whether or not a robot was in them. 

Previously, the Tron lab used the video feeds of Roomba Create robots to monitor each other as part of a security protocol. All of the robots were provided with observation guidelines for where they should anticipate the other robots to be, in case one of the other robots veered off in an unexpected direction, posing a risk to the facility. For the robot to detect another robot within the frame of its video feed, a neural network is required. 

Link to my poster: https://docs.google.com/presentation/d/1PhZVwcVXEPDdUp0-q9S6qtPHq6jwGptK1i3fDfSt6QI/edit?usp=sharing

Link to my website: https://sites.google.com/view/audreygarongrowupdates/home

# Methods
## 1. Positive data (images with the robot) 
I. For my positive data, I positioned a Roomba Create robot on top of several green mats on the floor.

II. I then carried and walked around with another Roomba Create robot as it took a video of the original robot with the green mats posing as a green screen background.

III. I distilled the video into 38 individual images.

<a href="https://drive.google.com/uc?export=view&id=16gDZQXTNvyLs8h0VYAHToXCZYux7fTMm"><img src="https://drive.google.com/uc?export=view&id=16gDZQXTNvyLs8h0VYAHToXCZYux7fTMm" style="width: 400px; max-width: 100%; height: auto" title="Image taken by one Roomba Create robot of another robot on top of a green screen background." /></a>

IV. Next, I wrote a script that pixel-by-pixel swapped the green pixels in the background of each image for the pixels in another image. Every image’s green screen background was replaced with 10 other images, so that for every original image there was now 10 (in total 380).

<a href="https://drive.google.com/uc?export=view&id=1oTz0uw9G1f_n3lOjqnr52GRG_hp1kGvG"><img src="https://drive.google.com/uc?export=view&id=1oTz0uw9G1f_n3lOjqnr52GRG_hp1kGvG" style="width: 400px; max-width: 100%; height: auto" title="Image taken by one Roomba Create robot of another robot on top of a green screen background." /></a>

<a href="https://drive.google.com/uc?export=view&id=1p_c0QQ4UGRSz02QFs7DQBGyQQiXzzCLO"><img src="https://drive.google.com/uc?export=view&id=1p_c0QQ4UGRSz02QFs7DQBGyQQiXzzCLO" style="width: 400px; max-width: 100%; height: auto" title="Image taken by one Roomba Create robot of another robot on top of a green screen background." /></a>

V. To further augment my dataset, I wrote a program that created copies of the mixed images that were then vertically flipped so my data set contained 760 images instead of 380.

## 2. Negative data (images without the robot)
I. For my negative data, I carried and walked around with a Roomba Create robot while it took a video of different spaces in the lab.

II. I distilled the video into 760 individual images.

## 3. Storing the data
I. I organized my data into two directories: training and testing. Within each of those folders, I had two subdirectories labelled “robot” and “not-robot.”

II. I put 90% of the positive data and 90% of the negative data in my training folder, and 10% of the positive data and 10% of the negative data in my testing folder.

## 4. Corrupting the testing images
I wrote a script that based on a pre-set number of pixels, randomly selected pixels in each of the mixed images within the testing data set and turned them black. I made several test data sets— each with a certain amount of corrupted pixels. I made a total of 14 data sets (not including the original, uncorrupted images) where both the positive and negative data were corrupted. The number of affected pixels ranged from 50 to 650 pixels for all of the datasets. I later compared the testing accuracy of these data sets with each other and the uncorrupted testing data set.

## 5. Creating the model
The height, width, and number of channels were inputs to the model. The model had seven layers and 378,152 parameters. They were passed through the first activation function, a maxpool layer, two more activation functions, another maxpool layer, a linear layer, and a layer that moved the model forward. The model produced a prediction for whether there is or is not a robot in the image.

## 6. Running the data through the model
I trained my data and then tested it on the model.

# Training
1. First, the model predicted whether or not there was a robot in the image. 

2. The model then computed loss by finding the difference between the groundtruth (labels) and outputs (predictions).

3. By backward passing, the model calculated the gradients and updated the parameters. 

4. The model iterated over the training images 15 times and the accuracy was 100%.

# Testing
1. I inputted each of my testing data sets (uncorrupted, 50-650 pixels corrupted) into the model. 

2. The model’s predictions were then compared with the groundtruth.

3. The accuracy of the model was calculated and is shown below for each of the testing data sets based on how many pixels were corrupted.

# Conclusions
While 100% accuracy (for uncorrupted images) might seem impossible, the dataset itself provides an explanation for why the model can consistently predict whether or not a robot is in an image. The robot - no matter its rotation - looks the same in every image because it has a spherical design; this makes it easier for the model since the pixels values are similar in all the images. Before working on this project, I followed a tutorial that classified images based on whether they contained hotdogs. The hotdogs in these images were not all the same, meaning the model could not always predict if a hotdog was a hotdog. Additionally, the low testing accuracy for corrupted images demonstrates that a complex model would be needed for an expanded data set that includes more complicated images than those that were used in the uncorrupted data set.

Though simple, this model can be used to classify other objects that appear in images. The most practical use of the model is for objects that - when rotated - look the same from all angles. For example, a data set with images containing water bottles could be well suited for this model. However, if the data set contains images with multiple types of the same object (i.e. hotdogs with different toppings) and the object looks different from multiple angles, then a more complex model may be required to maintain a high accuracy rate.

