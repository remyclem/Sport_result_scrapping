# coding: utf-8

import os
from gtts import gTTS
import vlc
import tempfile

from tkinter.messagebox import *
from tkinter.filedialog import *

from scraping import basket_ball_request


class AppGui(Frame):
    """Main window.
    All widgets are stored as attributes in this window."""

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

        # save file frame
        self.browse_csv_frame = LabelFrame(self, text="Save file", padx=20, pady=20)
        self.browse_csv_frame.pack(fill="both")

        self.browse_button = Button(self.browse_csv_frame, text="Browse", command=self.browse_button)
        self.browse_button.pack()

        # fetch frame
        self.summary_frame = LabelFrame(self, text="Fetch data", padx=20, pady=20)
        self.summary_frame.pack(fill="both", expand="yes")

        self.quit_button = Button(self.summary_frame, text="Fetch!", command=self.fetch_data_button)
        self.quit_button.pack()


    def alert(self):
        showinfo("Alert", "In case of problem call Remy")


    def browse_button(self):
        print("titi")
        self.csv_path = asksaveasfilename()
        print(self.csv_path)


    def fetch_data_button(self):
        basketball_results_history_csv = os.path.join("/", "home", "remy", "workspace",
                                                      "Sport_result_scrapping",
                                                      "scrapped_data",
                                                      "basketball_history.csv")

        print(self.csv_path)

        basket_ball_request(self.csv_path)

        # TTS feature for fun
        language = "en"
        tempMp3file = os.path.join(tempfile.gettempdir(), "mission_accomplished.mp3")
        tts = gTTS(text='Mission accomplished!', lang=language)
        tts.save(tempMp3file)
        p = vlc.MediaPlayer(tempMp3file)
        p.play()



