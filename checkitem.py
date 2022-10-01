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

        self.close_btn = Label(
            self, 
            text='-',
            bg='black',
            fg='white',
            font='Helvetica 20 normal',
            name='delete'
        )

        self.close_btn.bind('<Enter>', self.hover)
        self.close_btn.bind('<Leave>', self.leave)
        self.close_btn.bind('<ButtonPress-1>', self.delete)
        
        
        sublist_icon = self.master.master.icons['check-double']
        self.sublist_btn = Label(
            self, 
            image=sublist_icon,
            compound='left',
            name='sublist',
            bg='white'
        )

        self.sublist_btn.bind('<Enter>', self.hover)
        self.sublist_btn.bind('<Leave>', self.leave)
        self.sublist_btn.bind('<ButtonPress-1>', self.sublist)
        
        # delete_icon = self.master.master.icons['trash']
        # delete_btn = Label(
        #     self, 
        #     image=delete_icon,
        #     compound='left',
        #     name='delete',
        #     bg='white'
        # )

        # delete_btn.bind('<Enter>', self.hover)
        # delete_btn.bind('<Leave>', self.leave)
        # delete_btn.bind('<ButtonPress-1>', self.delete)
        # delete_btn.pack(side=RIGHT, padx=5, ipadx=2, ipady=2)

        self.bind('<Enter>', self.show_btns)
        self.bind('<Leave>', self.hide_btns)
        self.pack(side=TOP, fill=BOTH, expand=True, pady=5, ipady=5)
    
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
            event.widget.configure(fg='red')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        event.widget.configure(fg='white')
    
    def focus_out(self, event=None):
        self.master.master.save()
        
    def show_btns(self, event=None):
        '''
        Show sublist and delete buttons
        '''
        self.close_btn.pack(side=RIGHT, ipadx=5)
        self.sublist_btn.pack(side=RIGHT, padx=2, ipadx=2)
    
    def hide_btns(self, event=None):
        '''
        Hide sublist and delete buttons
        '''
        self.close_btn.pack_forget()
        self.sublist_btn.pack_forget()
    
    def delete(self, event=None):
        '''
        Remove item from checklist
        '''
        self.destroy()
        self.master.master.save()
        self.master.master.reload()
    
    def sublist(self, event=None):
        '''
        Create sublist
        '''
        title = self.label_var.get()
        