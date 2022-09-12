#!/usr/bin/python3

__author__ = 'piper'
__version__ = '1.0'

from tkinter import *
from tkinter.scrolledtext import ScrolledText
# import win32api,win32con

# hkey=win32api.RegCreateKey(win32con.HKEY_CURRENT_USER,"Software\\Microsoft\\Windows\\CurrentVersion\\Run")
# win32api.RegSetValueEx(hkey,'Scratch',0,win32con.REG_SZ,(os.getcwd()+"\\scratch.pyw"))
# win32api.RegCloseKey(hkey)

root = Tk()
screen_width = root.winfo_screenwidth()
width = screen_width - 250
root.geometry("+%d+0" % width)
# root.overrideredirect(1)
# root.attributes('-alpha', 0.7)
root['background'] = '#161a1d'
root.title('ScratchPad')

textpad = ScrolledText(root, background='#161a1d', highlightthickness=0,
                       fg='#fdfffc', height=11, width=40)
textpad['font'] = 'cursive 10 normal'
textpad.grid(column=0, row=0, rowspan=10, sticky=NSEW)

# grip = Label(root, bitmap='gray25')
# grip.grid(column=1, row=0, sticky=NE)

# close_button = Label(root, text='X', fg='#9fd477')
# close_button['background'] = root['background']
# close_button['font'] = 'Forte 11 normal'
# close_button.grid(column=1, row=8, sticky=SE)


def load():
    import os
    filename = 'scratch.nt'
    files = os.listdir(os.getcwd())
    if filename in files:
        file = open(filename, 'r')
        data = file.read()
        file.close()
    else:
        file = open('scratch.nt', 'w+')
        file.write('')
        data = file.read()
        file.close()
        
    textpad.insert('1.0', data)


def save(e):
    data = textpad.get('1.0', END)
    file = open('scratch.nt', 'w')
    file.write(data)
    file.close()


def focus_in(e):
    textpad['highlightthickness'] = 1


def focus_out(e):
    save(e)
    textpad['highlightthickness'] = 0
    
# def hover(event):
#    close_button['fg'] = 'red'

# def leave(event):
#    close_button['fg'] = '#9fd477'

# def close(event):
#    root.destroy()

# def startMove(event):
#    x = event.x
#    y = event.y

# def stopMove(event):
#    x = None
#    y = None

# def onMotion(event):
#    deltax = event.x
#    deltay = event.y
#    x = root.winfo_x()+deltax
#    y = root.winfo_y()+deltay
#    root.geometry("+%s+%s" %(x, y))

load()

# close_button.bind('<Enter>', hover)
# close_button.bind('<Leave>', leave)
# close_button.bind('<Button-1>', close)

textpad.bind('<FocusIn>', focus_in)
textpad.bind('<FocusOut>', focus_out)
textpad.bind('<Return>', save)

# grip.bind('<ButtonPress-1>', startMove)
# grip.bind('<ButtonRelease-1>', stopMove)
# grip.bind('<B1-Motion>', onMotion)
root.mainloop()
