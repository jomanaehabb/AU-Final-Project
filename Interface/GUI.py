import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from pyzbar.pyzbar import decode 
import paho.mqtt.client as mqtt


ip_webcam_url = 'http://192.168.1.4:8080/video'
# cap = cv2.VideoCapture(ip_webcam_url)  # Initialize video capture
rec_data = "none"
# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqttBroker = "92b2787cd70e4ecbbc692c1a48a92520.s1.eu.hivemq.cloud"
# Connect to the MQTT Broker
mqtt_client.connect(mqttBroker, port=8883)
direction=''
def publish_command(command):
    if mqtt_client.is_connected():
        print(f"Publishing command: {command}")
        mqtt_client.publish("robot/control", command)
    else:
        print("MQTT client is not connected!")

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

def arrowsHide(right_button, left_button, up_button, down_button, direction):
    # Hide all buttons first
    up_button.place_forget()
    down_button.place_forget()
    left_button.place_forget()
    right_button.place_forget()

    # Show the button according to the direction
    if direction == "Up":
        up_button.place(x=150, y=0)
        publish_command("Up")
    elif direction == "Down":
        down_button.place(x=150, y=200)
        publish_command("Down")
    elif direction == "Left":
        left_button.place(x=0, y=200)
        publish_command("Left")
    elif direction == "Right":
        right_button.place(x=300, y=200)
        publish_command("Right")

def on_key_press(event):
    # Map key presses to directions
    global direction
    if event.keysym == 'w':
        direction = "Up"
    elif event.keysym == 's':
        direction = "Down"
    elif event.keysym == 'a':
        direction = "Left"
    elif event.keysym == 'd':
        direction = "Right"
    else:
        direction = None

    # Call arrowsHide with the determined direction
    if direction:
        arrowsHide(right_button, left_button, up_button, down_button, direction)
def on_key_release(event):
    # Hide all buttons when any of the control keys is released
    if event.keysym in ['w', 's', 'a', 'd']:
        arrowsHide(right_button, left_button, up_button, down_button, None)
# Tkinter window setup
root = Tk()

# Label to display the QR code data
coordinate_label = tk.Label(root, text=f"QR Data: {rec_data}", font=22)
coordinate_label.place(x=700, y=100)

# Label to display the video stream
video_label = tk.Label(root)
video_label.place(x=700, y=200, width=800, height=600)

# Start updating the video
#update_video()  

# Arrow buttons images
left_arrow = ImageTk.PhotoImage(Image.open("left-arrow.png"))
right_arrow = ImageTk.PhotoImage(Image.open("right-arrow.png"))
down_arrow = ImageTk.PhotoImage(Image.open("down-arrow.png"))
up_arrow = ImageTk.PhotoImage(Image.open("up-arrow.png"))

# Arrow buttons
left_button = tk.Button(root, image=left_arrow)
right_button = tk.Button(root, image=right_arrow)
up_button = tk.Button(root, image=up_arrow)
down_button = tk.Button(root, image=down_arrow)



# Fullscreen setup and bind ESC to exit fullscreen
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)
# Ensure proper release of the webcam on closing
# def on_closing():
#    cap.release()  # Release the webcam
#    root.destroy()  # Destroy the Tkinter window

# root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
mqtt_client.disconnect()