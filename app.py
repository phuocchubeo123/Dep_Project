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

progressbar_test = App_Progressbar(master = main_screen, length = 100, mode = 'determinate', orient = HORIZONTAL)
progressbar_test.pack()

left_label = App_Label(master = main_screen, text = 'Welcome')
left_label.configure(font = 20)
left_label.place(relx = 0.1, rely = 0.1)
left_label.video = cv2.VideoCapture(0)
left_label.video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
left_label.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 250)

right_label = App_Label(master = main_screen, text = 'Right', another_label = left_label, progressbar = progressbar_test)
right_label.place(relx = 0.9, rely = 0.1, anchor = 'ne')

start_video_button = App_Button(master = main_screen, text = "Take the video from the webcam", command = right_label.show_frame_from_another_label)
start_video_button.place(relx = 0.5, rely = 0.7, anchor = 'center')

stop_video_button = App_Button(master = main_screen, text = "Stop recording", command = right_label.callback)
stop_video_button.place(relx = 0.5, rely = 0.8, anchor = 'center')

main_screen.mainloop()

print()