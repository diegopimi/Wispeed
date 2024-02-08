The intention of this project is to create an **app that is capable of reading and registering wifi (upload and download speeds) of a network periodically or at user-specified times/frequency**.

Ideally the app should **return results in a graphical manner** and should have a **nice user interface**. 

**THIS PROJECT HAS A LONG WAY TO GO**


**----------- SETUP -----------** 
Install MongoDB -> Create "DBPimi" database -> add "WiSpeed" Collection

Run these commands in CMD:
  -  pip install speedtest-cli
  -  pip install flask-pymongo


**REQUIREMENTS / TO-DO LIST** (Not in order):

- The user shall be able to specify the frequency of readings. For example, the user can ask for readings to occur every 25 minutes, every 30 seconds, every day, or any other.
- The user shall be able to specify the time and date in which readings occur. For example February 20th at 5:00 PM and 9:59 PM.
- The app shall keep count of number of readings and reading ID.
- Results shall be presented graphically after every reading, alongside a progress bar or indication of readings left.
- The app shall count with a professional looking user-interface.
- Evaluate efficiency and accuracy of test.
