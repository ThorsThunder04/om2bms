import tkinter as tk
import om2bms_osz
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
import os, shutil
import json


global toConvert, settings, root

# constants
global WIDTH, HEIGHT
WIDTH, HEIGHT = 500, 350
BG_COLOR = "#f1bcfc"
BUTTON_COLOR = "#a7e0fc"


settings = json.load(open("./settings.json", "r"))
root = tk.Tk()
root.title("OM2BMS Converter")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(width=False, height=False)
toConvert = []


def updateFileList():
    global toConvert, fileListBox
    fileListBox.config(state="normal")
    fileListBox.delete(1.0, tk.END)
    for k,file in enumerate(toConvert): # go over each path, get the filename, display it to text field
        filename = os.path.basename(file)
        formattedString = f"({k+1}){filename[filename.index('-')+2:-4]}"
        if len(formattedString) > 30:
            formattedString = formattedString[:27] + "..."
        fileListBox.insert(tk.END, formattedString + "\n")
    fileListBox.config(state="disabled")

def getfileslist():
    global toConvert
    # get a list of selected songs to convert
    lst = askopenfilenames()
    for file in lst:
        if os.path.isfile(file) and file.endswith(".osz") and file not in toConvert:
            toConvert.append(file)
    # print(toConvert)
    updateFileList()

def clearToConvert():
    global toConvert
    toConvert = []
    updateFileList()
    print("Queue List Cleared")

def deleteOutputDir():
    global settings
    shutil.rmtree(settings["custom"]["set_default_out"])
    print("Output Directory Cleared")

def loadFromInputDirectory():
    global toConvert, settings 
    for file in os.listdir(settings["custom"]["in_file"]):
        path = os.path.join(settings["custom"]["in_file"] ,file)
        if os.path.isfile(path) and path.endswith(".osz") and path not in toConvert:
            toConvert.append(path)

    updateFileList()
    print("Loaded from Input Folder")

def convertFiles():
    global settings, toConvert

    while len(toConvert) > 0:
        runSettings = settings["custom"].copy()
        runSettings["in_file"] = toConvert.pop(0) 
        # print(runSettings)
        om2bms_osz.convert(**runSettings)
    print("Conversion Complete!")
    updateFileList()

