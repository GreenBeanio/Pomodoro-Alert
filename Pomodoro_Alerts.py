#!/usr/bin/env python3
from datetime import datetime
import sys
import simpleaudio as sa
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QGridLayout,
    QRadioButton,
)
from PyQt6.QtGui import QIcon
import os
import json

##### Variables #####
curent_status = ""  # For Current Task
state = False  # F=False, T=On
hour_type = True  # T=8hr, F=7hr
sound = True  # T=Make Sound, F=No Sound
time_until_next = 0
elapsed_time = 0
next_status = ""
next_time = 0
total_steps = 0
current_step = 0
current_time = 0
next_time = 0
# Directories
directory_path = os.path.dirname(os.path.realpath(__file__))
path_to_8hr = directory_path + "/Data/8hr.json"
path_to_7hr = directory_path + "/Data/7hr.json"
path_to_icon = directory_path + "/Data/icon.ico"
path_to_start = directory_path + "/Data/Start.wav"
path_to_work = directory_path + "/Data/Work.wav"
path_to_break = directory_path + "/Data/Break.wav"
path_to_lunch = directory_path + "/Data/Lunch.wav"
path_to_finished = directory_path + "/Data/Finished.wav"
# Audio Clips
start_aduio = sa.WaveObject.from_wave_file(path_to_start)
work_audio = sa.WaveObject.from_wave_file(path_to_work)
break_audio = sa.WaveObject.from_wave_file(path_to_break)
lunch_audio = sa.WaveObject.from_wave_file(path_to_lunch)
finished_audio = sa.WaveObject.from_wave_file(path_to_finished)
# Data
time_data = {}

##### Applicaiton Starting #####

### Plays audio based on the current task ###
def Play_Audio(current):
    if current == "Start":
        start_aduio.play()
    elif current == "Work":
        work_audio.play()
    elif current == "Break":
        break_audio.play()
    elif current == "Lunch":
        lunch_audio.play()
    elif current == "Finished":
        finished_audio.play()


### Stopping the Sound To Indicate you are switching tasks ###
def Stop_Sound():
    global sound
    if sound == True:
        sound = False


### Toggling Pomodoro ###
def Toggle_Pomodoro():
    # Set Hour Type
    global hour_type
    hour_type = _8hr_Radio.isChecked()
    # Set state and Buttons
    global state
    if state == False:
        state = True
        Pomodoro_Button.setText("Stop")
        Gather_Data()
        _8hr_Radio.setCheckable(False)
        _7hr_Radio.setCheckable(False)
        timer.start(1000)
    else:
        state = False
        Pomodoro_Button.setText("Start")
        Init_Time()
        _8hr_Radio.setCheckable(True)
        _7hr_Radio.setCheckable(True)
        timer.stop()


### Setting up Application ###
# Setting up application and window
app = QApplication([])
window = QWidget()
window.setWindowTitle("Pomodoro Alerts")

