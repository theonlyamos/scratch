from tkinter import *
from tkinter import ttk

class CheckItem(Frame):
    '''
    Item in check list
    '''
    def __init__(self, master=None, label='', checked=False, has_sublists=False, bg = 'black', **kw):
        super().__init__(master, bg=bg, **kw)
        self.label = label
        self.checked = checked
        self.has_sublists = has_sublists
        self.bg = bg

        self.content()
    
    def to_object(self)->dict:
        '''
        Convert to object for saving
        '''
        return {
            'label': self.label_var.get(),
            'checked': self.check_var.get(),
            'has_sublists': self.has_sublists,
            'bg': self.bg
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
            # self.pack_forget()
            self.pack_configure(side=TOP, fill=BOTH, expand=True, pady=5, ipady=5)
        else:
            self.entry.configure(state='disabled')
            self.entry.configure(fg='#161a1d')

            # if not self.master.show_checked_var.get():
            #     self.pack_forget()
            # else:
            self.pack_configure(side=BOTTOM, fill=X, expand=True, pady=5)
        
        self.master.master.save()
    
    def hover(self, event=None):
        '''
        Change foreground color on mouse enter
        '''
        if '.sublist' in event.widget.__str__():
            event.widget.configure(bg='#66FFFF')
        elif '.delete' in event.widget.__str__():
            event.widget.configure(fg='red')
        elif event.widget.cget('text') == '+':
            event.widget.configure(bg='turquoise')
        else:
            event.widget.configure(fg='red')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        if '.sublist' in event.widget.__str__():
            event.widget.configure(bg='white')
        elif '.delete' in event.widget.__str__():
            event.widget.configure(fg='white')
        else:
            event.widget.configure(fg='white')
    
    def focus_out(self, event=None):
        self.master.master.save()
        
    def show_btns(self, event=None):
        '''
        Show sublist and delete buttons
        '''
        self.pack_configure(ipady=0)
        self.close_btn.pack(side=RIGHT, ipadx=5)
        self.sublist_btn.pack(side=RIGHT, padx=2, ipadx=2)
    
    def hide_btns(self, event=None):
        '''
        Hide sublist and delete buttons
        '''
        self.pack_configure(ipady=5)
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
        item_id = self.__str__()
   
        new_list = self.master.create_sublist(self.master.master, title=title, item_id=item_id, bg=self.bg)
        self.has_sublists = True
        
        self.master.master.save()
        