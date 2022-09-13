from tkinter import *

class ToolBar(Frame):
    '''
    Toolbar Frame for all windows
    '''
    def __init__(self, master=None, add_btn=False, add_btn_command=None, close_btn=True, **kw):
        super().__init__(master, **kw)
        self.show_close_btn = close_btn
        self.show_add_btn = add_btn
        self.add_btn_command = add_btn_command if add_btn_command else lambda e: e
        self.content()
    
    def content(self):
        '''
        Add components
        '''

        if self.show_add_btn:
            add_btn = Label(
                self, 
                text='+',
                bg='black',
                fg='white',
                font='Helvetica 20 normal'
            )

            add_btn.bind('<Enter>', self.hover)
            add_btn.bind('<Leave>', self.leave)
            add_btn.bind('<ButtonPress-1>', self.add_btn_command)
            add_btn.pack(side=LEFT, ipadx=5)

        if self.show_close_btn:
            close_btn = Label(
                self, 
                text='-',
                bg='black',
                fg='white',
                font='Helvetica 20 normal'
            )

            close_btn.bind('<Enter>', self.hover)
            close_btn.bind('<Leave>', self.leave)
            close_btn.bind('<ButtonPress-1>', self.close_app)
            close_btn.pack(side=RIGHT, ipadx=5)
    
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
    
    def close_app(self, event=None):
        '''
        Close the program
        '''
        if self.master.__str__() == '.':
            self.master.save()
        else:
            self.master.master.save()
        self.master.destroy()