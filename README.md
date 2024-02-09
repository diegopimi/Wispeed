The intention of this project is to create an **app that is capable of reading and registering wifi (upload and download speeds) of a network periodically or at user-specified times/frequency**.

Ideally the app should **return results in a graphical manner** and should have a **nice user interface**. 

**THIS PROJECT HAS A LONG WAY TO GO**


**----------- SETUP -----------** 

Install MongoDB -> Create "DBPimi" database -> add "WiSpeed" Collection
(make sure to also have MongoDB Compass)

Run these commands in CMD:
  -  pip install speedtest-cli
  -  pip install flask-pymongo
  -  have the following folder structure C:\Program Files\MongoDB\data\db (db should be an empty folder)

Clone repository

**----------- HOW TO RUN -----------**

1. Open cmd and type 'mongod' to start an instance of MongoDB
2. Open MongoDB Compass and connect to uri 'mongodb://localhost:27017/'
3. Open the code project in VSCode and in the terminal type 'python app.py'
4. In a browser, go to 'http://127.0.0.1:5000/'
5. Click the button to read wifi speeds. It takes a bit for the readings to occur, reload the page after a couple minutes and you should see the table being populated. 

**----------------------------------**

**REQUIREMENTS / TO-DO LIST** (Not in order):

- The user shall be able to specify the frequency of readings. For example, the user can ask for readings to occur every 25 minutes, every 30 seconds, every day, or any other.
- The user shall be able to specify the time and date in which readings occur. For example February 20th at 5:00 PM and 9:59 PM.
- The app shall keep count of number of readings and reading ID.
- Results shall be presented graphically after every reading, alongside a progress bar or indication of readings left.
- The app shall count with a professional looking user-interface and animations. (Website and app deployment?) 
- Evaluate efficiency and accuracy of test.
- Input validation, no room for crashing.
- Follow consistent coding standards.
- Create UML and following documentation and proper design. 
