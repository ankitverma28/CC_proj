import csv
import hashlib
import os
import tkinter as tk
from collections import defaultdict
from tkinter import ttk, filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Duplicacy')
        self.geometry('900x700')
        self.configure(bg='DodgerBlue2')

        # label
        self.label = ttk.Label(self, text='Find duplicate files in a folder',font='100',foreground='white',background='dodgerblue2')
        self.label.pack()

        # button
        self.button = tk.Button(self, text='Click to select  a folder',bg="white",foreground='black',font='20')
        self.button['command'] = self.button_clicked
        self.button.pack()



    def button_clicked(self):
        self.command=self.destroy()


def generate_md5(fname, chunk_size=1024):
    """
    Function which takes a file name and returns md5 checksum of the file
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        # Read the 1st block of the file
        chunk = f.read(chunk_size)
        # Keep reading the file until the end and update hash
        while chunk:
            hash.update(chunk)
            chunk = f.read(chunk_size)

    # Return the hex checksum
    return hash.hexdigest()


if __name__ == "__main__":
    app = App()
    app.mainloop()
    # The dict will have a list as values
    md5_dict = defaultdict(list)

    file_types_inscope = [ "ppt", "pptx", "pdf", "txt", "html",
                           "mp4", "jpg", "png", "xls", "xlsx", "xml",
                           "vsd", "py", "json" ]

    # Walk through all files and folders within directory
    root = tk.Tk()
    root.withdraw()
    new=filedialog.askdirectory()
    for path, dirs, files in os.walk(new):
        print("Analyzing {}".format(path))
        for each_file in files:
            if each_file.split(".")[ -1 ].lower() in file_types_inscope:
                # The path variable gets updated for each subfolder
                file_path = os.path.join(os.path.abspath(path), each_file)
                # If there are more files with same checksum append to list
                md5_dict[ generate_md5(file_path) ].append(file_path)

    # Identify keys (checksum) having more than one values (file names)
    duplicate_files = (
        val for key, val in md5_dict.items() if len(val) > 1)

    # Write the list of duplicate files to csv file
    with open("duplicates.csv", "w") as log:
        # Lineterminator added for windows as it inserts blank rows otherwise
        csv_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL, delimiter=",",
                                lineterminator="\n")
        header = [ "File Names" ]
        csv_writer.writerow(header)

        for file_name in duplicate_files:
            csv_writer.writerow(file_name)

    print("Done")


