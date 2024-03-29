from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor

from toolbar import ToolBar

class Settings(Toplevel):
    '''
    Settings Window
    '''

    def __init__(self, master=None, _id=None,  width=250,  **kw):
        super().__init__(master, **kw)
        self._id = _id
        self.width = width

        height = master.winfo_height()
        screen_width = master.winfo_screenwidth()
        width = (screen_width - (self.width*2))-10
        
        self.geometry(f"+%d+0" % width)
        self.minsize(width=self.width, height=200)
        self['background'] = 'black'
        self.overrideredirect(1)
        self.attributes('-alpha', 0.8)

        self.content()
    
    def content(self):
        '''
        Widgets for settings window
        '''

        top_frame = ToolBar(
            self,
            bg='grey60',
            lock_btn=False,
            close_cmd=self.master.toggle_settings
        )

        self.title = Label(
            top_frame,
            text='Settings',
            font='Consolas 14 bold',
            fg='black',
            bg='grey60'
        )
        self.title.pack(side=LEFT, anchor=W, padx=5, pady=5)

        top_frame.pack(side=TOP, fill=X)

    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.master.toggle_settings)
        self.wait_window(self)
        return True