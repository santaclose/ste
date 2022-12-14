import os
import time
import signal
import string
import random
import pyperclip
import pyautogui
import subprocess
import pydirectinput

loremIpsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum."""
loremIpsumLines = loremIpsum.split('\n')

def waitAndClickOnImage(imagePath, clicks=1):
	point = None
	while point is None:
		point = pyautogui.locateCenterOnScreen(imagePath)
	pyautogui.moveTo(point)
	pyautogui.click(clicks=clicks)

def generateRandomText():
	digits = ''.join(random.sample(string.digits, 8))
	chars = ''.join(random.sample(string.ascii_letters, 15))
	return digits + chars


os.chdir("..")
p = subprocess.Popen(["bin/Release-windows-x86_64/ste/ste.exe"], stdout=subprocess.DEVNULL)

try:
	waitAndClickOnImage("testing/menu.png")
	waitAndClickOnImage("testing/newpanel.png")

	randomText = generateRandomText()
	pyautogui.write(randomText)
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == randomText)
	print("Write and copy test passed")

	pyperclip.copy(loremIpsum)
	pyautogui.hotkey("ctrl", "v", interval=0.1)
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == loremIpsum)
	print("Paste from outside test passed")

	pydirectinput.press("left")
	pyautogui.write('\n')
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == '\n' + loremIpsum)
	print("Add line to beginning test passed")

	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pydirectinput.press("right")
	pyautogui.write('\n')
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == '\n' + loremIpsum + '\n')
	print("Add line to end test passed")

	pydirectinput.press("right")
	pyautogui.hotkey("ctrl", "shift", "k", interval=0.1)
	pydirectinput.press("up")
	pydirectinput.press("up")
	pyautogui.hotkey("ctrl", "shift", "k", interval=0.1)
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pydirectinput.press("left")
	pyautogui.hotkey("ctrl", "shift", "k", interval=0.1)
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	clipboardLines = pyperclip.paste().split('\n')
	assert(len(clipboardLines) == 3)
	assert(clipboardLines[0] == loremIpsumLines[0])
	assert(clipboardLines[1] == loremIpsumLines[2])
	assert(clipboardLines[2] == loremIpsumLines[3])
	print("Ctrl shift k test passed")

	pyautogui.write("asdf\n\tasdf\n\t\tasdf\n\nasdf\n\t\t\tasdf")
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "[", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "asdf\nasdf\n\tasdf\n\nasdf\n\t\tasdf")
	pyautogui.hotkey("ctrl", "[", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "asdf\nasdf\nasdf\n\nasdf\n\tasdf")
	pyautogui.hotkey("ctrl", "[", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "asdf\nasdf\nasdf\n\nasdf\nasdf")
	pyautogui.hotkey("ctrl", "]", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "\tasdf\n\tasdf\n\tasdf\n\n\tasdf\n\tasdf")
	print("Ctrl [ and ctrl ] test passed")

	pyautogui.write("a b")
	waitAndClickOnImage("testing/a.png", clicks=2)
	pyautogui.keyDown('ctrl')
	waitAndClickOnImage("testing/b.png", clicks=2)
	pyautogui.keyUp('ctrl')
	pyautogui.write("zxcv")
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "zxcv zxcv")
	pyautogui.hotkey("ctrl", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "a b")
	pyautogui.hotkey("ctrl", "shift", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "shift", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "shift", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "shift", "z", interval=0.1)
	pyautogui.hotkey("ctrl", "a", interval=0.1)
	pyautogui.hotkey("ctrl", "c", interval=0.1)
	assert(pyperclip.paste() == "zxcv zxcv")
	print("Multicursor replace and undo redo test passed")

	# breakpoint()
except Exception as e:
	os.kill(p.pid, signal.SIGTERM)
	raise e

print("All tests passed")
os.kill(p.pid, signal.SIGTERM)