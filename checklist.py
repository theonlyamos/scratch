from tkinter import *

from toolbar import ToolBar
from checkitem import CheckItem

class CheckList(Toplevel):
    '''
    New CheckList Window
    '''

    def __init__(self, master=None, posX=0, posY=0, title='Title Here', width=250, items:list[dict]=[], text='', bg='#161a1d', fg='#fdfffc', toolbar_bg='#66FFFF', is_sublist=False, item_id=None, show_checked=True, locked=False, is_withdrawn=False, **kw):
        super().__init__(master, **kw)
        self.items = items
        self.title = title
        self.is_sublist = is_sublist
        self.item_id = item_id
        self.show_checked = show_checked
        self.locked = locked
        self.toolbar_bg = toolbar_bg
        self.is_withdrawn = is_withdrawn
        
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
            'posX': self.winfo_x(),
            'posY': self.winfo_y(),
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'title': self.title_var.get(),
            'bg': self.bg,
            'fg': self.fg,
            'toolbar_bg': self.toolbar_bg,
            'text': self.text,
            'items': items,
            'is_sublist': self.is_sublist,
            'item_id': self.item_id,
            'show_checked': self.show_checked,
            'locked': self.locked,
            'is_withdrawn': self.is_withdrawn
        }
    
    def content(self):
        '''
        CheckList components
        '''
        tools_frame = ToolBar(
            self,
            bg=self.toolbar_bg, # if not self.is_sublist else self.bg,
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
            disabledforeground='black',
            disabledbackground=self.toolbar_bg,
            border=0
        )
        
        self.title_entry.bind('<Double-1>', self.focus_in)
        self.title_entry.bind('<FocusOut>', self.focus_out)
        self.title_entry.bind('<Return>', self.focus_out)
        self.title_entry.pack(side=LEFT, fill=X, expand=True, ipady=5)
        
        check_btn = Label(
            tools_frame, 
            image=self.master.icons['square-check'] if self.show_checked else self.master.icons['square'],
            compound='left',
            name='check',
            bg=self.toolbar_bg
        )

        check_btn.bind('<Enter>', self.hover)
        check_btn.bind('<Leave>', self.leave)
        check_btn.bind('<ButtonPress-1>', self.toggle_checked)
        check_btn.pack(side=RIGHT, padx=2)
        
        tools_frame.pack(side=TOP, ipady=5, fill=X)

        for item in self.items:
            if not item['checked']:
                CheckItem(self, **item)
                
        for item in self.items:
            if item['checked']:
                CheckItem(self, **item)
        
        self.toggle_checked()

    
    def toggle_checked(self, event=None):
        '''
        Toggle checked items
        '''
        if self.show_checked:
            self.show_checked = False
            for item in self.children.values():
                if '!checkitem' in item.__str__():
                    if item.check_var.get():
                        item.pack(side=BOTTOM, fill=X, pady=5)
        else:
            self.show_checked = True
            for item in self.children.values():
                if '!checkitem' in item.__str__():
                    if item.check_var.get():
                        item.pack_forget()              
    
     
    def add_item(self, event=None):
        '''
        Add new checklist item
        '''
        item = {'label': '', 'checked': False}
        self.items.append(item)
        CheckItem(self, **item)
        
        self.master.save()
        self.master.reload()
    
    def focus_in(self, event=None):
        event.widget.configure(state='normal')
        self.title = event.widget.get()
        if self.title == 'Title Here':
            self.title_var.set('')
        self.title_entry.focus()

    def focus_out(self, event=None):
        event.widget.configure(state='disabled')
        self.master.save()
    
    @classmethod
    def create_sublist(cls, master, title, item_id, toolbar_bg):
        '''
        Create new list under a checkitem
        
        @param title str Label of checkitem
        @return Type[Classlist]
        '''
        return cls(master, title=title, toolbar_bg=toolbar_bg, is_sublist=True, item_id=item_id, posX = master.get_posX(), posY=master.get_posY())

    def hover(self, event=None):
        '''
        Change foreground color on mouse enter
        '''
        if '.!toolbar.check' in event.widget.__str__():
            if self.show_checked:
                event.widget.configure(image=self.master.icons['square-check'])
            else:
                event.widget.configure(image=self.master.icons['square'])

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        if '.!toolbar.check' in event.widget.__str__():
            if self.show_checked:
                event.widget.configure(image=self.master.icons['square'])
            else:
                event.widget.configure(image=self.master.icons['square-check'])
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        # return self.text