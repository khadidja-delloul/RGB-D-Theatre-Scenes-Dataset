
from pykinect import nui
import time
import pygame
from pygame.color import THECOLORS
from pykinect.nui import JointId
import itertools
import shutil
import os
import cv2
import numpy
import sys

current_directory = os.getcwd()

SKELETON_COLORS = [ THECOLORS["red"],
                    THECOLORS["blue"],
                    THECOLORS["green"],
                    THECOLORS["orange"],
                    THECOLORS["purple"],
                    THECOLORS["yellow"],
                    THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter,
            JointId.ShoulderLeft,
            JointId.ElbowLeft,
            JointId.WristLeft,
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter,
             JointId.ShoulderRight,
             JointId.ElbowRight,
             JointId.WristRight,
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter,
            JointId.HipLeft,
            JointId.KneeLeft,
            JointId.AnkleLeft,
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter,
             JointId.HipRight,
             JointId.KneeRight,
             JointId.AnkleRight,
             JointId.FootRight)
SPINE = (JointId.HipCenter,
         JointId.Spine,
         JointId.ShoulderCenter,
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def draw_skeleton_data(pSkelton, index, positions, width=4):
    start = pSkelton.SkeletonPositions[positions[0]]

    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]

        curstart = skeleton_to_depth_image(start, window_size[0], window_size[1])
        curend = skeleton_to_depth_image(next, window_size[0], window_size[1])

        pygame.draw.line(window, SKELETON_COLORS[index], curstart, curend, width)

        start = next

def draw_skeletons(skeletons):

    for i, data in enumerate(skeletons):

        # draw the Head
        index=i
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], window_size[0], window_size[1])
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(window, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)

        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)

        #bounding box
        #y2=minY(data)
        #x1=minX(data)
        #x2=maxX(data)
        #y1=maxY(data)
        #width=x2-x1
        #height=y2-y1
        #pygame.draw.rect(window, SKELETON_COLORS[index], (x1, y1, width, height),2) #bounding box drawing
    pygame.display.update()

def minX(data):
    min=200000
    index=-1
    for i in range(0,19):
        if data.SkeletonPositions[i].x<min:
            min=data.SkeletonPositions[i].x
            index=i
    return skeleton_to_depth_image(data.SkeletonPositions[index], window_size[0], window_size[1])[0]

def minY(data):
    min=200000
    index=-1
    for i in range(0,19):
        if data.SkeletonPositions[i].y<min:
            min=data.SkeletonPositions[i].y
            index=i
    return skeleton_to_depth_image(data.SkeletonPositions[index], window_size[0], window_size[1])[1]
def maxX(data):
    max=-2000000
    index=-1
    for i in range(0,19):
        if data.SkeletonPositions[i].x>max:
            max=data.SkeletonPositions[i].x
            index=i
    return skeleton_to_depth_image(data.SkeletonPositions[index], window_size[0], window_size[1])[0]
def maxY(data):
    max=-2000000
    index=-1
    for i in range(0,19):
        if data.SkeletonPositions[i].y>max:
            max=data.SkeletonPositions[i].y
            index=i
    return skeleton_to_depth_image(data.SkeletonPositions[index], window_size[0], window_size[1])[1]




def video_frame_ready(frame):
    frame.image.copy_bits(window._pixels_address)
    draw_skeletons(skeletons)
    pygame.display.update()
    height, width = frame.image.height, frame.image.width  # get width and height of the images
    rgb = numpy.empty((height, width, 4), numpy.uint8)
    frame.image.copy_bits(rgb.ctypes.data)
    folder = 'RGB_images' + '\\C' + camera_id + 'P' + person_id + 'A'+action_id+'T'+ take_id
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = current_directory + str('\\') + folder
    image_name = 'F' + str(frame.frame_number) + '.jpg'
    if save_image:
        cv2.imwrite(os.path.join(path, image_name), rgb)



