from tkinter import Toplevel, Label, Entry,  \
    Frame, LabelFrame, StringVar, IntVar, \
    LEFT, RIGHT, TOP, X
from tkinter.ttk import Combobox

from toolbar import ToolBar

from threading import Thread
from datetime import datetime
from time import sleep

class Reminder(Toplevel):
    '''
    New Reminder Window
    '''
    MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')

    COMBO_SELECTED_EVENT = "<<ComboboxSelected>>"
    def __init__(self, master=None, _id=None, pos_x=0, pos_y=0, title='Title Here', date_time=datetime.utcnow(), width=250, height=120, bg='#161a1d', fg='#fdfffc', locked=False, is_withdrawn=False, **kw):
        super().__init__(master, **kw)
        self._id = _id
        self.date_time = date_time
        self.year = date_time.year
        self.month = date_time.month
        self.day = date_time.day
        self.time = date_time.time().isoformat(timespec='seconds')
        self.title = title
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.locked = locked
        self.is_withdrawn = is_withdrawn
        self.expired = False
        
        self.geometry(f"{width}x{height}+%d+%d" % (pos_x, pos_y))

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
            '_id': self._id,
            'type': 'reminder',
            'pos_x': self.winfo_x(),
            'pos_y': self.winfo_y(),
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'title': self.title_var.get(),
            'bg': self.bg,
            'fg': self.fg,
            'date_time': self.date_time,
            'locked': self.locked,
            'is_withdrawn': self.is_withdrawn
        }
    
    def content(self):
        '''
        Reminder components
        '''
        tools_frame = ToolBar(
            self,
            bg='crimson',
        )
        
        info_frame = Frame(
            self,
            bg='crimson',
        )

        self.title_var = StringVar(value=self.title)
        self.title_entry = Entry(
            tools_frame,
            textvariable=self.title_var,
            font='Consolas 10 bold',
            bg='black',
            fg='white',
            state='disabled',
            disabledforeground='gold',
            disabledbackground='crimson',
            border=0
        )
        
        self.title_entry.bind('<Double-1>', self.focus_in)
        self.title_entry.bind('<FocusOut>', self.focus_out)
        self.title_entry.bind('<Return>', self.focus_out)
        self.title_entry.pack(side=LEFT, fill=X, expand=True, padx=5, ipady=5)
        
        tools_frame.pack(side=TOP, ipady=5, fill=X)
        
        self.date_label = Label(
            info_frame,
            text=self.date_time.strftime("%a %b %d %Y"),
            font='Consolas 12 bold',
            bg='black',
            fg='white',
            justify='left',
        )
        
        self.days_left_label = Label(
            info_frame,
            text=self.get_days_left(),
            font='Consolas 12 bold',
            bg='black',
            fg='lime',
            justify='right',
        )
        
        self.date_label.pack(side=LEFT, fill=X, expand=True, ipadx=5)
        self.days_left_label.pack(side=RIGHT, fill=X, expand=True, ipadx=5)
        info_frame.pack(side=TOP, fill=X, expand=True, pady=5)
        
        date_frame = LabelFrame(
            self,
            text='Set Date',
            bg=self.bg,
            fg=self.fg
        )
        
        
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
        
        
        yearbox.bind(Reminder.COMBO_SELECTED_EVENT, lambda e: self.set_datetime())
        monthbox.bind(Reminder.COMBO_SELECTED_EVENT, lambda e: self.set_datetime())
        daybox.bind(Reminder.COMBO_SELECTED_EVENT, lambda e: self.set_datetime())
        
        yearbox.pack(side=LEFT, pady=2, padx=2)
        monthbox.pack(side=LEFT, pady=2, padx=2)
        daybox.pack(side=LEFT, pady=2, padx=2)
        
        date_frame.pack(side=TOP, ipadx=3, fill=X)
        
        check_thread = Thread(target=self.check_days_left)
        check_thread.daemon = True

        expired_thread = Thread(target=self.blink)
        expired_thread.daemon = True

        self.bind('<<OnExpired>>', lambda e: expired_thread.start())
        self.after(100, lambda: check_thread.start())

    def blink(self):
        '''
        Blink days left on expire
        '''
        on = True
        try:
            while True:
                if self.expired:
                    self.days_left_label.configure(fg='red' if on else 'black')
                    self.update_idletasks()
                    on = False if on else True
                sleep(0.5)
        except Exception:
            pass
    
    def get_days_left(self)->str:
        '''
        Calculate days difference
        '''
        
        return f"{(self.date_time - datetime.utcnow()).days} days"

    def check_days_left(self):
        '''
        Toggle days left color
        '''
        try:
            while True:
                self.days_left_label.configure(text=self.get_days_left())

                difference = self.date_time - datetime.utcnow()
                remaining_days = difference.days
                # print(difference.__str__())
                if remaining_days < 1:
                    self.days_left_label.configure(fg='red')
                    if not self.expired:
                        self.expired = True
                        self.event_generate('<<OnExpired>>', when='tail')
                else:
                    self.expired = False
                    self.days_left_label.configure(fg='lime')
                self.update_idletasks()
                
                sleep(60)
        except Exception:
            pass
            
    
    def set_datetime(self):
        '''
        Set date_time from combobox
        '''
        self.date_time = datetime(self.year_var.get(), Reminder.MONTHS.index(self.mon_var.get())+1, self.day_var.get())
        self.date_label.configure(text=self.date_time.strftime("%a %b %d %Y"))
        self.days_left_label.configure(text=self.get_days_left())

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
