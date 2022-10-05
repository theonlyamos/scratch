from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor

from toolbar import ToolBar

class Note(Toplevel):
    '''
    New Note Window
    '''

    def __init__(self, master=None, posX=0, posY=0, width=250, text='', bg = '#161a1d', fg = '#fdfffc', locked=False, is_withdrawn=False,  **kw):
        super().__init__(master, **kw)
        self.width = width
        self.text = text
        self.bg = bg
        self.fg = fg
        self.posX = posX
        self.posY = posY
        self.locked= locked
        self.is_withdrawn = is_withdrawn

        self.geometry(f"{width}x200+%d+%d" % (posX, posY))

        self['background'] = '#161a1d'
        self.overrideredirect(1)
        self.attributes('-alpha', 0.7)

        self.content()
    
    def to_object(self)->dict:
        '''
        Convert to object for saving
        '''
        return {
            'type': 'note',
            'posX': self.winfo_x(),
            'posY': self.winfo_y(),
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'bg': self.bg,
            'fg': self.fg,
            'text': self.textpad.get('1.0', END),
            'locked': self.locked,
            'is_withdrawn': self.is_withdrawn
        }
    
    def bg_color(self, event=None):
        '''
        Choose color from color picker
        '''
        color = askcolor(color=self.bg, title='Select Color')
        self.bg = color[1]
        self.textpad.configure(bg=self.bg)
        self.bg_btn.configure(bg=self.bg)
    
    def fg_color(self, event=None):
        '''
        Choose color from color picker
        '''
        color = askcolor(color=self.fg, title='Select Color')
        self.fg = color[1]
        self.textpad.configure(fg=self.fg)
        self.fg_btn.configure(bg=self.fg)
    
    def content(self):
        '''
        Widgets for creating new note
        '''

        top_frame = ToolBar(
            self,
            bg='grey60'
        )

        self.bg_btn = Button(
            top_frame, 
            text='',
            width=1,
            height=1,
            bg=self.bg,
            command=self.bg_color
        )
        self.bg_btn.pack(side=LEFT, anchor=W, padx=5, pady=5)

        self.fg_btn = Button(
            top_frame, 
            text='',
            width=1,
            height=1,
            bg=self.fg,
            command=self.fg_color
        )
        self.fg_btn.pack(side=LEFT, anchor=W, padx=5, pady=5)

        top_frame.pack(side=TOP, fill=X)

        self.textpad = Text(
            self, 
            background=self.bg, 
            highlightthickness=0,
            fg=self.fg, 
            font=('Lucida Console', 10, 'normal'),
            height=11, 
            borderwidth=0,
            padx=5,
            pady=5
        )

        self.textpad.bind('<FocusOut>', self.focus_out)
        self.textpad.insert('1.0', self.text)
        self.textpad.pack(side=TOP, fill=BOTH, expand=True)
    
    def focus_out(self, event=None):
        self.master.save()
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.text