def post_frame(frame):
    try:
        pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons=frame.SkeletonData))
    except:
        # event queue full
        pass


def saveSkeletons(skeletons):
    num=0
    for i,skeleton in enumerate(skeletons):
        if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
            num=num+1
    if num>0:
        #save number of detected skeletons
        skeletonfile.write(str(num)+"\n")
    num=1
    for i,data in enumerate(skeletons):
        if data.eTrackingState == nui.SkeletonTrackingState.TRACKED:
            skeletonfile.write(str(num)+"\n") #number of the following skeleton
            skeletonfile.write("25\n") #number of joints
            skeletonfile.write(str(data.SkeletonPositions[JointId.HipCenter].x)+" "+str(data.SkeletonPositions[JointId.HipCenter].y)+" "+str(data.SkeletonPositions[JointId.HipCenter].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.Spine].x)+" "+str(data.SkeletonPositions[JointId.Spine].y)+" "+str(data.SkeletonPositions[JointId.Spine].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.Head].x)+" "+str(data.SkeletonPositions[JointId.Head].y)+" "+str(data.SkeletonPositions[JointId.Head].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.Head].x)+" "+str(data.SkeletonPositions[JointId.Head].y)+" "+str(data.SkeletonPositions[JointId.Head].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.ShoulderLeft].x)+" "+str(data.SkeletonPositions[JointId.ShoulderLeft].y)+" "+str(data.SkeletonPositions[JointId.ShoulderLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.ElbowLeft].x)+" "+str(data.SkeletonPositions[JointId.ElbowLeft].y)+" "+str(data.SkeletonPositions[JointId.ElbowLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.WristLeft].x)+" "+str(data.SkeletonPositions[JointId.WristLeft].y)+" "+str(data.SkeletonPositions[JointId.WristLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HandLeft].x)+" "+str(data.SkeletonPositions[JointId.HandLeft].y)+" "+str(data.SkeletonPositions[JointId.HandLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.ShoulderRight].x)+" "+str(data.SkeletonPositions[JointId.ShoulderRight].y)+" "+str(data.SkeletonPositions[JointId.ShoulderRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.ElbowRight].x)+" "+str(data.SkeletonPositions[JointId.ElbowRight].y)+" "+str(data.SkeletonPositions[JointId.ElbowRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.WristRight].x)+" "+str(data.SkeletonPositions[JointId.WristRight].y)+" "+str(data.SkeletonPositions[JointId.WristRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HandRight].x)+" "+str(data.SkeletonPositions[JointId.HandRight].y)+" "+str(data.SkeletonPositions[JointId.HandRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HipLeft].x)+" "+str(data.SkeletonPositions[JointId.HipLeft].y)+" "+str(data.SkeletonPositions[JointId.HipLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.KneeLeft].x)+" "+str(data.SkeletonPositions[JointId.KneeLeft].y)+" "+str(data.SkeletonPositions[JointId.KneeLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.AnkleLeft].x)+" "+str(data.SkeletonPositions[JointId.AnkleLeft].y)+" "+str(data.SkeletonPositions[JointId.AnkleLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.FootLeft].x)+" "+str(data.SkeletonPositions[JointId.FootLeft].y)+" "+str(data.SkeletonPositions[JointId.HipCenter].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HipRight].x)+" "+str(data.SkeletonPositions[JointId.HipRight].y)+" "+str(data.SkeletonPositions[JointId.HipRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.KneeRight].x)+" "+str(data.SkeletonPositions[JointId.KneeRight].y)+" "+str(data.SkeletonPositions[JointId.KneeRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.AnkleRight].x)+" "+str(data.SkeletonPositions[JointId.AnkleRight].y)+" "+str(data.SkeletonPositions[JointId.AnkleRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.FootRight].x)+" "+str(data.SkeletonPositions[JointId.FootRight].y)+" "+str(data.SkeletonPositions[JointId.FootRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.ShoulderCenter].x)+" "+str(data.SkeletonPositions[JointId.ShoulderCenter].y)+" "+str(data.SkeletonPositions[JointId.ShoulderCenter].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HandLeft].x)+" "+str(data.SkeletonPositions[JointId.HandLeft].y)+" "+str(data.SkeletonPositions[JointId.HandLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HandLeft].x)+" "+str(data.SkeletonPositions[JointId.HandLeft].y)+" "+str(data.SkeletonPositions[JointId.HandLeft].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HandRight].x)+" "+str(data.SkeletonPositions[JointId.HandRight].y)+" "+str(data.SkeletonPositions[JointId.HandRight].z)+"\n")
            skeletonfile.write(str(data.SkeletonPositions[JointId.HandRight].x)+" "+str(data.SkeletonPositions[JointId.HandRight].y)+" "+str(data.SkeletonPositions[JointId.HandRight].z)+"\n")
            num=num+1





