import cv2
import random
import os
import datetime
from moviepy.editor import VideoFileClip

def returnFolders():
    return (os.listdir('input'))

def returnVideos(name: str):
    return (os.listdir('input/' + name))

def checkForFolder(name: str):
    return (os.path.isdir("input/" + name))

def checkForVideo(folder: str, name: str):
    if (checkForFolder(folder) == False):
        return False
    else:
        for video in os.listdir('input/' + folder):
            if (name.lower() == str(video).lower().split(".")[0]):
                return True
            
        return False

def chooseFolder():
    entries = os.listdir('input')
    return (entries[random.randint(0, len(entries) - 1)])

def chooseVideo(name: str):
    entries = os.listdir('input/' + name)
    return (entries[random.randint(0, len(entries) - 1)])

def returnName(name: str):
    for folder in os.listdir('input'):
        if (name.lower() == str(folder).lower()):
            return str(folder)
        
def returnVideoName(folder: str, name: str):
    for video in os.listdir('input/' + folder):
        if (name.lower() == str(video).lower().split(".")[0]):
            return str(video)
        
def convertFrameToTime(frame: int, video: str):
    videoClip = VideoFileClip(video)
    fps = videoClip.fps
    videoClip.close()
    return (datetime.timedelta(seconds=frame / fps))

def obtainFrame(name: str, nameOfVideo: str = ""):
    if (nameOfVideo == ""):
        nameOfVideo = str(chooseVideo(name))
    else:
        nameOfVideo = returnVideoName(name, nameOfVideo)

    directory = "input/" + name + "/" + nameOfVideo
    video = cv2.VideoCapture(directory)
    numOfFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    randomFrame = None
    ret = False
    frame = None

    while (ret == False):
        randomFrame = random.randint(0, numOfFrames)
        video.set(cv2.CAP_PROP_POS_FRAMES, randomFrame)
        ret, frame = video.read()
    
    cv2.imwrite("output.jpg", frame)
    video.release()
    cv2.destroyAllWindows()
    return ([returnName(name), nameOfVideo.split(".")[0], str(convertFrameToTime(randomFrame, directory)).split(".")[0]])