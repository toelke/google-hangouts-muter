import win32gui
import win32ui
from ctypes import windll
from PIL import Image, ImageStat
import win32con
import time
import ctypes
import serial
import threading
import pywinauto
from pywinauto import Desktop

top_windows = Desktop(backend="uia").windows()
cw = [x for x in top_windows if 'Chrome' in x.window_text()][0]
app = pywinauto.Application(backend="win32").connect(process=cw.process_id())
form = app.window()


def f(hwnd, l):
    l.append((hwnd, win32gui.GetWindowText(hwnd)))


l = []
win32gui.EnumWindows(f, l)
hwnd_target = [x for x in l if 'Chrome' in x[1]][0][0]

ser = serial.Serial('COM6', 9600)


def thread():
    while True:
        try:
            n = ser.read(1)
            if n == b'1':
                form.send_keystrokes('^d')
        except:
            pass


t = threading.Thread(target=thread)
t.setDaemon(True)
t.start()

while True:
    time.sleep(0.1)
    fgw = win32gui.GetForegroundWindow()
    if fgw != hwnd_target:
        ser.write(b'?')
        print('?')
        continue

    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    left, top, right, bot = (right - 27, top + 109, right - 11, top + 125)
    w = right - left
    h = bot - top

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)

    if result is None:
        # im.save("test.png")
        # break
        s = ImageStat.Stat(im)
        # check how red the image is
        ser.write(b'm' if (3 * s.median[0] - sum(s.median)) > 200 else b'u')
        print('m' if (3 * s.median[0] - sum(s.median)) > 200 else 'u')
