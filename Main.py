from pynput import keyboard
from threading import Thread
import pyLOUS

bip="255.255.255.255"
port=6969

class Reciever(Thread):
    def __init__(self):

        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        global port,othersData
        receiver = pyLOUS.LOUS_Receiver("", port)
        receiver.start()
        olddata=""
        while True:
            data = receiver.last("")
            if (data and data!=olddata):
                #print(data.decode("utf-8"))
                othersData.append(data.decode("utf-8"))
                olddata=data

record = False
shift = False
alt_l = False
caps = False
alt_data=""

data = ""
othersData=[]
position = 0
values = dict({"`": "~", "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(",
     "0": ")", "-": "_", "=": "+",
     "[": "{", "]": "}", ";": ":", "'": "\"", ",": "<", ".": ">", "/": "?"})

def insertChar(chartoinsert):
    global record,data,position
    if (record == True):
        data = data[:position] + chartoinsert + data[position:]
        position += 1

def removeChar():
    global record, data, position
    if (record == True):
        data = data[:position - 1] + data[position:]
        position -= 1

def on_press(key):
    global record,position,shift,alt_l,caps,values,alt_data
    try:
        key.char
        if (shift == True):
            try:
                insertChar(values[key.char])
            except:
                if (key.char.isalpha()):
                    if (caps):
                        insertChar(key.char.lower())
                    else:
                        insertChar(key.char.upper())
        elif (alt_l == True):
            if (key.char == "r"):
                record = True
            elif (key.char == "p"):
                record = False
            elif (key.char == "s"):
                #print(data)
                sender = pyLOUS.LOUS_Sender()
                global bip,port
                sender.send(data.encode(), (bip, port))
            elif (key.char == "l"):
                alt_data="l"
            elif (key.char.isdigit()):
                alt_data += key.char

        else:
            insertChar(key.char)

    except AttributeError:
        if (key.name == "shift"):
            shift = True
        elif (key.name == "alt_l"):
            alt_l = True
        elif (key.name == "alt_l"):
            caps != caps
        elif (key.name == "space"):
            insertChar(" ")
        elif (key.name == "tab"):
            insertChar("\t")
        elif (key.name == "backspace"):
            removeChar()
        elif (key.name == "enter"):
            insertChar("\n")
        elif (key.name == "left"):
            if (position != 0):
                position -= 1
        elif (key.name == "right"):
            if (position != len(data)):
                position += 1
        elif (key.name == "up"):
            pass
        elif (key.name == "down"):
            pass

def on_release(key):
    global shift, alt_l
    try:
        key.char

    except AttributeError:
        if (key.name == "shift"):
            shift = False
        elif (key.name == "alt_l"):
            alt_l = False
            global alt_data,othersData
            if(alt_data == "l"):
                typeData(str(len(othersData)))
            elif(alt_data.isnumeric()):
                try:
                    typeData(othersData[int(alt_data)])
                except:
                    pass
            alt_data=""

def typeData(data):
    #print(data)
    controller = keyboard.Controller()
    controller.type(data)

Reciever()
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
