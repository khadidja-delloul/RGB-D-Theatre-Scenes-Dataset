# RGB-D-Theatre-Scenes-Dataset
In this repository you will find a python code that allowed us to record depth, RGB and Skeletal data using Kinect v1.
You will also find scenarios that were interpreted by a group of computer science students in the auditorium of the University of Sciences and Technologies Houari Boumediene (USTHB), Algeria.
In the end, recorded frames can be found in the folders: RGB_images, Depth_data, Skeleton_data.
Depth is saved to JPEG images after a normalization.
Two Kinect cameras were placed at different positions to guarantee more diversity in the angles of taken images (scalability).

![Kinects' Positions.](../Scene.png)


# Requirements
  - Microsoft Kinect v1
  - Windows 10
  - Kinect Windows SDK v1.8
  - python 2.7
  - pykinect
  - OpenCV
 
 # Notes
 For each recorded scene there are 3 folders: one for depth frames, the second for RGB frames and the third for skeletons.
 The dataset is organized as follows:
  - For sequences: the folder name contains the number of the camera, the scene number, then the take number <C..S..T..>
  - For actions: the folder name contains the same information as sequence except we added the number of the actor <C..P..A..T..> 
 
 # Download Links
 Here are links to download raw data:
  - [Camera 1 Data](https://drive.google.com/drive/folders/19AHzZdrccA3IBmkZ-UQ_BIknK_4EozUo?usp=sharing)
  - [Camera 2 Data](https://drive.google.com/drive/folders/1aDHcl8zsBLjVrAiwIfAsq5yq3ypEW7jJ?usp=sharing)
 
 
 
