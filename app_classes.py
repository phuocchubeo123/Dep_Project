import cv2
from tkinter import *
from tkinter.ttk import *
import numpy as np
import torch
import PIL
from PIL import Image, ImageTk
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
	static_image_mode = False,
	max_num_hands = 2,
	min_detection_confidence = 0.5,
	min_tracking_confidence = 0.5)

def draw_hand_tracking(image):
	image.flags.writeable = False
	results = hands.process(image)
	image.flags.writeable = True
	if results.multi_hand_landmarks:
		for hand_landmarks in results.multi_hand_landmarks:
			mp_drawing.draw_landmarks(
				image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
	return image

class App_Tk(Tk):
	def __init__(self, screenName):
		super().__init__(screenName = screenName)
		self.fullscreenstate = False
		self.bind("<F11>", self.fullscreen)

	def fullscreen(self, event):
		self.fullscreenstate = not self.fullscreenstate
		self.attributes("-fullscreen", self.fullscreenstate)

class App_Label(Label):
	def __init__(self, master, text = None, another_label = None, height = None, width = None, progressbar = None):
		super().__init__(master = master, text = text, height = height, width = width)
		self.master = master
		self.count = 0
		self.video = None
		self.query = False
		self.another_label = another_label
		self.image = None
		self.progressbar = progressbar

	def read_frame(self):
		_, frame = self.video.read()
		frame = cv2.flip(frame, 1)
		self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	def show_frame(self):
		self.read_frame()
		img = PIL.Image.fromarray(self.image)
		imgtk = ImageTk.PhotoImage(image = img)
		self.imgtk = imgtk
		self.configure(image = imgtk)

	def show_frame_from_another_label(self):
		print(self.count)
		self.count += 1
		self.another_label.show_frame()
		if self.count <= 150:
			if self.count % 50 == 1:
				img2 = PIL.Image.fromarray(self.another_label.image.copy())
				imgtk2 = ImageTk.PhotoImage(image = img2)
				self.imgtk = imgtk2
				self.configure(text = 3 - (self.count - 1) // 50)
				self.imgtk = None
			else:
				pass
			self.after_id = self.after(10, self.show_frame_from_another_label)
		else:
			if self.count == 300:
				self.callback()
			else:
				if self.progressbar:
					self.progressbar['value'] = ((self.count - 150) * 100) // 150 + 2
				img2 = PIL.Image.fromarray(draw_hand_tracking(self.another_label.image.copy()))
				imgtk = ImageTk.PhotoImage(image = img2)
				self.imgtk = imgtk
				self.configure(image = self.imgtk)
				self.after_id = self.after(10, self.show_frame_from_another_label)

	def callback(self):
		if self.after_id:
			self.after_cancel(self.after_id)
			self.after_id = None
			del self.imgtk
			self.count = 0

class App_Button(Button):
	def __init__(self, master, text, command = None):
		super().__init__(master = master, text = text, command = command)

class App_Progressbar(Progressbar):
	def __init__(self, master, length = None, mode = None, orient = None):
		super().__init__(master = master, length = length, mode = mode, orient = orient)