import os

directory = './input'
file_type = input("Are you converting osz or osu: ").lower().strip()


for filename in os.scandir(directory):
    if filename.is_file():
        if file_type == 'osz' and filename.path.split(".")[-1] == "osz":
            # print(filename.path)
            os.system("python om2bms_osz.py -i \"" + filename.path + "\"")
        else:
            os.system("python om2bms.py -i /" + filename.path + "/")
