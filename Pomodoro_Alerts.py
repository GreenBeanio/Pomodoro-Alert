#!/usr/bin/env python3
# region Imports
from datetime import datetime
from genericpath import exists
import sys
from time import time
import simpleaudio as sa
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QGridLayout,
    QRadioButton,
    QMessageBox,
)
from PyQt6.QtGui import QIcon
import os
import json

# endregion
# region Variables
##### Variables #####
curent_status = ""  # For Current Task
state = False  # F=False, T=On
hour_type = "8"  # 8, 7, P, R
sound = True  # T=Make Sound, F=No Sound
mute = False  # Used to force off sound
toggle_color = True  # Toggle if colors can change or not
paused = False  # Toggle if paused or not
time_until_next = 0
elapsed_time = 0
elapsed_work = 0
elapsed_break = 0
elapsed_start = 0
elapsed_lunch = 0
elapsed_finished = 0
next_status = ""
next_time = 0
total_steps = 0
current_step = 0
current_time = 0
next_time = 0
prompt_result = ""
total_steps_repeat = 0
current_step_repeat = 0
start_time = 0
total_elapsed_time = 0
end_time = 0
# Directories
directory_path = os.path.dirname(os.path.realpath(__file__))
path_to_8hr = directory_path + "/Data/8hr.json"
path_to_7hr = directory_path + "/Data/7hr.json"
path_to_pomodoro = directory_path + "/Data/pomodoro.json"
path_to_repeat = directory_path + "/Data/repeat.json"
path_to_icon = directory_path + "/Data/icon.ico"
path_to_start = directory_path + "/Data/Start.wav"
path_to_work = directory_path + "/Data/Work.wav"
path_to_break = directory_path + "/Data/Break.wav"
path_to_lunch = directory_path + "/Data/Lunch.wav"
path_to_finished = directory_path + "/Data/Finished.wav"
path_to_save = directory_path + "/Export/"
path_to_save_file = directory_path + "/Export/Save_Data.json"
# Audio Clips
start_aduio = sa.WaveObject.from_wave_file(path_to_start)
work_audio = sa.WaveObject.from_wave_file(path_to_work)
break_audio = sa.WaveObject.from_wave_file(path_to_break)
lunch_audio = sa.WaveObject.from_wave_file(path_to_lunch)
finished_audio = sa.WaveObject.from_wave_file(path_to_finished)
# Data
time_data = {}
# endregion
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


### Toggling on the mute or unmute option ###
def Toggle_Mute():
    global mute
    global sound
    if mute == False:
        mute = True
        sound = (
            False  # Setting this false just incase sound is currently playing it stops
        )
        Mute_Button.setText("Un-Mute")
    else:
        mute = False
        Mute_Button.setText("Mute")


### Toggline Pause ###
def Toggle_Pause():
    if state == True:
        global paused
        if paused == False:
            paused = True
            Pause_Button.setText("Un-Pause")
        else:
            paused = False
            Pause_Button.setText("Pause")
            # Getting the math for the pause
            Pause_Time()
    Change_Color()


### Toggling on or off if the color can switch ###
def Toggle_Color():
    global toggle_color
    if toggle_color == True:
        toggle_color = False
        Color_Button.setText("No Color")
    else:
        toggle_color = True
        Color_Button.setText("Color")
    Change_Color()


### Stopping the Sound To Indicate you are switching tasks ###
def Stop_Sound():
    global sound
    if sound == True:
        sound = False


### Check the confirmaton box ###
def Confirmation_Box(button):
    global prompt_result
    prompt_result = button.text()


### Box for asking if the user really wants to stop ###
def Stop_Box():
    # Reset promp results
    global prompt_result
    prompt_result = ""
    # Dialouge box to confirm you want to stop
    dialog = QMessageBox(text="This will reset the time. Are you sure?", parent=window)
    dialog.setWindowTitle("Confirmation")
    dialog.setIcon(QMessageBox.Icon.Question)
    dialog.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    dialog.buttonClicked.connect(Confirmation_Box)
    dialog.exec()


### Box for asking if the user wants to save their results
def Save_Box():
    # Reset promp results
    global prompt_result
    prompt_result = ""
    # Dialouge box to confirm you want to save
    dialog = QMessageBox(text="Do you wish to save your results?", parent=window)
    dialog.setWindowTitle("Save")
    dialog.setIcon(QMessageBox.Icon.Question)
    dialog.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    dialog.buttonClicked.connect(Confirmation_Box)
    dialog.exec()


