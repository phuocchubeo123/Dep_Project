import tkinter

import cv2
from tkinter import *
from tkinter.ttk import *
import numpy as np
import PIL
from PIL import Image, ImageTk
import mediapipe as mp
import torch
from model import *

model = load_model()
word_dict = load_word_dict()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
	static_image_mode = False,
	max_num_hands = 2,
	min_detection_confidence = 0.5,
	min_tracking_confidence = 0.5)



class App_Tk(tkinter.Tk):
	def __init__(self, screenName):
		super().__init__(screenName = screenName)
		self.fullscreenstate = False
		self.bind("<F11>", self.fullscreen)

	def fullscreen(self, event):
		self.fullscreenstate = not self.fullscreenstate
		self.attributes("-fullscreen", self.fullscreenstate)

class App_Label(tkinter.Label):
	def __init__(self, master, text = None, height = None, width = None, progressbar = None, font = None, relief = None):
		super().__init__(master = master, text = text, font = font, height = height, width = width , relief = relief)
		self.master = master
		self.count = 0
		self.video = None
		self.query = False
		self.friend_label = None
		self.image = None
		self.progressbar = progressbar
		self.hand_tracking_flag = False
		self.array = np.zeros((150, 2, 21, 3), dtype = np.float32)

	def change_hand_tracking_flag(self):
		self.hand_tracking_flag = 1 - self.hand_tracking_flag

	def results_to_np_array(self, results):
		multi_handland_mark = results.multi_hand_landmarks
		if multi_handland_mark == None:
			pass
		elif len(multi_handland_mark) == 1:
			self.array[self.friend_label.count - 150, 0, :, :] = np.array([[lm.x, lm.y, lm.z] for lm in multi_handland_mark[0].landmark])
		else:
			try:
				self.array[self.friend_label.count - 150, :, :, :] = np.array([[[lm.x, lm.y, lm.z] for lm in lmark.landmark] for lmark in multi_handland_mark])
			except ValueError:
				pass

	def draw_hand_tracking(self, image):
		image.flags.writeable = False
		results = hands.process(image)
		self.results_to_np_array(results)
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

	def your_word_is(self):
		self.friend_label.array = clear_zero(self.friend_label.array)
		self.friend_label.array = seq_len_filter(self.friend_label.array, 8)
		self.friend_label.array = torch.from_numpy(self.friend_label.array)
		output = model.forward(self.friend_label.array)
		softmaxoutput = torch.exp(output) / torch.sum(torch.exp(output))
		lst = topk_correct(softmaxoutput, 3)
		return [[float(softmaxoutput[0][lst[0][i]]), lst[0][i]] for i in range(3)]

	def when_count_l_150(self):
		if self.count % 50 == 1:
			self.configure(text=f'Get ready: {3 - self.count // 50}')
		self.after_id = self.after(10, self.record_hand_tracking)

	def when_count_eq_150(self):
		self.friend_label.hand_tracking_flag = True
		self.configure(text='Recording')
		self.after_id = self.after(10, self.record_hand_tracking)

	def when_count_l_300(self):
		self.progressbar['value'] = ((self.count - 150) * 100) // 150 + 2
		self.after_id = self.after(10, self.record_hand_tracking)

	def when_count_eq_300(self):
		self.friend_label.hand_tracking_flag = False
		answer = self.your_word_is()
		words = [word_dict[str(int(answer[i][1]))] for i in range(3)]
		self.configure(text = f'The top three words are: \n {words[0]}: {answer[0][0] * 100: .2f}%'
							  f' \n {words[1]}: {answer[1][0] * 100: .2f}%'
							  f' \n {words[2]}: {answer[2][0] * 100: .2f}%' )
		self.friend_label.array = np.zeros((150, 2, 21, 3), dtype=np.float32)
		self.count = 0
		self.progressbar['value'] = 0
		self.after_cancel(self.after_id)
		self.after_id = None

	def record_hand_tracking(self):
		self.count += 1
		if self.count < 150:
			self.when_count_l_150()
		elif self.count == 150:
			self.when_count_eq_150()
		elif self.count < 300:
			self.when_count_l_300()
		elif self.count == 300:
			self.when_count_eq_300()

	def callback(self):
		if self.after_id:
			self.after_cancel(self.after_id)
			self.after_id = None
			self.count = 0

class App_Button(tkinter.Button):
    def __init__(self, master, text = None, font = None, height = None, width = None, command = None):
        super().__init__(master = master, text = text, font = font, height = height, width = width, command = command)

class App_Progressbar(Progressbar):
	def __init__(self, master, length = None, mode = None, orient = None):
		super().__init__(master = master, length = length, mode = mode, orient = orient)

class Text(Text):
	def __init__(self, master):
		super().__init__(master = master)
