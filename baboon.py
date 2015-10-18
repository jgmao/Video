#baboon 
import cv2 as cv
import numpy as np
import os
import re
import sys
from cv2 import __version__


def getAbsPath(relativePath):
    try:
        # PyInstaller stores data files in a tmp folder refered to as _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        # If not running as a PyInstaller created binary, try to find the data file as
        # an installed Python egg
        try:
            basePath = os.path.dirname(sys.modules['cryptully'].__file__)
        except Exception:
            basePath = ''

        # If the egg path does not exist, assume we're running as non-packaged
        if not os.path.exists(os.path.join(basePath, relativePath)):
            basePath = 'cryptully'

    path = os.path.join(basePath, relativePath)

    # If the path still doesn't exist, this function won't help you
    if not os.path.exists(path):
        return None

    return path

def compressJPEG(data, quality):
    param = [int(cv.IMWRITE_JPEG_QUALITY),quality]
    rst,enc = cv.imencode('.jpg',data, param) #,[cv.IMWRITE_JPEG_QUALITY,50])
    output = cv.imdecode(enc,1)
    print 'jpeg ', quality
    return output

def blur(data,wsize):
    output = cv.GaussianBlur(data,(wsize,wsize),3)
    print 'blur ', wsize
    return output;

def parseCfg(filename):
    f = open(filename,'r')
    for str in f.readlines():
      m = re.search('FPS\s*=\s*(\d+).\s*#',str)
      if m:
        fps =  int(m.group(1))
      m = re.search('INTERVAL\s*=\s*(\d+).\s*#',str)
      if m:
        num = int(m.group(1))
      m = re.search('MAP\s*=\s*\[\s*(.*)\s*\]\s*#',str)
      if m:
        p = re.split('\s+',m.group(1))
    f.close()
    return fps,num,p
def blank(shape,value):
    out = np.full(b2.shape,value,np.uint8)
    #out = np.ones(shape,np.uint8)
    print 'blank ', value
    return out
if len(sys.argv) != 2:
  print ( 'Usage: baboon path_to_cfg_file')
  sys.exit()

fps,num,p = parseCfg(sys.argv[1])

#print ShowFrame, BlankFrame
#print sys._MEIPASS
#print resource_path('baboon1.png')
#print('step0')
#print(getAbsPath('baboon1.png'))
#if getAbsPath('baboon1.png'):
#  print('file exist')
#print( __version__ )
#print(np.version.version)
b1 = cv.imread(getAbsPath('baboon1.png'))
b2 = cv.imread(getAbsPath('baboon2.png'))
path = os.path.dirname(os.path.realpath(__file__))

#bj1 = np.zeros(b1.shape,np.uint8);
#bj1 = compressJPEG(b1,10)
#bb1 = blur(b1,3)
#print('step1')
#cv.namedWindow('baboon')
#cv.imshow('baboon',bb1)
#cv.waitKey()

[H,W,D] = b1.shape
#g = np.full(b1.shape,int(Bc),np.uint8)
#print ('step2')

#fourcc = cv.cv.CV_FOURCC('X','V','I','D')
fourcc = cv.cv.CV_FOURCC('8','B','P','S')
out = cv.VideoWriter(os.path.join(path,'baboon.mov'),fourcc,float(fps),(W,H))
print 'Processing .... '

for f in range(0,2*num+2):
  if f==0:
      frame = b1
      print 'org 1'
  elif f == num+1:
      frame = b2
      print 'org 2'
  elif f<num+1:
      if p[(int(f)-1)*2]=='J': #jpeg
          frame = compressJPEG(b1,int(p[(int(f)-1)*2+1]))
      if p[(int(f)-1)*2]=='D': #blank
          #frame = np.full(b1.shape,int(p[(int(f)-1)*2+1]),np.uint8)
          frame = blank(b1.shape,int(p[(int(f)-1)*2+1]))
      if p[(int(f)-1)*2]=='B': #blur
          frame = blur(b1,int(p[(int(f)-1)*2+1]))
  else:
      if p[(int(f)-num-2)*2]=='J': #jpeg
          frame = compressJPEG(b2,int(p[(int(f)-num-2)*2+1]))
      if p[(int(f)-num-2)*2]=='D': #blank
          frame = blank(b1.shape,int(p[(int(f)-num-2)*2+1]))
          #frame = np.full(b2.shape,int(p[(int(f)-num-2)*2+1]),np.uint8)
      if p[(int(f)-num-2)*2]=='B': #blur
          frame = blur(b2,int(p[(int(f)-2-num)*2+1]))
  out.write(frame)




#for f in range(0,2*(BlankFrame+ShowFrame)):
#  if f < ShowFrame:
#    frame = b1;
#  elif f < ShowFrame+BlankFrame:
#    frame = g;
  #
#  elif f < 2*ShowFrame+BlankFrame:
#    frame = b2
#  else:
#    frame = g
  #cv.imshow('baboon',frame)
#  out.write(frame)
  #print f
 # if cv.waitKey(30) & 0xFF == ord('q'):
 #   break
out.release()
print('Done !')
print 'the output file is ', os.path.join(path,'baboon.mov'), ' with total ', 2*num+2, ' frames'
