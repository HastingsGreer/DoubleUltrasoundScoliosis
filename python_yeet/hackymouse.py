import ctypes

def click(x, y):
  ctypes.windll.user32.SetCursorPos(x, y)
  ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
  ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

def getPos():
  p = ctypes.wintypes.POINT()
  ctypes.windll.user32.GetCursorPos(ctypes.pointer(p))
  return p.x, p.y
import time
def sleep(t):
  x, y = getPos()
  time.sleep(t)
  if(x != getPos()[0]):
    raise KeyboardInterrupt


def promptPos(text):
  print("Move Mouse to " + text, end = "\r")
  for n in range(5):
     print("Move Mouse to " + text + " " + str(5 - n), end = "\r")
     time.sleep(1)
  print()
  return getPos()

import math
def alien():
  center = promptPos("Center:")
  p1 = promptPos("Edge: ")
  r = math.sqrt((center[0] - p1[0])**2 + (center[1] - p1[1])**2)
  th = 0
  while True:
        th += .05
        click(int(center[0] + r * math.cos(th)), int(center[1] + r * math.sin(th)))
        sleep(.01)

def epi():
  p1 = promptPos("Color 1:")
  p2 = promptPos("Color 2: ")
  while True:
       
        click(*p1)
        sleep(.05)
        click(*p2)
        sleep(.05)
