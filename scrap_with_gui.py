# coding: utf-8

import os
from gtts import gTTS
import vlc
import tempfile

import tkinter.ttk as ttk
from tkinter.messagebox import *
from tkinter.filedialog import *

from scraping import basket_ball_request


class AppGui(Frame):
    """Main window"""

    def __init__(self, master, **kwargs):

        Frame.__init__(self, master=None, relief=SUNKEN, background="white", bd=2, **kwargs)
        self.pack(fill=BOTH)

        self.csv_path = ""

        # menus
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.menu1)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="About", command=self.alert)
        self.menubar.add_cascade(label="help", menu=self.menu2)

        self.master.config(menu=self.menubar)

        # tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand='yes')
        self.tab1 = Frame();
        self.notebook.add(self.tab1, text='Basketball')

        # save file frame
        self.browse_csv_frame = LabelFrame(self.tab1, text="Save file", padx=20, pady=20)
        self.browse_csv_frame.pack(fill="both")

        self.browse_button = Button(self.browse_csv_frame, text="Browse", command=self.browse_button)
        self.browse_button.pack()

        self.csv_path_label = Label(self.browse_csv_frame, text=self.csv_path)
        self.csv_path_label.pack(side="left")

        # fetch frame
        self.fetch_frame = LabelFrame(self.tab1, text="Fetch data", padx=20, pady=20)
        self.fetch_frame.pack(fill="both", expand="yes")

        self.var_case = IntVar()
        self.case = Checkbutton(self.fetch_frame, text="tell when finished", variable=self.var_case)
        self.case.pack()

        self.quit_button = Button(self.fetch_frame, text="Fetch!", command=self.fetch_data_button)
        self.quit_button.pack()


    def alert(self):
        showinfo("Info", "In case of problem call Remy")


    def browse_button(self):
        self.csv_path = asksaveasfilename()
        print(self.csv_path)
        self.csv_path_label["text"] = self.csv_path


    def fetch_data_button(self):

        if self.csv_path == "":
            showinfo("Alert", "You need to select a path for the csv file")
            return None

        basket_ball_request(self.csv_path)

        if self.var_case.get() > 0:  # TTS feature for fun
            language = "en"
            tempMp3file = os.path.join(tempfile.gettempdir(), "mission_accomplished.mp3")
            tts = gTTS(text='Mission accomplished!', lang=language)
            tts.save(tempMp3file)
            p = vlc.MediaPlayer(tempMp3file)
            p.play()


if __name__ == '__main__':
    main_window = Tk()
    main_window.title("Fetch from oddsportal")

    app = AppGui(main_window)

    main_window.mainloop()
    main_window.destroy()