### Saving the user data ###
def Save_Data():
    # Convert to date format
    export_start_time = datetime.fromtimestamp(start_time).strftime(
        "%Y/%m/%d, %H:%M:%S"
    )
    export_end_time = datetime.fromtimestamp(end_time).strftime("%Y/%m/%d, %H:%M:%S")
    # Convert to time format
    export_total_elapsed_time = datetime.utcfromtimestamp(total_elapsed_time).strftime(
        "%H:%M:%S"
    )
    export_elapsed_time = datetime.utcfromtimestamp(elapsed_time).strftime("%H:%M:%S")
    export_work_time = datetime.utcfromtimestamp(elapsed_work).strftime("%H:%M:%S")
    export_break_time = datetime.utcfromtimestamp(elapsed_break).strftime("%H:%M:%S")
    export_lunch_time = datetime.utcfromtimestamp(elapsed_lunch).strftime("%H:%M:%S")
    export_starting_time = datetime.utcfromtimestamp(elapsed_start).strftime("%H:%M:%S")
    export_finished_time = datetime.utcfromtimestamp(elapsed_finished).strftime(
        "%H:%M:%S"
    )
    # Covnert Hour Type
    if hour_type == "8":
        export_type = "8 Hours"
    elif hour_type == "7":
        export_type = "7 Hours"
    elif hour_type == "P":
        export_type = "Pomodoro"
    elif hour_type == "R":
        export_type = "Repeating"
    # Create dictionary
    pre_data = {
        "Start Time": export_start_time,
        "End Time": export_end_time,
        "Total Elapsed Time": export_total_elapsed_time,
        "Elapsed Time": export_elapsed_time,
        "Pomodoro Type": export_type,
        "Work Time": export_work_time,
        "Break Time": export_break_time,
        "Lunch Time": export_lunch_time,
        "Starting Time": export_starting_time,
        "Finished Time": export_finished_time,
    }
    # Check if the directory exists
    if not exists(path_to_save):
        os.mkdir(path_to_save)
    # Checking if the file exists
    if not exists(path_to_save_file):
        new_file = open(path_to_save_file, "x")
        new_file.close()
    # Opening file
    with open(path_to_save_file, "r") as outputfile:
        # loading previous file
        try:
            loaded_data = json.load(outputfile)
        except:
            loaded_data = {}
        # Getting length of data
        data_length = len(loaded_data)
        outputfile.close()
    # Saving file
    with open(path_to_save_file, "w") as outputfile:
        # Making export data
        export_data = {data_length + 1: pre_data}
        # Adding to the laoded data
        loaded_data.update(export_data)
        # Saving the data
        json.dump(loaded_data, outputfile, sort_keys=False, indent=4)
        outputfile.close()


