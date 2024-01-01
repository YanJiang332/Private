# coding="utf-8"
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
floderpath = filedialog.askdirectory()


path = floderpath + "/"
new_path_write = path + "output.csv"
first_line = "sysname, is-name, result\n"
with open(new_path_write, "w") as title:
    title.write(first_line)
    title.close()
files = os.listdir(path)
for file in files:
    new_path = path + file
    if "log" not in file:
        pass
    else:
        with open(new_path, encoding='utf-8', errors='ignore') as configration:
            #lines = configration.readlines()
            for line in configration.readlines():
                if "sysname " in line:
                    sysname = line.replace("sysname ", "").replace("\n","")
                elif "router id" in line or "mpls lsr-id" in line:
                    ip = line.replace("router id", "").replace("mpls lsr-id", "").replace("\n", "")
                    # print(ip)
                elif " is-name " in line:
                    is_name = line.replace(" is-name ", "").replace("\n","")
                    if sysname == is_name:
                        result = "ok"
                    else:
                        result = "nok"
                    info = f"{sysname},{ip},{is_name},{result}\n"
                    # print(info)
                    with open(new_path_write, "a+") as info_write:
                        info_write.write(info)