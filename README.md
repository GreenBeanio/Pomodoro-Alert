# Pomodoro-Alert
## What Does It Do?
Follows a pomodoro ultradian rhythm. When clicking the start button it calculates the time and schedule. Every time the activity switches it will make a noise. You click the sound button to stop the sound. Clicking stop with restart the program, so be careful about that.

## Reason For Creation
This program was made for me to try and use the pomodoro time schedule.
There were two different day types. Both have 1 hours lunch breaks. The difference is that one has 8 work hours and the other has 7 work hours.
## Running The Python Script
### Windows
- Initial Run
    - cd /your/folder
    - python3 -m venv env
    - call env/Scripts/activate.bat
    - python3 -m pip install -r requirements.txt
    - python3 Pomodoro_Alerts.py
- Running After
    - cd /your/folder
    - call env/Scripts/activate.bat && python3 Pomodoro_Alerts.py
- Running Without Terminal Staying Around
    - Change the file type from py to pyw
    - You should just be able to click the file to launch it
    - May need to also change python3 to just python if it doesn't work after the change
        - In the first line of the code change python3 to python
### Linux
- Initial Run
    - cd /your/folder
    - python3 -m venv env
    - source env/bin/activate
    - python3 -m pip install -r requirements.txt
    - python3 Pomodoro_Alerts.py
- Running After
    - cd /your/folder
    - source env/bin/activate && python3 Pomodoro_Alerts.py
- Running Without Terminal Staying Around
    - Run the file with nohup
    - May have to set executable if it's not already
        - chmod +x Pomodoro_Alerts.py