from tkinter import *
from tkinter.ttk import Combobox

from toolbar import ToolBar

from datetime import datetime

class Reminder(Toplevel):
    '''
    New Reminder Window
    '''
    MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')

    def __init__(self, master=None, posX=0, posY=0, title='Title Here', date_time=datetime.utcnow(), width=250, height=100, bg='#161a1d', fg='#fdfffc', **kw):
        super().__init__(master, **kw)
        self.date_time = date_time
        self.year = date_time.year
        self.month = date_time.month
        self.day = date_time.day
        self.time = date_time.time().isoformat(timespec='seconds')
        self.title = title
        self.posX = posX
        self.posY = posY
        
        self.geometry(f"{width}x{height}+%d+%d" % (posX, posY))

        #self.minsize(width=width, height=40)
        
        self.bg = bg
        self.fg = fg
        self['background'] = bg
        self.overrideredirect(1)
        self.attributes('-alpha', 0.7)
        self.content()
    
    def to_object(self)->dict:
        '''
        Convert to object for saving
        '''
         
        return {
            'type': 'reminder',
            'posX': self.posX,
            'posY': self.posY,
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'title': self.title_var.get(),
            'bg': self.bg,
            'fg': self.fg,
            'date_time': self.date_time
        }
    
    def content(self):
        '''
        Reminder components
        '''
        tools_frame = ToolBar(
            self,
            bg='black',
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
        
        # close_btn = Label(
        #     tools_frame, 
        #     text='-',
        #     bg='black',
        #     fg='white',
        #     font='Helvetica 20 normal'
        # )


        # close_btn.bind('<ButtonPress-1>', lambda e: self.destroy())
        # close_btn.pack(side=LEFT, padx=5, ipadx=5)
        
        self.title_entry.bind('<Double-1>', self.focus_in)
        self.title_entry.bind('<FocusOut>', self.focus_out)
        self.title_entry.bind('<Return>', self.focus_out)
        self.title_entry.pack(side=LEFT, fill=X, padx=5, ipady=5)
        
        tools_frame.pack(side=TOP, fill=X)
        
        date_frame = LabelFrame(
            self,
            text='Date',
            bg=self.bg,
            fg=self.fg
        )
        
        time_frame = LabelFrame(
            self,
            text='Date',
            bg=self.bg,
            fg=self.fg
        )
        
        # self.months_var = StringVar()
        # self.months_var.set('All')
        
        
        self.year_var = IntVar(value=self.date_time.year)
        yearbox = Combobox (
            date_frame,
            textvariable=self.year_var,
            values=tuple(range(datetime.utcnow().year, datetime.utcnow().year+30)),
            state='readonly',
            justify='left',
            width=10
        )
        
        self.mon_var = StringVar(value=Reminder.MONTHS[self.date_time.month-1])
        monthbox = Combobox (
            date_frame,
            textvariable=self.mon_var,
            values=Reminder.MONTHS,
            state='readonly',
            justify='left',
            width=11
        )
        
        self.day_var = IntVar(value=self.date_time.day)
        daybox = Combobox (
            date_frame,
            textvariable=self.day_var,
            values=tuple(range(1, 32)),
            state='readonly',
            justify='left',
            width=9
        )
        
        
        yearbox.bind("<<ComboboxSelected>>", lambda e: self.set_datetime(e))
        monthbox.bind("<<ComboboxSelected>>", lambda e: self.set_datetime(e))
        daybox.bind("<<ComboboxSelected>>", lambda e: self.set_datetime(e))
        
        yearbox.pack(side=LEFT, pady=2, padx=2)
        monthbox.pack(side=LEFT, pady=2, padx=2)
        daybox.pack(side=LEFT, pady=2, padx=2)
        
        date_frame.pack(side=TOP, pady=5, ipady=3, ipadx=3, fill=X)
    
    def set_datetime(self, event=None):
        '''
        Set date_time from combobox
        '''
        self.date_time = datetime(self.year_var.get(), Reminder.MONTHS.index(self.mon_var.get())+1, self.day_var.get())

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