### Toggling Pomodoro ###
def Toggle_Pomodoro():
    # Set Hour Type
    global hour_type
    # Set state and Buttons
    global state
    if state == False:
        # Setting everything
        if _8hr_Radio.isChecked() == True:
            hour_type = "8"
            _8hr_Radio.setCheckable(True)
            _7hr_Radio.setCheckable(False)
            Pomodoro_Radio.setCheckable(False)
            Repeat_Radio.setCheckable(False)
        elif _7hr_Radio.isChecked() == True:
            hour_type = "7"
            _8hr_Radio.setCheckable(False)
            _7hr_Radio.setCheckable(True)
            Pomodoro_Radio.setCheckable(False)
            Repeat_Radio.setCheckable(False)
        elif Pomodoro_Radio.isChecked() == True:
            hour_type = "P"
            _8hr_Radio.setCheckable(False)
            _7hr_Radio.setCheckable(False)
            Pomodoro_Radio.setCheckable(True)
            Repeat_Radio.setCheckable(False)
        elif Repeat_Radio.isChecked() == True:
            hour_type = "R"
            _8hr_Radio.setCheckable(False)
            _7hr_Radio.setCheckable(False)
            Pomodoro_Radio.setCheckable(False)
            Repeat_Radio.setCheckable(True)
        Pomodoro_Button.setText("Stop")
        # Getting information
        Gather_Data()
        # Starting the main loop
        state = True
        timer.start(1000)
    else:
        # Dialouge box to confirm you want to stop
        Stop_Box()
        if prompt_result == "&Yes":
            # Stopping the main loop
            timer.stop()
            state = False
            # Setting everything back
            Pomodoro_Button.setText("Start")
            _8hr_Radio.setCheckable(True)
            _7hr_Radio.setCheckable(True)
            Pomodoro_Radio.setCheckable(True)
            Repeat_Radio.setCheckable(True)
            Pomodoro_Radio.setCheckable(True)
            if hour_type == "8":
                _8hr_Radio.setChecked(True)
                _7hr_Radio.setChecked(False)
                Pomodoro_Radio.setChecked(False)
                Repeat_Radio.setChecked(False)
            elif hour_type == "7":
                _8hr_Radio.setChecked(False)
                _7hr_Radio.setChecked(True)
                Pomodoro_Radio.setChecked(False)
                Repeat_Radio.setChecked(False)
            elif hour_type == "P":
                _8hr_Radio.setChecked(False)
                _7hr_Radio.setChecked(False)
                Pomodoro_Radio.setChecked(True)
                Repeat_Radio.setChecked(False)
            elif hour_type == "R":
                _8hr_Radio.setChecked(False)
                _7hr_Radio.setChecked(False)
                Pomodoro_Radio.setChecked(False)
                Repeat_Radio.setChecked(True)
            # Checking if the user wants to export the results
            Save_Box()
            if prompt_result == "&Yes":
                Save_Data()
            # Initializing everything back to the start
            Init_Time()


