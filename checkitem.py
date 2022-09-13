from tkinter import *
from tkinter import ttk

class CheckItem(Frame):
    '''
    Item in check list
    '''
    def __init__(self,master=None, label='', checked=False, **kw):
        super().__init__(master, bg='black', **kw)
        self.label = label
        self.checked = checked

        self.content()
    
    def to_object(self)->dict:
        '''
        Convert to object for saving
        '''
        return {
            'label': self.label_var.get(),
            'checked': self.check_var.get(),
        }
    
    def content(self):
        '''
        Item components
        '''

        self.check_var = BooleanVar(value=self.checked)
        Checkbutton(
            self,
            variable=self.check_var,
            onvalue=1,
            offvalue=0,
            command=self.check,
            bg='black'
        ).pack(side=LEFT)

        self.label_var = StringVar(value=self.label)

        self.entry = Entry(
            self,
            textvariable=self.label_var,
            bg='black',
            fg='white',
            border=0,
            font=('Times New Roman', 10, 'normal'),
            justify='left',
            state= 'disabled' if self.checked else 'normal'
        )

        self.entry.bind('<FocusOut>', self.focus_out)
        self.entry.bind('<Return>', self.focus_out)
        self.entry.focus()
        self.entry.pack(side=LEFT, fill=BOTH, expand=True, ipady=5)

        close_btn = Label(
            self, 
            text='-',
            bg='black',
            fg='white',
            font='Helvetica 20 normal'
        )

        close_btn.bind('<Enter>', self.hover)
        close_btn.bind('<Leave>', self.leave)
        close_btn.bind('<ButtonPress-1>', self.delete)
        close_btn.pack(side=RIGHT, ipadx=5)

        self.pack(side=TOP, fill=BOTH, expand=True, pady=5)
    
    def check(self):
        '''
        Invoked on checkbutton checked
        '''
        if not self.check_var.get():
            self.entry.configure(state='normal')
            self.entry.configure(fg='white')
            self.pack_forget()
            self.pack(side=TOP, fill=X, pady=5)
        else:
            self.entry.configure(state='disabled')
            self.entry.configure(fg='#161a1d')
            self.pack_forget()
            if self.master.show_checked_var.get():
                self.pack(side=BOTTOM, fill=X, pady=5)
        
        self.master.master.save()
    
    def hover(self, event=None):
        '''
        Change foreground color on mouse enter
        '''
        if event.widget.cget('text') == '+':
            event.widget.configure(bg='turquoise')
        else:
            event.widget.configure(bg='brown')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        event.widget.configure(bg='black')
    
    def focus_out(self, event=None):
        self.master.master.save()
    
    def delete(self, event=None):
        '''
        Remove item from checklist
        '''
        self.master.master.save()
        self.destroy()