from pygame import mixer
from registr import *
from tkinter import *
import sys
from game import *
from PIL import ImageTk, Image

windowEntry = Tk()
mixer.init()
windowEntry.title('Homm')
mixer.music.load('Data/bgmusic.mp3')
mixer.music.play(loops=-1)
mixer.music.set_volume(0.0)


def Main_menu():
    button_image_start = PhotoImage(file='Data/start.png')
    button_image_settings = PhotoImage(file='Data/settings.png')
    button_image_exit = PhotoImage(file='Data/exit.png')

    img = Image.open('Data/bg.png')
    width = 800
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height), Image.ANTIALIAS)
    background = ImageTk.PhotoImage(imag)
    bg = Label(windowEntry, image=background)
    bg.pack()

    button_play = Button(windowEntry, image=button_image_start, border='0',
                         command=lambda: startdagame())
    button_settings = Button(windowEntry, image=button_image_settings, border='0',
                             command=lambda: Options([bg, button_exit, button_play, button_settings]))
    button_exit = Button(windowEntry, image=button_image_exit, border='0', command=sys.exit)
    button_play.place(x=600, y=250)
    button_settings.place(x=600, y=300)
    button_exit.place(x=600, y=350)
    windowEntry.resizable(False, False)
    windowEntry.iconbitmap('Data/ms.ico')
    windowEntry.eval('tk::PlaceWindow . center')
    windowEntry.mainloop()


def get_ready(Buttons, a=0):
    if a == 0:
        for i in Buttons:
            i.destroy()
    elif a == 1:
        for i in Buttons:
            i.destroy()
        Main_menu()
    else:
        for i in Buttons:
            i.destroy()
        mixer.music.stop()


def Options(Buttons):
    get_ready(Buttons, 0)
    v = DoubleVar()
    v.set(mixer.music.get_volume() * 100)

    img = Image.open('Data/bg.png')
    width = 800
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height), Image.ANTIALIAS)
    background = ImageTk.PhotoImage(imag)
    bg = Label(windowEntry, image=background)
    bg.pack()

    button_back_image = PhotoImage(file='Data/back.png')
    button_back = Button(windowEntry, image=button_back_image, border='0',
                         command=lambda: get_ready([bg, button_back, scale_music], 1))
    scale_music = Scale(windowEntry, variable=v, from_=0, to=100, orient=HORIZONTAL,
                        border='0', length=183, label='Громкость музыки')
    scale_music.bind("<Motion>", lambda e: mixer.music.set_volume(v.get() * 0.01))

    button_back.place(x=300, y=250)
    scale_music.place(x=300, y=300)

    windowEntry.mainloop()


def startdagame():
    windowEntry.destroy()
    Game()


Main_menu()
