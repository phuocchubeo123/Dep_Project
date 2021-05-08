from app_classes import *

root = App_Tk(screenName = "American Sign Language Interpreter")
'''main_screen.attributes('-fullscreen', False)'''

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)



# Welcome
welcome_label = App_Label (root, text = 'Welcome to our ASL Interpreter', font = 'Source_Sans_Pro 20 bold', height = 2, width = 30, relief = GROOVE)
welcome_label.place(relx = 0.5, rely = 0.05, anchor = 'n')


# Progress Bar
progress_label = App_Label (root, text = 'Progress:', font = 'Source_Sans_Pro 10')
progress_label.place(relx = 0.5, rely = 0.13, anchor = 'n')

progressbar_hand_tracking = App_Progressbar(root, length = 250, mode = 'determinate', orient = HORIZONTAL)
progressbar_hand_tracking.place(relx = 0.5, rely = 0.16, anchor = 'n')



# Webcam Video
video_label = App_Label(root)
video_label.video = cv2.VideoCapture(0)
video_label.video.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
video_label.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_label.place(relx = 0.5, rely = 0.2, anchor = 'n')
video_label.show_frame()



# Model Output
getready_label = App_Label(root, text = 'Get ready!', font = 'Source_Sans_Pro 15 bold', progressbar = progressbar_hand_tracking)
getready_label.place(relx = 0.5, rely = 0.67, anchor = 'n')

#Friend_label
video_label.friend_label = getready_label
getready_label.friend_label = video_label

# Start Button
start_video_button = App_Button(root, text = "Start Recording", font = 'Source_Sans_Pro 10 bold', height = 2, width = 20, command = getready_label.record_hand_tracking)
start_video_button.place(relx = 0.40, rely = 0.75, anchor = 'n')


# Stop Button
stop_video_button = App_Button(root, text = "Stop Recording", font = 'Source_Sans_Pro 10 bold', height = 2, width = 20, command = getready_label.when_count_eq_300)
stop_video_button.place(relx = 0.60, rely = 0.75, anchor = 'n')


# tkinter Parameters
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_centre_x = screen_width/2
window_centre_y = screen_height/2

root.geometry(str(screen_width) + "x" + str(screen_height))

root.mainloop()

