import datetime
import subprocess


def note(text):
    date = datetime.datetime.now()
    filename = "Notes/" + str(date).replace(":", "-") + "-note.txt"
    with open(filename, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", filename])
