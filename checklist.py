from tkinter import *

from toolbar import ToolBar
from checkitem import CheckItem

class CheckList(Toplevel):
    '''
    New CheckList Window
    '''

    def __init__(self, master=None, posX=0, posY=0, title='Title Here', width=250, items:list[dict]=[], text='', bg='#161a1d', fg='#fdfffc', **kw):
        super().__init__(master, **kw)
        self.items = items
        self.title = title
        self.posX = posX
        self.posY = posY
        
        self.geometry(f"+%d+%d" % (posX, posY))

        self.minsize(width=width, height=40)
        
        self.bg = bg
        self.fg = fg
        self['background'] = bg
        self.overrideredirect(1)
        self.attributes('-alpha', 0.7)
        self.text = text
        self.content()
    
    def to_object(self)->dict:
        '''
        Convert to object for saving
        '''
        items = []
        for key in self.children.keys():
            if '!checkitem' in key:
                items.append(self.children[key].to_object())
                
        return {
            'type': 'checklist',
            'posX': self.posX,
            'posY': self.posY,
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'title': self.title_var.get(),
            'bg': self.bg,
            'fg': self.fg,
            'text': self.text,
            'items': items
        }
    
    def content(self):
        '''
        CheckList components
        '''
        tools_frame = ToolBar(
            self,
            bg='black',
            add_btn=True,
            add_btn_command=self.add_item
        )

        self.title_var = StringVar(value=self.title)
        self.title_entry = Entry(
            tools_frame,
            textvariable=self.title_var,
            font='Consolas 10 bold',
            bg='black',
            fg='white',
            state='disabled',
            disabledforeground='white',
            disabledbackground='black',
            border=0
        )
        
        self.title_entry.bind('<Double-1>', self.focus_in)
        self.title_entry.bind('<FocusOut>', self.focus_out)
        self.title_entry.bind('<Return>', self.focus_out)
        self.title_entry.pack(side=LEFT, fill=X, ipady=5)
        
        tools_frame.pack(side=TOP, fill=X)

        for item in self.items:
            CheckItem(self, **item)
    
    def add_item(self, event=None):
        '''
        Add new checklist item
        '''
        item = {'label': '', 'checked': False}
        self.items.append(item)
        CheckItem(self, **item)
        self.master.save()
    
    def focus_in(self, event=None):
        event.widget.configure(state='normal')
        self.title = event.widget.get()
        if self.title == 'Title Here':
            self.title_var.set('')
        self.title_entry.focus()

    def focus_out(self, event=None):
        event.widget.configure(state='disabled')
        self.master.save()

    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        # return self.text