def load_main_widgets(parent):
    global fileListBox, outputDirLabelVar
    frame = tk.Frame(parent, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
    
    # creation of widgets and inner frames
    outputDirLabelVar = tk.StringVar(value="Current output folder:\n"+settings["custom"]["set_default_out"])
    outputDirLabel = tk.Label(frame, textvariable=outputDirLabelVar, justify="left", bg="#e7a3f4")
    fileListBox = tk.Text(frame, width=30, height=13)
    browseButton = tk.Button(frame, text="Browse Files", command=getfileslist, bg=BUTTON_COLOR)
    loadFromInputButton = tk.Button(frame, text="Load Input Directory", command=loadFromInputDirectory, bg=BUTTON_COLOR)
    clearQueueButton = tk.Button(frame, text="Clear Selected", background="#fa7867", fg="#000000", command=clearToConvert)
    deleteOutputDirButton = tk.Button(frame, text="Delete Output Files", background="#fa7867", fg="#000000", command=deleteOutputDir)
    convertButton = tk.Button(frame, text="Convert", background="#b3fa74", command=convertFiles, font=("Times New Roman", 15))
    #TODO must clear queue after converting

    # place the frame
    frame.grid(column=0, row=0)

    # placement of widgets
    fileListBox.place(x=WIDTH//2, y=35)
    browseButton.place(x=WIDTH//2, y=8)
    loadFromInputButton.place(x=WIDTH//2 + 80, y=8)
    clearQueueButton.place(x=WIDTH//2, y=HEIGHT - 92)
    convertButton.place(x=20, y = HEIGHT-HEIGHT//4)
    deleteOutputDirButton.place(x=20, y = 60)
    outputDirLabel.place(x=20, y=90)

    fileListBox.config(state="disabled")
    return frame


def applyConfig():
    global configObjectList, settings, outputDirLabelVar
    in_file, set_default_out, offset, judge, video, bg, hitsound = configObjectList
    settings["custom"] = {
        "in_file":in_file.get(),
        "set_default_out":set_default_out.get(),
        "hitsound":hitsound.get(),
        "bg":bg.get(),
        "video":video.get(),
        "offset":offset.get(),
        "judge":judge.get()
    }
    outputDirLabelVar.set("Current output folder:\n"+settings["custom"]["set_default_out"])

def saveConfig():
    applyConfig()
    json.dump(settings, open("settings.json", "w"), indent=2)

def resetConfigToDefault():
    global settings, configObjectList

    settings["custom"] = settings["default"].copy()
    for obj, string in zip(configObjectList, ("in_file", "set_default_out", "offset", "judge", "video", "bg", "hitsound")):
        value = settings["custom"][string]
        obj.set(False if value is None else value)

def load_config_widgets(parent):
    global settings, configObjectList

    frame = tk.Frame(parent, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
    frame.grid(column=0, row=0)

    in_file = tk.StringVar(value=settings["custom"]["in_file"])
    set_default_out = tk.StringVar(value=settings["custom"]["set_default_out"])
    offset = tk.IntVar(value=settings["custom"]["offset"])
    judge = tk.IntVar(value=settings["custom"]["judge"])
    video = tk.BooleanVar(value=settings["custom"]["video"])
    bg = tk.BooleanVar(value=settings["custom"]["bg"])
    hitsound = tk.BooleanVar(value=settings["custom"]["hitsound"])
    configObjectList = [in_file, set_default_out, offset, judge, video, bg, hitsound]

    inFileField = tk.Entry(frame, textvariable=in_file)
    inFileLabel = tk.Label(frame, text="Input Directory", bg=BG_COLOR)
    outFileField = tk.Entry(frame, textvariable=set_default_out)
    outFileLabel = tk.Label(frame, text="Output Directory", bg=BG_COLOR)
    offsetField = tk.Spinbox(frame, textvariable=offset)
    offsetLabel = tk.Label(frame, text="Audio Offset", bg=BG_COLOR)
    judgeField = tk.Spinbox(frame, from_=0, to=5, textvariable=judge)
    judgeLabel = tk.Label(frame, text="Judgement", bg=BG_COLOR)
    videoField = tk.Checkbutton(frame, text="Convert Video", variable=video, onvalue=True, offvalue=False, bg=BG_COLOR)
    bgField = tk.Checkbutton(frame, text="Resize/Convert Background", variable=bg, onvalue=True, offvalue=False, bg=BG_COLOR)
    hitsoundField = tk.Checkbutton(frame, text="Convert Hitsounds", variable=hitsound, onvalue=True, offvalue=False, bg=BG_COLOR)

    applyButton = tk.Button(frame, text="Apply", command=applyConfig, bg=BUTTON_COLOR)
    saveButton = tk.Button(frame, text="Save", command=saveConfig, bg=BUTTON_COLOR)
    resetButton = tk.Button(frame, text="Reset", command=resetConfigToDefault, bg=BUTTON_COLOR)


    inFileField.place(x=110, y=10)
    inFileLabel.place(x=20, y=10)
    outFileField.place(x=120, y=40)
    outFileLabel.place(x=20, y=40)
    offsetField.place(x=95, y=70)
    offsetLabel.place(x=20, y=70)
    judgeField.place(x=90, y=100)
    judgeLabel.place(x=20, y=100)
    hitsoundField.place(x=20, y=130)
    bgField.place(x=20, y=160)
    videoField.place(x=20, y=190)

    saveButton.place(x=WIDTH-60, y=HEIGHT-60)
    applyButton.place(x=WIDTH-120, y=HEIGHT-60)
    resetButton.place(x=WIDTH-60, y=20)

    # frame.pack(expand=True, fill="both")
    return frame

if __name__ == "__main__":

    tabControl = ttk.Notebook(root)
    tabControl.pack(expand=True, fill="both")

    mainFrame = load_main_widgets(tabControl)
    configFrame = load_config_widgets(tabControl)

    tabControl.add(mainFrame, text="MainMenu")
    tabControl.add(configFrame, text="Config")

    root.mainloop()
