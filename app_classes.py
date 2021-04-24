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



class App_Tk(Tk):
	def __init__(self, screenName):
		super().__init__(screenName = screenName)
		self.fullscreenstate = False
		self.bind("<F11>", self.fullscreen)

	def fullscreen(self, event):
		self.fullscreenstate = not self.fullscreenstate
		self.attributes("-fullscreen", self.fullscreenstate)

class App_Label(Label):
	def __init__(self, master, text = None, friend_label = None, height = None, width = None,
				 progressbar = None):
		super().__init__(master = master, text = text, height = height, width = width)
		self.master = master
		self.count = 0
		self.video = None
		self.query = False
		self.friend_label = friend_label
		self.image = None
		self.progressbar = progressbar
		self.hand_tracking_flag = False
		self.array = []

	def change_hand_tracking_flag(self):
		self.hand_tracking_flag = 1 - self.hand_tracking_flag

	def draw_hand_tracking(self, image):
		image.flags.writeable = False
		results = hands.process(image)
		hand_tracking_landmarks = results.multi_hand_landmarks
		self.array.append(hand_tracking_landmarks)
		image.flags.writeable = True
		if results.multi_hand_landmarks:
			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
					image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
		return image

	def read_frame(self):
		_, frame = self.video.read()
		frame = cv2.flip(frame, 1)
		self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	def show_frame(self):
		self.read_frame()
		if self.hand_tracking_flag == False:
			img = PIL.Image.fromarray(self.image)
		else:
			img = PIL.Image.fromarray(self.draw_hand_tracking(self.image))
		imgtk = ImageTk.PhotoImage(image=img)
		self.imgtk = imgtk
		self.configure(image=imgtk)
		self.after_id = self.after(10, self.show_frame)

	def record_hand_tracking(self):
		self.count += 1
		if self.count < 150:
			if self.count % 50 == 1:
				self.configure(text = f'Get ready: {3 - self.count // 50}')
			self.after_id = self.after(10, self.record_hand_tracking)
		elif self.count == 150:
			self.friend_label.hand_tracking_flag = True
			self.configure(text = 'Recording')
			self.after_id = self.after(10, self.record_hand_tracking)
		elif self.count < 300:
			self.progressbar['value'] = ((self.count - 150) * 100) // 150 + 2
			self.after_id = self.after(10, self.record_hand_tracking)
		elif self.count == 300:
			self.friend_label.hand_tracking_flag = False
			self.configure(text = 'Your word is:')
			self.friend_label.array = []
			self.count = 0
			self.progressbar['value'] = 0
			self.after_cancel(self.after_id)
			self.after_id = None

	def callback(self):
		if self.after_id:
			self.after_cancel(self.after_id)
			self.after_id = None
			self.count = 0

class App_Button(Button):
	def __init__(self, master, text, command = None):
		super().__init__(master = master, text = text, command = command)

class App_Progressbar(Progressbar):
	def __init__(self, master, length = None, mode = None, orient = None):
		super().__init__(master = master, length = length, mode = mode, orient = orient)

class Text(Text):
	def __init__(self, master):
		super().__init__(master = master)