def getDepthImage(frame):
    height, width = frame.image.height, frame.image.width  #get frame height and width
    depth = numpy.empty((height, width, 1), numpy.uint8)
    arr2d = (depth >> 3) & 4095
    arr2d >>= 4

    frame.image.copy_bits(arr2d.ctypes.data)
    cv2.imshow('KINECT depth Stream', arr2d)



    tab=arr2d


    folder = 'Depth_data' + '\\C' + camera_id + 'P' + person_id + 'A'+action_id+'T'+ take_id
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = current_directory + str('\\') + folder
    file_name = 'F' + str(frame.frame_number) + '.jpeg'
    file_to_save = os.path.join(path, file_name)
    if save_image:
        cv2.normalize(arr2d, arr2d, 0, 255, cv2.NORM_MINMAX)
        cv2.imwrite(file_to_save, arr2d)





if __name__ == '__main__':

    # Screen Settings
    global tab

    global window_size
    global skeletonfile
    global skeletonfilename
    global camera_id, action_id, take_id, person_id
    global save_image
    save_image = False

    camera_id="2"
    action_id= raw_input("action_id: ")
    person_id= raw_input("person_id: ")
    take_id= raw_input("take_id: ")


    window_size= (640, 480)
    tab=numpy.empty((640, 480, 1), numpy.uint8)
    folder = 'Skeleton_data'
    if not os.path.exists(folder):
        os.makedirs(folder)
    skeletonfilename= 'C' + camera_id + 'P' + person_id + 'A'+action_id+'T'+ take_id
    skeletonfile=open(folder+'//'+skeletonfilename+'.skeleton',"w")

    window = pygame.display.set_mode(window_size)
    KINECTEVENT = pygame.USEREVENT

    skeletons = []
    cpt=0 #to count number of frame s
    pygame.init()
    clock = pygame.time.Clock()


    #Game loop start
    with nui.Runtime() as kinect:

        #standard initialization for kinect
        kinect.skeleton_engine.enabled = True

        #RGB and Skeleton frames
        kinect.video_frame_ready += video_frame_ready
        kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)

        #Depth frames
        kinect.depth_frame_ready += getDepthImage
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)
        cv2.namedWindow('KINECT depth Stream', cv2.WINDOW_AUTOSIZE)

        #Updating Skeleton frames
        kinect.skeleton_frame_ready += post_frame
        pygame.display.update()


        # update skeleton drawing
        while True:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(tab)
                    cv2.normalize(tab, tab, 0, 255, cv2.NORM_MINMAX)
                    cv2.imwrite("hh.jpeg", tab)
                    skeletonfile.write(str(cpt))
                    skeletonfile.close()
                    sys.exit()
                elif event.type== pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        save_image = True
                        print('t')
                        if save_image :
                            print("start recording")

                #enters when kinect detects a person
                if event.type == KINECTEVENT:
                    skeletons = event.skeletons
                    #draw skeletons
                    draw_skeletons(skeletons)
                    pygame.display.update()
                    if save_image:
                        saveSkeletons(skeletons)
                        cpt=cpt+1







