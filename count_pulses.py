import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.signal
import argparse

parser = argparse.ArgumentParser(description='Count red pulses in a video file.')
parser.add_argument('filename',help='path to video file', type=str, metavar="filename")
parser.add_argument('--frames',nargs='?',help='number of frames to process (defualt: process entire video)',type=int)
parser.add_argument('--prominence',
                    nargs='?',
                    help='peak prominence needed for to include peak in count (defualt: 8)\nsee scipy.signal documentation for definition of peak prominence',
                    type=float,
                    default=8
                   )
parser.add_argument('--wlen',
                    nargs='?',
                    help='size of window in which peak prominence is measured (defualt: 200)\nfor details, see scipy.signal documentation on peak prominance',
                    type=int,
                    default=200
                   )
parser.add_argument('--window',
                    nargs='?',
                    help='size (in pixels) of window in which to crop red pulse image in each frame. (default:40)',
                    type=int,
                    default=40
                   )
parser.add_argument('--showframe',
                    nargs='?',
                    help='instead of running as usual, show cropped frame of given index (default: show frame 2)\nrecommended to use this with --window to get cropping right',
                    type=int,
                    metavar='frame_number',
                    default=2)
args=parser.parse_args()
FILENAME=args.filename
PROMINENCE=args.prominence
FRAMES=args.frames
WLEN=args.wlen
WINSIZE=args.window
SHOWFRAME=args.showframe


filename=FILENAME
vid=cv2.VideoCapture(filename)

def find_dot(channel, threshold=250,window_size=WINSIZE//2):
    """Return crop xmin,xmax,yminymax.
       
       channel: the img/channel to use in order to find the dot (e.g. the red channel of a frame)
       threshold: minimum value of pixels in channel to be considered part of average for dot finding
       window_size: the img will be cropped to a box at the mean point +/- window_size
    
    """
    red_pixels=[]
    for i in range(channel.shape[0]):
        for j in range(channel.shape[1]):
            if channel[i,j] > threshold:
                    red_pixels.append([i,j])
    dotx,doty=np.round(np.mean(red_pixels,axis=0))
    dotx,doty=int(dotx),int(doty)
    return dotx-window_size,dotx+window_size,doty-window_size,doty+window_size


if not (SHOWFRAME is None):
    i=0
    successful_read=True
    while successful_read:
        i+=1
        successful_read,frame = vid.read()
        if i>=SHOWFRAME:
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            xmin,xmax,ymin,ymax=find_dot(frame[:,:,0])
            plt.imshow(frame[xmin:xmax,ymin:ymax])
            plt.show()
            sys.exit(0)

    

successful_read,frame = vid.read()
red_channel=frame[:,:,2]
xmin,xmax,ymin,ymax=find_dot(red_channel)
means=[]
i=0
while successful_read:
    i+=1
    sys.stdout.write("Frame {}\r".format(i))
    sys.stdout.flush()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_cropped_frame=frame[xmin:xmax,ymin:ymax]
    means.append(np.mean(gray_cropped_frame))
    successful_read,frame = vid.read()
    if i%200==0: xmin,xmax,ymin,ymax=find_dot(frame[:,:,2])
    if (not FRAMES is None) and i>FRAMES: break
means=np.array(means)

peaks, properties = scipy.signal.find_peaks(means,prominence=PROMINENCE,wlen=WLEN)
plt.plot(means)
plt.plot(peaks,[means[p] for p in peaks],'ro')
print(len(peaks), " peaks found.")
plt.show()
