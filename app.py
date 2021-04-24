from app_classes import *

def capture_webcam():
	cap = cv2.VideoCapture(0)   
	while(True): 
	    ret, frame = cap.read()  
	    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
	    out.write(hsv)  
	    cv2.imshow('Original', frame) 
	    if cv2.waitKey(1) & 0xFF == ord('a'): 
	        break
	cap.release() 
	out.release()  
	cv2.destroyAllWindows()



main_screen = App_Tk(screenName = "Main Screen")
main_screen.geometry('1800x1000')
#main_screen.attributes('-fullscreen', False)

progressbar_hand_tracking = App_Progressbar(master = main_screen, length = 200, mode = 'determinate', orient = HORIZONTAL)

video_label = App_Label(master = main_screen)
video_label.video = cv2.VideoCapture(0)
video_label.video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
video_label.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 250)
video_label.show_frame()

text_label = App_Label(master = main_screen, text = 'Welcome', friend_label = video_label, progressbar = progressbar_hand_tracking)
text_label.configure(font = 30)


start_video_button = App_Button(master = main_screen, text = "Take the video from the webcam", command = text_label.record_hand_tracking)

stop_video_button = App_Button(master = main_screen, text = "Stop recording", command = video_label.callback)

progressbar_hand_tracking.pack()
text_label.pack()
video_label.pack()
start_video_button.pack()
stop_video_button.pack()
main_screen.mainloop()

print()
