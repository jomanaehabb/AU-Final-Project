import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from pyzbar.pyzbar import decode

# IP camera URL (use 'http' instead of 'https' for OpenCV compatibility)
ip_webcam_url = 'http://192.168.246.164:8080/video'
cap = cv2.VideoCapture(ip_webcam_url)
rec_data = "none"

def update_video():
    global rec_data
    ret, frame = cap.read()
    
    if ret:
        decoded_data = decode(frame)
        
        # If QR code is detected, extract the data
        if decoded_data:
            try:
                data = decoded_data[0].data.decode('utf-8')  # Properly decode QR data
                if data != rec_data:
                    print(data)
                    rec_data = data  # Update the global rec_data with the new QR code data
            except:
                pass
        
        # Update the label with the latest rec_data
        coordinate_label.config(text=f"QR Data: {rec_data}")
        
        # Convert frame from BGR to RGB for Tkinter display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Refresh the video feed every 10ms
    video_label.after(10, update_video)

# Tkinter window setup
root = Tk()

# Label to display the QR code data (needs to be defined before calling update_video)
coordinate_label = tk.Label(root, text=f"QR Data: {rec_data}", font=22)
coordinate_label.place(x=700, y=100)

# Label to display the video stream
video_label = tk.Label(root)
video_label.place(x=700, y=200, width=800, height=600)

# Start updating the video
update_video()

# Arrow buttons (placeholders)
left_arrow = ImageTk.PhotoImage(Image.open("left-arrow.png"))
right_arrow = ImageTk.PhotoImage(Image.open("right-arrow.png"))
down_arrow = ImageTk.PhotoImage(Image.open("down-arrow.png"))
up_arrow = ImageTk.PhotoImage(Image.open("up-arrow.png"))

# Position arrow buttons
left_button = tk.Button(root, image=left_arrow)
left_button.place(x=0, y=200)
right_button = tk.Button(root, image=right_arrow)
right_button.place(x=300, y=200)
up_button = tk.Button(root, image=up_arrow)
up_button.place(x=150, y=0)
down_button = tk.Button(root, image=down_arrow)
down_button.place(x=150, y=400)

# Fullscreen setup and bind ESC to exit fullscreen
root.attributes('-fullscreen', True)

root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Ensure proper release of the webcam on closing
def on_closing():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