# Setting up a label and button
Pomodoro_Label = QLabel("<h1>Pomodoro</h1>", parent=window)  # Static
Current_Status_Text_Label = QLabel("Current Status:", parent=window)  # Static
Current_Status_Label = QLabel("Status", parent=window)  # Dynamic
Current_Time_Text_Label = QLabel("Current Time:", parent=window)  # Static
Current_Time_Label = QLabel("Time", parent=window)  # Dynamic
Time_Until_Next_Text_Label = QLabel("Time Until Next:", parent=window)  # Static
Time_Until_Next_Label = QLabel("Until", parent=window)  # Dynamic
Elapsed_Time_Text_Label = QLabel("Elapsed Time:", parent=window)  # Static
Elapsed_Time_Label = QLabel("Elapsed Time", parent=window)  # Dynamic
Current_Step_Text_Label = QLabel("Current Step:", parent=window)  # Static
Current_Step_Label = QLabel("Current Step", parent=window)  # Dynamic
Total_Step_Text_Label = QLabel("Total Steps:", parent=window)  # Static
Total_Step_Label = QLabel("Total Step", parent=window)  # Dynamic
Next_Status_Text_Label = QLabel("Next Status:", parent=window)  # Static
Next_Status_Label = QLabel("Next Status", parent=window)  # Dynamic
Next_Time_Text_Label = QLabel("Next Time:", parent=window)  # Static
Next_Time_Label = QLabel("Next Time", parent=window)  # Dynamic
Pomodoro_Button = QPushButton("Start", parent=window)  # Static
Sound_Button = QPushButton("Sound", parent=window)  # Static
_7hr_Radio = QRadioButton("7 Hour Day", parent=window)  # Static
_8hr_Radio = QRadioButton("8 Hour Day", parent=window)  # Static
# Laying it all out
layout = QGridLayout()
layout.addWidget(Pomodoro_Label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(
    Current_Status_Text_Label, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter
)
layout.addWidget(Current_Status_Label, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Current_Time_Text_Label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Current_Time_Label, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Time_Text_Label, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Time_Label, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(
    Time_Until_Next_Text_Label, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
)
layout.addWidget(Time_Until_Next_Label, 3, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Current_Step_Text_Label, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Current_Step_Label, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Total_Step_Text_Label, 4, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Total_Step_Label, 4, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Status_Text_Label, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Status_Label, 5, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Time_Text_Label, 5, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Next_Time_Label, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(_8hr_Radio, 6, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(_7hr_Radio, 6, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Pomodoro_Button, 7, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Sound_Button, 7, 2, alignment=Qt.AlignmentFlag.AlignCenter)
# Default Selection
_8hr_Radio.setChecked(1)
### Button Events ###
# Toggling Pomodoro
Pomodoro_Button.clicked.connect(Toggle_Pomodoro)
# Stopping the sound
Sound_Button.clicked.connect(Stop_Sound)

### Load JSON Data ###
def Load_Time():
    good_path = ""
    if hour_type == True:
        good_path = path_to_8hr
    else:
        good_path = path_to_7hr
    with open(good_path) as temp_file:
        loaded_time = json.load(temp_file)
    return loaded_time


def Format_Time():
    # Get time from JSON
    unformatted = Load_Time()
    total_time = 0
    total_seconds = 0
    temp_current_time = datetime.now().timestamp()
    formatted = {}
    # For each do math
    for x in unformatted:
        # Loading Data
        load_stage = int(x)
        load_type = unformatted[x]["Type"]
        load_time = int(unformatted[x]["Time"])
        # Math to get time
        to_seconds = load_time * 60
        total_seconds += to_seconds
        total_time = temp_current_time + total_seconds
        # Write to dictionary
        formatted[load_stage] = {"Type": load_type, "Time": total_time}
    return formatted


### Data Collection ###
def Gather_Data():
    # Setting Variables
    global current_status
    global state
    global hour_type
    global current_time
    global current_step
    global next_time
    global sound
    global time_until_next
    global elapsed_time
    global next_status
    global time_data
    global total_steps
    # Setting basic Variables
    state = True  # Yes
    hour_type = _8hr_Radio.isChecked()
    sound = False
    current_time = datetime.now().timestamp()
    elapsed_time = 0
    ######
    current_status = ""
    current_step = 0
    next_time = 0
    # next_time = 0
    time_until_next = 0
    next_status = ""
    ######
    # Get time from json and shit
    time_data = Format_Time()
    # Getting step info
    total_steps = len(time_data)


### Initializing everything ###
def Init_Time():
    # Setting Labels
    Current_Status_Label.setText("Not Started")
    Current_Time_Label.setText("Not Started")
    Elapsed_Time_Label.setText("Not Started")
    Time_Until_Next_Label.setText("Not Started")
    Current_Status_Label.setText("Not Started")
    Current_Time_Label.setText("Not Started")
    Current_Step_Label.setText("Not Started")
    Total_Step_Label.setText("Not Started")
    Next_Status_Label.setText("Not Started")
    Next_Time_Label.setText("Not Started")
    # Setting Variables
    global current_status
    global state
    global hour_type
    global current_time
    global current_step
    global next_time
    global sound
    global time_until_next
    global elapsed_time
    global next_status
    global time_data
    global total_steps
    current_status = ""
    state = False
    hour_type = _8hr_Radio.isChecked()
    current_time = 0
    current_step = 0
    next_time = 0
    sound = False
    time_until_next = 0
    elapsed_time = 0
    next_status = ""
    time_data = {}
    total_steps = 0


### Checking the Time ###
def Check_Time():
    # global variables
    global current_status
    global current_time
    global current_step
    global next_time
    global sound
    global time_until_next
    global elapsed_time
    global next_status
    # Setting time and elapsed time
    if current_step <= total_steps:
        current_time = datetime.now().timestamp()
        elapsed_time += 1
    # Getting time data
    if current_time >= next_time and current_step < total_steps:
        current_step += 1
        current_status = time_data[current_step]["Type"]
        next_time = time_data[current_step]["Time"]
        if current_step != total_steps:
            next_status = time_data[current_step + 1]["Type"]
        sound = True
    # doing this to stop the labels
    elif current_time >= next_time and current_step == total_steps:
        current_step += 1
    # Writing Labels and Time Until Next
    if current_step <= total_steps:
        # Getting Time until next
        time_until_next = next_time - current_time
        if time_until_next < 0:
            time_until_next = 0
        # Convert times to good looking
        display_current_time = datetime.fromtimestamp(current_time).strftime("%H:%M:%S")
        display_elapsed_time = datetime.utcfromtimestamp(elapsed_time).strftime(
            "%H:%M:%S"
        )
        display_time_until_next = datetime.utcfromtimestamp(time_until_next).strftime(
            "%H:%M:%S"
        )
        display_next_time_label = datetime.fromtimestamp(next_time).strftime("%H:%M:%S")
        # Writing Labels
        Current_Time_Label.setText(str(display_current_time))
        Elapsed_Time_Label.setText(str(display_elapsed_time))
        Time_Until_Next_Label.setText(str(display_time_until_next))
        Next_Time_Label.setText(str(display_next_time_label))
        Current_Status_Label.setText(current_status)
        Current_Step_Label.setText(str(current_step))
        Total_Step_Label.setText(str(total_steps))
        Next_Status_Label.setText(next_status)


###### Main Timer Logic ######
def Timing():
    # Check time
    Check_Time()
    # Play sound
    if sound == True:
        Play_Audio(current_status)


### Initializing Everything ###
Init_Time()
### Timer for Repeated Events & Running This###
timer = QTimer()
timer.timeout.connect(Timing)
###
window.setWindowIcon(QIcon(path_to_icon))
### Showing the application and window ###
window.setLayout(layout)
window.setMinimumSize(window.minimumSizeHint())
window.setMaximumSize(window.sizeHint())
window.show()
sys.exit(app.exec())
