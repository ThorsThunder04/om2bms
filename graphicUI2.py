import PySimpleGUI as sg
import os, shutil, json
import om2bms_osz

def main_menu_tab():
    layout = [
        [sg.Text("File Converter", font=("Calibrie", 25))],
        [sg.Listbox([], key="-TO_CONVERT_LIST-", size=(35, 7))],
        [sg.Input(key="-ADD_FILES-", visible=False, enable_events=True), sg.FilesBrowse("Add Files"), sg.Button("Clear Files", key="-CLEAR_FILES-"), sg.Button("Convert", key="-CONVERT-")]
    ]

    return layout

def apply_settings(values_dict):
    global main_settings
    main_settings["custom"] = {
        "in_file": values_dict["-CONFIG_INPUTV-"],
        "set_default_out": values_dict["-CONFIG_OUTPUTV-"],
        "offset": values_dict["-CONFIG_OFFSETV-"],
        "judge": values_dict["-CONFIG_JUDGEMENTV-"],
        "video": values_dict["-CONFIG_VIDEOV-"],
        "bg": values_dict["-CONFIG_BGV-"],
        "hitsound": None if not values_dict["-CONFIG_HITSOUNDV-"] else True
    }
    print("Settings Applied!")

def save_settings(values_dict):
    global main_settings
    apply_settings(values_dict)
    json.dump(main_settings, open("settings.json", "w"), indent=4)
    print("Settings Saved!")

def reset_settings(windowObj):
    global main_settings
    def_conf = main_settings["default"]
    windowObj["-CONFIG_INPUTV-"].update(def_conf["in_file"])
    windowObj["-CONFIG_OUTPUTV-"].update(def_conf["set_default_out"])
    windowObj["-CONFIG_OFFSETV-"].update(def_conf["offset"])
    windowObj["-CONFIG_JUDGEMENTV-"].update(def_conf["judge"])
    windowObj["-CONFIG_VIDEOV-"].update(def_conf["video"])
    windowObj["-CONFIG_BGV-"].update(def_conf["bg"])
    windowObj["-CONFIG_HITSOUNDV-"].update(not (def_conf["hitsound"] in (False, None)))
    print("Settings Reset!")


def config_tab():
    global main_settings
    curr_conf = main_settings["custom"]
    layout = [
        [sg.Text("Input Directory"), sg.Input(curr_conf["in_file"], key="-CONFIG_INPUTV-"), sg.FolderBrowse()],
        [sg.Text("Output Directory"), sg.Input(curr_conf["set_default_out"], key="-CONFIG_OUTPUTV-"), sg.FolderBrowse()],
        [sg.Text("Audio Offset"), sg.Spin(list(range(-1000, 1001)), curr_conf["offset"], key="-CONFIG_OFFSETV-")],
        [sg.Text("Judgement"), sg.Spin(list(range(-1000, 1001)), curr_conf["judge"], key="-CONFIG_JUDGEMENTV-")],
        [sg.Checkbox("Convert Video", curr_conf["video"], key="-CONFIG_VIDEOV-")],
        [sg.Checkbox("Resize/Convert Background", curr_conf["bg"], key="-CONFIG_BGV-")],
        [sg.Checkbox("Convert Hitsounds", not (curr_conf["hitsound"] in (False, None)), key="-CONFIG_HITSOUNDV-")],
        [sg.Button("Apply", key="-CONFIG_APPLY-"), sg.Button("Save", key="-CONFIG_SAVE-"), sg.Button("Reset", key="-CONFIG_RESET-")]
    ]

    return layout


def createWindow():
    # here we call config_tab() and main_menu_tab() that will return layouts. Then we load the layout into the window.
    final_layout = [
        [sg.TabGroup([[sg.Tab("MainMenu", main_menu_tab()), sg.Tab("Config", config_tab())]])]
    ]
    return sg.Window("om2bms GUI", final_layout)

global main_settings
main_settings = json.load(open("settings.json", "r"))
window = createWindow()
convertq = []

def convert_maps(settings, queue):

    while len(queue) > 0:
        settings["in_file"] = queue.pop()
        om2bms_osz.convert(**settings)

    print("Conversion Complete!")




while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "-ADD_FILES-":
        newfiles = [] # formatted filenames for the list display
        filesList = values["-ADD_FILES-"].split(";")
        for file in filesList:
            if file.endswith(".osz"):
                convertq.append(file)
                file = os.path.basename(file)[:-4]
                file = file[file.find(" ")+1:]
                newfiles.append(file)
        window["-TO_CONVERT_LIST-"].update(values["-TO_CONVERT_LIST-"] + newfiles) 
        print(f"{len(newfiles)} maps added to queue")

    elif event == "-CLEAR_FILES-":
        convertq = []
        window["-TO_CONVERT_LIST-"].update([])
        print("Cleared map conversion queue")

    elif event == "-CONVERT-":

        window["-CONVERT-"].update(disabled=True)
        tmp_settings = main_settings["custom"].copy()
        print(f"Converting {len(convertq)} maps")
        while len(convertq) > 0:
            tmp_settings["in_file"] = convertq.pop()
            om2bms_osz.convert(**tmp_settings)
        print("Conversion Complete!")
        window["-CONVERT-"].update(disabled=False)
        window["-TO_CONVERT_LIST-"].update([])

    elif event == "-CONFIG_APPLY-":
        apply_settings(values)
    elif event == "-CONFIG_SAVE":
        save_settings(values)
    elif event == "-CONFIG_RESET-":
        reset_settings(window)

window.close()