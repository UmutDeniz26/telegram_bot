
# -*- coding: utf-8 -*-
import pyautogui as pag
import time
import cv2 as cv
import os
import attributes as atr


def executeCmd(command):
    pag.hotkey('win','m')
    os.system(command)


def takePhotoAndScreenShot():

    cam = cv.VideoCapture(0)
    result, image = cam.read()
    
    if pag.locateCenterOnScreen('./assets/kaspersky.png'):
        print('Submit button location: '+str(pag.locateCenterOnScreen('./assets/kaspersky.png')))
        clickImage('./assets/kaspersky.png',sleepTime=1)
        result, image = cam.read()
        
    return [result,image,pag.screenshot()]


def clickImage(imagePath, confidenceChoice=0.7,sleepTime=0, xMargin=0, yMargin=0):
    (x,y)=pag.locateCenterOnScreen(imagePath,confidence=confidenceChoice)
    pag.moveTo(x+xMargin,y+yMargin,0.1)
    pag.click()
    time.sleep(sleepTime)

def getParamsFromMessage(text):
    output=str(text).split(' ')[1:len(str(text).split(' '))]
    return False if output==[] else output

def stopCast():
    clickImage('./assets/closeCast.png',xMargin=65,sleepTime=0.5)
    clickImage('./assets/pauseCast.png')

def openSong(index):
    executeCmd('start '+ atr.songUris[index]['link'])
    time.sleep(3)

def nextSong(currentSongCnt):
    pag.hotkey('win','up')
    time.sleep(0.2)
    pag.moveTo(304,63)
    pag.click()
    pag.write(atr.songUris[currentSongCnt%len(atr.songUris)]['link'])
    pag.hotkey('enter')

