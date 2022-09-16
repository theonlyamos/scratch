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
        self.bg = '#161a1d'
        self.fg = '#fdfffc'

        height = master.winfo_height()
        screen_width = master.winfo_screenwidth()
        width = screen_width - (self.width*2)
        
        self.geometry(f"+%d+0" % width)
        self.minsize(width=self.width, height=40)
        self['background'] = 'black'
        self.overrideredirect(1)
        self.attributes('-alpha', 0.7)

        self.selected = ''
        self.content()
    
    def content(self):
        '''
        CheckList components
        '''
        add_menu_frame = Frame(
            self,
            bg=self.bg
        )

        new_note_btn = Button(
            add_menu_frame,
            text='Note',
            bg=self.bg,
            fg=self.fg,
            font=('Consolas', 10, 'normal'),
            command=lambda: self.set_selected(item='note')
        )
        
        new_note_btn.bind('<Enter>', self.hover)
        new_note_btn.bind('<Leave>', self.leave)
        new_note_btn.pack(side=LEFT, ipady=5, fill=X, expand=True)

        new_checklist_btn = Button(
            add_menu_frame,
            text='CheckList',
            bg=self.bg,
            fg=self.fg,
            font=('Consolas', 10, 'normal'),
            command=lambda: self.set_selected(item='checklist')
        )

        new_checklist_btn.bind('<Enter>', self.hover)
        new_checklist_btn.bind('<Leave>', self.leave)
        new_checklist_btn.pack(side=LEFT, ipady=5, fill=X, expand=True)

        new_event_btn = Button(
            add_menu_frame,
            text='Event',
            bg=self.bg,
            fg=self.fg,
            font=('Consolas', 10, 'normal'),
            command=lambda: self.set_selected(item='event')
        )

        new_event_btn.bind('<Enter>', self.hover)
        new_event_btn.bind('<Leave>', self.leave)
        new_event_btn.pack(side=LEFT, ipady=5, fill=X, expand=True) 

        new_reminder_btn = Button(
            add_menu_frame,
            text='Reminder',
            bg=self.bg,
            fg=self.fg,
            font=('Consolas', 10, 'normal'),
            command=lambda: self.set_selected(item='reminder')
        )

        new_reminder_btn.bind('<Enter>', self.hover)
        new_reminder_btn.bind('<Leave>', self.leave)
        new_reminder_btn.pack(side=LEFT, ipady=5, fill=X, expand=True)       

        add_menu_frame.pack(padx=2, fill=X, expand=True)

    def set_selected(self, item: str):
        '''
        Set selected item type
        '''
        self.selected = item
        self.destroy()
    
    def hover(self, event=None):
        '''
        Change background and foreground color on mouse enter
        '''
        event.widget.configure(bg='black')

    def leave(self, event=None):
        '''
        Revert background and foreground color to default
        '''
        event.widget.configure(bg=self.bg)
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.selected