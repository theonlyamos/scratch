from tkinter import *
from tkinter import ttk

from toolbar import ToolBar
from checkitem import CheckItem

class AddMenu(Toplevel):
    '''
    New CheckList Window
    '''

    def __init__(self, master=None, width=250, **kw):
        super().__init__(master, **kw)
        self.width = width
        height = master.winfo_height()
        screen_width = master.winfo_screenwidth()
        width = screen_width - (self.width*2)
        
        self.geometry(f"+%d+0" % width)

        self.minsize(width=self.width, height=40)
        
        self['background'] = '#161a1d'
        self.overrideredirect(1)
        self.bg = '#161a1d'
        self.fg = '#fdfffc'

        self.selected = ''
        self.content()
    
    def content(self):
        '''
        CheckList components
        '''
        add_menu_frame = Frame(
            self
        )

        ttk.Button(
            add_menu_frame,
            text='New Note',
            command=lambda: self.set_selected(item='note')
        ).pack(fill=X)

        ttk.Button(
            add_menu_frame,
            text='New CheckList',
            command=lambda: self.set_selected(item='checklist')
        ).pack(fill=X)

        ttk.Button(
            add_menu_frame,
            text='New Event',
            command=lambda: self.set_selected(item='event')
        ).pack(fill=X)

        add_menu_frame.pack(fill=X, expand=True)

    def set_selected(self, item: str):
        '''
        Set selected item type
        '''
        self.selected = item
        self.destroy()
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.selected