# region GUI Setup
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
Pomodoro_Button = QPushButton("Start", parent=window)  # Dynamic
Sound_Button = QPushButton("Sound", parent=window)  # Static
Mute_Button = QPushButton("Mute", parent=window)  # Dynamic
Color_Button = QPushButton("Color", parent=window)  # Dynamic
Pause_Button = QPushButton("Pause", parent=window)  # Dynamic
Elapsed_Work_Text_Label = QLabel("Elapsed Work:", parent=window)  # Static
Elapsed_Work_Label = QLabel("Elapsed Work", parent=window)  # Dynamic
Elapsed_Break_Text_Label = QLabel("Elapsed Break:", parent=window)  # Static
Elapsed_Break_Label = QLabel("Elapsed Break", parent=window)  # Dynamic
_7hr_Radio = QRadioButton("7 Hour Day", parent=window)  # Static
_8hr_Radio = QRadioButton("8 Hour Day", parent=window)  # Static
Pomodoro_Radio = QRadioButton("Pomodoro", parent=window)  # Static
Repeat_Radio = QRadioButton("Repeat", parent=window)  # Static
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
layout.addWidget(Elapsed_Work_Text_Label, 6, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Work_Label, 6, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Break_Text_Label, 6, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Elapsed_Break_Label, 6, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(_8hr_Radio, 7, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(_7hr_Radio, 7, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Pomodoro_Radio, 7, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Repeat_Radio, 7, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Pomodoro_Button, 8, 0, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Pause_Button, 8, 1, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Sound_Button, 8, 2, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Mute_Button, 8, 3, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(Color_Button, 8, 4, alignment=Qt.AlignmentFlag.AlignCenter)
# Default Selection
_8hr_Radio.setChecked(1)
### Button Events ###
# Toggling Pomodoro
Pomodoro_Button.clicked.connect(Toggle_Pomodoro)
# Pause Button
Pause_Button.clicked.connect(Toggle_Pause)
# Stopping the sound
Sound_Button.clicked.connect(Stop_Sound)
# Toggling Mute
Mute_Button.clicked.connect(Toggle_Mute)
# Toggling Color
Color_Button.clicked.connect(Toggle_Color)
# endregion
### Changing color of window ###
def Change_Color():
    current_color = ""
    if toggle_color == True:
        if paused == False:
            if current_status == "Start":
                current_color = "lightpink"
            elif current_status == "Work":
                current_color = "mediumspringgreen"
            elif current_status == "Break":
                current_color = "mediumturquoise"
            elif current_status == "Lunch":
                current_color = "thistle"
            elif current_status == "Finished":
                current_color = "salmon"
            else:
                current_color = "lightgray"
        else:
            current_color = "mediumorchid"
    else:
        current_color = "lightgray"
    window.setStyleSheet(f"background-color: {current_color}")


### Load JSON Data ###
def Load_Time():
    good_path = ""
    if hour_type == "8":
        good_path = path_to_8hr
    elif hour_type == "7":
        good_path = path_to_7hr
    elif hour_type == "P":
        good_path = path_to_pomodoro
    elif hour_type == "R":
        good_path = path_to_repeat
    with open(good_path) as temp_file:
        loaded_time = json.load(temp_file)
    return loaded_time


### Formatting Time ###
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


### Remaking the Paused Data ###
def Pause_Time():
    # Global data
    global time_data
    global next_time
    # Get time from JSON
    unformatted = Load_Time()
    total_time = 0
    total_seconds = 0
    temp_current_time = datetime.now().timestamp() - elapsed_time
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
    # Making the formatted new data to time data
    time_data.clear()
    time_data = formatted.copy()
    # Getting fixed next_time
    next_time = time_data[current_step]["Time"]


### Data Collection ###
def Gather_Data():
    # Setting Variables
    global current_status
    global hour_type
    global current_time
    global current_step
    global next_time
    global sound
    global paused
    global time_until_next
    global elapsed_time
    global elapsed_work
    global elapsed_break
    global elapsed_start
    global elapsed_lunch
    global elapsed_finished
    global next_status
    global time_data
    global total_steps
    # Setting basic Variables
    if _8hr_Radio.isChecked() == True:
        hour_type = "8"
    elif _7hr_Radio.isChecked() == True:
        hour_type = "7"
    elif Pomodoro_Radio.isChecked() == True:
        hour_type = "P"
    elif Repeat_Radio.isChecked() == True:
        hour_type = "R"
    sound = False
    paused = False
    current_time = datetime.now().timestamp()
    elapsed_time = 0
    elapsed_work = 0
    elapsed_break = 0
    elapsed_start = 0
    elapsed_lunch = 0
    elapsed_finished = 0
    current_status = ""
    current_step = 0
    next_time = 0
    time_until_next = 0
    next_status = ""
    # Get time from json
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
    Elapsed_Work_Label.setText("Not Started")
    Elapsed_Break_Label.setText("Not Started")
    # Setting Variables
    global current_status
    global state
    global hour_type
    global current_time
    global current_step
    global next_time
    global sound
    global paused
    global time_until_next
    global elapsed_time
    global elapsed_work
    global elapsed_break
    global elapsed_start
    global elapsed_lunch
    global elapsed_finished
    global next_status
    global time_data
    global total_steps
    global prompt_result
    global total_steps_repeat
    global current_step_repeat
    global start_time
    global total_elapsed_time
    global end_time
    current_status = ""
    state = False
    Pomodoro_Button.setText("Start")
    if _8hr_Radio.isChecked() == True:
        hour_type = "8"
    elif _7hr_Radio.isChecked() == True:
        hour_type = "7"
    elif Pomodoro_Radio.isChecked() == True:
        hour_type = "P"
    elif Repeat_Radio.isChecked() == True:
        hour_type = "R"
    current_time = 0
    current_step = 0
    next_time = 0
    sound = False
    paused = False
    Pause_Button.setText("Pause")
    time_until_next = 0
    elapsed_time = 0
    elapsed_work = 0
    elapsed_break = 0
    elapsed_start = 0
    elapsed_lunch = 0
    elapsed_finished = 0
    next_status = ""
    time_data = {}
    total_steps = 0
    prompt_result = ""
    total_steps_repeat = 0
    current_step_repeat = 0
    start_time = 0
    total_elapsed_time = 0
    end_time = 0
    Change_Color()


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
    global elapsed_work
    global elapsed_break
    global elapsed_start
    global elapsed_lunch
    global elapsed_finished
    global next_status
    global start_time
    global total_elapsed_time
    global end_time
    # Setting time and elapsed time
    if current_step <= total_steps:
        current_time = datetime.now().timestamp()
        # Tracking specifc times
        if current_step > 0:
            elapsed_time += 1
            # Tracking specifc times
            if current_status == "Work":
                elapsed_work += 1
            elif current_status == "Break":
                elapsed_break += 1
            elif current_status == "Lunch":
                elapsed_lunch += 1
            elif current_status == "Start":
                elapsed_start += 1
            elif current_status == "Finished":
                elapsed_finished += 1
        else:
            start_time = current_time
    # Getting time data
    if current_time >= next_time and current_step < total_steps:
        current_step += 1
        current_status = time_data[current_step]["Type"]
        next_time = time_data[current_step]["Time"]
        if current_step != total_steps:
            next_status = time_data[current_step + 1]["Type"]
        # If not muted play the sound
        if mute == False:
            sound = True
        # Change the color
        Change_Color()
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
        display_elapsed_work = datetime.utcfromtimestamp(elapsed_work).strftime(
            "%H:%M:%S"
        )
        display_elapsed_break = datetime.utcfromtimestamp(elapsed_break).strftime(
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
        Elapsed_Work_Label.setText(str(display_elapsed_work))
        Elapsed_Break_Label.setText(str(display_elapsed_break))
        # True elapsed time & endtime
        total_elapsed_time = round(current_time - start_time)
        end_time = current_time


#### Trying this to test repeating #####
def Repeat_Time():
    # global variables
    global current_status
    global current_time
    global current_step
    global next_time
    global sound
    global time_until_next
    global elapsed_time
    global elapsed_work
    global elapsed_break
    global elapsed_start
    global elapsed_lunch
    global elapsed_finished
    global next_status
    global current_step_repeat
    global total_steps_repeat
    global start_time
    global total_elapsed_time
    global end_time
    # Setting time and elapsed time
    if current_step <= total_steps:
        current_time = datetime.now().timestamp()
        if total_steps_repeat <= total_steps:
            total_steps_repeat = total_steps
        if current_step > 0:
            elapsed_time += 1
            # Tracking specifc times
            if current_status == "Work":
                elapsed_work += 1
            elif current_status == "Break":
                elapsed_break += 1
            elif current_status == "Lunch":
                elapsed_lunch += 1
            elif current_status == "Start":
                elapsed_start += 1
            elif current_status == "Finished":
                elapsed_finished += 1
        else:
            start_time = current_time
    # Getting time data
    if current_time >= next_time and current_step < total_steps:
        current_step += 1
        current_step_repeat += 1
        current_status = time_data[current_step]["Type"]
        next_time = time_data[current_step]["Time"]
        if current_step != total_steps:
            next_status = time_data[current_step + 1]["Type"]
        # If not muted play the sound
        if mute == False:
            sound = True
        # Change the color
        Change_Color()
    # doing this to stop the labels
    elif current_time >= next_time and current_step == total_steps:
        current_step = 1
        current_step_repeat += 1
        total_steps_repeat += total_steps
        current_status = time_data[current_step]["Type"]
        next_time = time_data[current_step]["Time"]
        if current_step != total_steps:
            next_status = time_data[current_step + 1]["Type"]
        if mute == False:
            sound = True
        # Change the color
        Change_Color()
    # Writing Labels and Time Until Next
    # Getting Time until next
    time_until_next = next_time - current_time
    if time_until_next < 0:
        time_until_next = 0
    # Convert times to good looking
    display_current_time = datetime.fromtimestamp(current_time).strftime("%H:%M:%S")
    display_elapsed_time = datetime.utcfromtimestamp(elapsed_time).strftime("%H:%M:%S")
    display_elapsed_work = datetime.utcfromtimestamp(elapsed_work).strftime("%H:%M:%S")
    display_elapsed_break = datetime.utcfromtimestamp(elapsed_break).strftime(
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
    Current_Step_Label.setText(str(current_step_repeat))
    Total_Step_Label.setText(str(total_steps_repeat))
    Next_Status_Label.setText(next_status)
    Elapsed_Work_Label.setText(str(display_elapsed_work))
    Elapsed_Break_Label.setText(str(display_elapsed_break))
    # True elapsed time & endtime
    total_elapsed_time = round(current_time - start_time)
    end_time = current_time


###### Main Timer Logic ######
def Timing():
    # Pause Sate
    if paused == False:
        # Check time
        if hour_type != "R":
            Check_Time()
        else:
            Repeat_Time()
        # Play sound
        if sound == True:
            Play_Audio(current_status)


# region Initializing Everything
Init_Time()
### Timer for Repeated Events & Running This###
timer = QTimer()
timer.timeout.connect(Timing)
window.setWindowIcon(QIcon(path_to_icon))
### Showing the application and window ###
window.setLayout(layout)
window.setMinimumSize(window.minimumSizeHint())
window.setMaximumSize(window.sizeHint())
window.show()
sys.exit(app.exec())
# endregion
