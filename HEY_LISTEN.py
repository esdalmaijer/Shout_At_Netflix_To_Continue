import time

import numpy
import pyaudio

import win32api, win32con

DUMMYMODE = False

def click(x,y, dummymode=False):
    print("Click!")
    if dummymode:
        return
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

DISPSIZE = (1920, 1080)
CLICKPOS = (DISPSIZE[0]//2, int(DISPSIZE[1]*0.4))

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
REFRESHTIME = 10.0
AMBIENTMEMORY = 2
THRESHOLD = CHUNK * 0.3
MINCLICKTIMEDIST = 1.0

ambient = 10**-10
old_data = []
stopped = False
last_click = time.time() - MINCLICKTIMEDIST
while not stopped:

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    time.sleep(0.1)
    
    n_frames = int(RATE / CHUNK * REFRESHTIME)
    frame_size = CHUNK // 2
    data = numpy.zeros(n_frames*frame_size, dtype=numpy.float32) * numpy.NaN
    t0 = time.time()
    for i in range(0, n_frames):
        data[i*frame_size:(i+1)*frame_size] = numpy.fromstring(stream.read(CHUNK), count=frame_size)
        if ambient is None:
            ambient = numpy.nanmean(numpy.abs(data[i*frame_size:(i+1)*frame_size]))
        if numpy.sum(numpy.abs(data[i*frame_size:(i+1)*frame_size]) > ambient).astype(int) > THRESHOLD:
            print("Mean noise level: %s" % (numpy.mean(data[i*frame_size:(i+1)*frame_size])))
            if CLICKPOS is None:
                x = numpy.random.randint(0, DISPSIZE[0])
                y = numpy.random.randint(0, DISPSIZE[1])
            else:
                x, y = CLICKPOS
            if time.time() > last_click + MINCLICKTIMEDIST:
                click(x, y, dummymode=DUMMYMODE)
                last_click = time.time()

    old_data.append(data)
    if len(old_data) > AMBIENTMEMORY:
        old_data.pop(0)
    ambient = numpy.nanmean(numpy.abs(old_data))
    print("Ambient = %s" % (ambient))

    stream.stop_stream()
    stream.close()
    