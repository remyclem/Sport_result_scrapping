# coding: utf-8


from gui import *


main_window = Tk()
main_window.title("Fetch from oddsportal")

app = AppGui(main_window)

main_window.mainloop()
main_window.destroy()