from tkinter import Toplevel, Label, Entry,  \
    StringVar, LEFT, RIGHT, TOP, BOTTOM, X
from toolbar import ToolBar
from checkitem import CheckItem

class CheckList(Toplevel):
    '''
    
    New CheckList Window
    '''
    OBJECT_NAME = '!checkitem'

    def __init__(self, master=None,_id=None, pos_x=0, pos_y=0, title='Title Here', width=250, items: list[dict]=None, text='', bg='#161a1d', fg='#fdfffc', toolbar_bg='#66FFFF', is_sublist=False, parent_item=None, show_checked=True, locked=False, is_withdrawn=False, **kw):
        super().__init__(master, **kw)
        self._id = _id
        self.items = [] if items is None else items
        self.title = title
        self.is_sublist = is_sublist
        self.parent_item = parent_item
        self.show_checked = show_checked
        self.locked = locked
        self.toolbar_bg = toolbar_bg
        self.is_withdrawn = is_withdrawn
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.geometry(f"+{pos_x}+{pos_y}")
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
            if CheckList.OBJECT_NAME in key:
                items.append(self.children[key].to_object())
                
        return {
            '_id': self._id,
            'type': 'checklist',
            'pos_x': self.winfo_x(),
            'pos_y': self.winfo_y(),
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'title': self.title_var.get(),
            'bg': self.bg,
            'fg': self.fg,
            'toolbar_bg': self.toolbar_bg,
            'text': self.text,
            'items': items,
            'is_sublist': self.is_sublist,
            'parent_item': self.parent_item,
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

        if not self.is_sublist:
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
                if CheckList.OBJECT_NAME in item.__str__() and item.check_var.get():
                    item.pack(side=BOTTOM, fill=X, pady=5)
        else:
            self.show_checked = True
            for item in self.children.values():
                if CheckList.OBJECT_NAME in item.__str__() and item.check_var.get():
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
    def create_sublist(cls, master, title, parent_item, toolbar_bg):
        '''
        Create new list under a checkitem
        
        @param title str Label of checkitem
        @return Type[Classlist]
        '''
        return cls(master, title=title, toolbar_bg=toolbar_bg, is_sublist=True, parent_item=parent_item, pos_x = master.get_pos_x(), pos_y=master.get_pos_y())

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
