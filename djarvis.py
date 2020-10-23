import winreg as reg
import os
import pyttsx3
import SpeechRecognition as sr
import datetime
import wikipedia
import json
import webbrowser as wb
import subprocess

from pip._vendor.distlib.compat import raw_input

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # two voices available on sapi5

running = True
data = {}


def AddToRegistry():
    # in python __file__ is the instant of
    # file path where it was executed
    # so if it was executed from desktop,
    # then __file__ will be
    # c:\users\current_user\desktop
    pth = os.path.dirname(os.path.realpath(__file__))

    # name of the python file with extension
    s_name = "djarvis.py"

    # joins the file name to end of path address
    address = os.path.join(pth, s_name)
    #print(address)

    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    # open the key to make changes to
    open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

    # modifiy the opened key
    reg.SetValueEx(open, "any_name", 0, reg.REG_SZ, address)

    # now close the opened key
    reg.CloseKey(open)


# Driver Code
AddToRegistry()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()  # wait to get audio


def time():
    speak("Welcome back!")
    Time = datetime.datetime.now().strftime("%I:%M:%S")  # hour:min:sec
    print(Time)
    speak(f"The current time is {str(Time)}")


def wiki():
    query = input("What would you like to search?")
    results = wikipedia.summary(query, sentences=2)
    speak("according to wikipedia")
    print(results)
    speak(results)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again...")
        speak("Say that again...")
        return "None"
    return query


def takeText():
    return input("choose")


def startCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        #print(f"You said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again...")
        #speak("Say that again...")
        return "None"
    return query


def saveData(newdata):
    with open("djarvis.txt", "w") as f:  # in write mode
        f.write("{}".format(json.dumps(newdata)))


def loadData():
    with open("djarvis.txt") as f:  # in read mode, not in write mode, careful
        rd = f.readlines()
        return json.loads(rd[0])


def startApp(path):
    print("Opening app...")
    subprocess.call(path)
    print("App opened")


def openSite(url):
    print("Opening site...")
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    wb.get(chrome_path).open(url)
    print("Site opened")


def add():
    pass

def chooseOption(options):
    action = takeCommand()
    if action == "Add":
        add()
        return "None"
    chosen = False

    while not chosen:
        for i in options:
            if action == i:
                action = i
                chosen = True
                break
    if data[action].len() > 1:
        speak("More Specific?")
        for i in data[action]:
            print(i)
        chooseOption(data[action])
    else:
        return data[action]


data = {
   "Develop": [
      {
         "Unity": [
            {
               "App":"C:\\Program Files\\Unity Hub\\Unity Hub.exe"
            }
         ]
      },
      {
         "React": [
            {
               "Web": "http://localhost:3000"
            },
            {
               "App": "C:\\Users\\Cornelius\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            }
         ]
      }
   ]
}

choices = []
choices = data["Develop"]

openArr = []

"""choice = input("choose:\n")
for i in choices:
    for j in list(i.keys()):
        if j == choice:
            openArr = i[j]
            for k in openArr:
                if list(k.keys())[0] == "App":
                    startApp(list(k.values())[0])
                elif list(k.keys())[0] == "Web":
                    openSite(list(k.values())[0])"""

while running:
    command = startCommand()
    if command.upper() == "open".upper():
        speak("What would you like to do today?")
        cmdFin = False
        while not cmdFin:
            for key in choices:
                print(list(key.keys()))
            speak("Your options are listed here")
            chosen = takeCommand()
            for i in choices:
                for j in list(i.keys()):
                    if j.upper() == chosen.upper():
                        openArr = i[j]
                        cmdFin = True
                        for k in openArr:
                            if list(k.keys())[0] == "App":
                                startApp(list(k.values())[0])
                            elif list(k.keys())[0] == "Web":
                                openSite(list(k.values())[0])



