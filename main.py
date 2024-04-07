import serial
import time
from tkinter import *
from tkinter import messagebox

# Global variables to keep track of parking slot status and time
slot_status = [0, 0, 0]  # Assuming all slots are initially available
slot_start_time = [None, None, None]  # Keep track of start time for each slot
parking_rate_per_hour = 5  # Adjust the rate as needed


# Function to update parking slot status based on Arduino data
# Function to update parking slot status based on Arduino data
def update_status():
    global slot_status
    data = ser.readline().decode('ascii').strip()
    if len(data) == len(slot_status):
        for i in range(len(data)):
            if slot_status[i] != int(data[i]):
                if int(data[i]) == 0:
                    slot_start_time[i] = time.time()  # Record start time when slot becomes occupied
                else:
                    slot_start_time[i] = None  # Reset start time when slot becomes available
                slot_status[i] = int(data[i])
                update_labels()
                if int(data[i]) == 1:  # Check if the slot becomes available
                    messagebox.showinfo("Slot Empty", "Slot {} is now empty.".format(i+1))
    else:
        print("Received data length does not match expected length.")

    root.after(1000, update_status)



# Function to update GUI labels based on parking slot status
def update_labels():
    for i in range(len(slot_labels)):
        status = "Occupied" if slot_status[i] == 0 else "Available"
        if slot_status[i] == 0 and slot_start_time[i] is not None:
            duration = int(time.time() - slot_start_time[i])
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            slot_labels[i].config(text="Slot {}: {}, Duration: {}".format(i + 1, status, duration_str))
        else:
            slot_labels[i].config(text="Slot {}: {}".format(i + 1, status))


# Function to handle payment received for a parking slot
def pay(slot):
    if slot_status[slot - 1] == 0 and slot_start_time[slot - 1] is not None:
        end_time = time.time()
        duration = int(end_time - slot_start_time[slot - 1])
        hours = duration // 3600
        cost = parking_rate_per_hour * hours
        print("Payment received for Slot {}: ${}".format(slot, cost))
        messagebox.showinfo("Payment Received", "Payment received for Slot {}. You can go and park now.".format(slot))
        slot_status[slot - 1] = 1
        update_labels()
    else:
        print("Slot {} is not occupied or already paid for.".format(slot))


# Arduino Serial Communication
ser = serial.Serial('COM7', 9600)  # Change COM3 to your Arduino's port

# GUI Setup
root = Tk()
root.title("Parking Management System")
root.geometry("400x300")  # Fixed width and height

slot_labels = []
payment_buttons = []

for i in range(3):
    label = Label(root, text="Slot {}: Available".format(i + 1), width=30)
    label.pack()
    slot_labels.append(label)

    button = Button(root, text="Pay for Slot {}".format(i + 1), width=20, command=lambda i=i: pay(i + 1))
    button.pack()
    payment_buttons.append(button)

update_status()  # Start updating status from Arduino
root.mainloop()
