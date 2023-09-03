from tkinter import (
    Toplevel, Label, LabelFrame,
    Entry, StringVar,
    LEFT, TOP, W, X, BOTH
)
from tkinter.colorchooser import askcolor

from toolbar import ToolBar

class Settings(Toplevel):
    '''
    Settings Window
    '''

    def __init__(
        self,
        master=None,
        _id=None,
        width=250,
        openai_api_key='',
        cohere_api_key='',
        serpapi_api_key='',
        **kw):
        super().__init__(master, **kw)
        self._id = _id
        self.openai_api_key = StringVar(value=openai_api_key),
        self.cohere_api_key = StringVar(value=cohere_api_key),
        self.serpapi_api_key = StringVar(value=serpapi_api_key),
        self.width = width
        screen_width = master.winfo_screenwidth()
        width = (screen_width - (self.width*2))-10
        
        self.geometry(f"+{width}+0")
        self.minsize(width=self.width, height=200)
        self['background'] = 'black'
        self.overrideredirect(1)
        self.attributes('-alpha', 0.8)

        self.content()
    
    def to_object(self)->dict:
        '''
        Convert to object for saving
        '''
        
        return {
            '_id': self._id,
            'type': 'settings',
            "openai_api_key": self.openai_api_key[0].get(),
            "cohere_api_key": self.cohere_api_key[0].get(),
            "serpapi_api_key": self.serpapi_api_key[0].get()
        }
        
    def content(self):
        '''
        Widgets for settings window
        '''

        top_frame = ToolBar(
            self,
            bg='grey60',
            lock_btn=False,
            close_cmd=self.master.toggle_settings
        )
        
        settings_btn = Label(
            top_frame,
            image=self.master.icons['settings'],
            compound='left',
            name='settings',
            bg='grey60'
        )

        settings_btn.pack(side=LEFT, padx=5, pady=5)

        self.title = Label(
            top_frame,
            text='Settings',
            font='Consolas 12 bold',
            fg='black',
            bg='grey60'
        )
        self.title.pack(side=LEFT, anchor=W, pady=5)

        top_frame.pack(side=TOP, fill=X)
        
        ai_settings_frame = LabelFrame(
            self,
            text='AI Settings',
            fg='white',
            bg='black'
        )
        
        openai_api_label = Label(
            ai_settings_frame,
            text="OPENAI API KEY",
            fg="white",
            bg='black',
            justify=LEFT
        )

        openai_api_entry = Entry(
            ai_settings_frame,
            textvariable=self.openai_api_key,
            fg="white",
            bg="black",
            show="*"
        )
        
        cohere_api_label = Label(
            ai_settings_frame,
            text="COHERE API KEY",
            fg="white",
            bg='black',
            justify=LEFT
        )
        
        cohere_api_entry = Entry(
            ai_settings_frame,
            textvariable=self.cohere_api_key,
            fg="white",
            bg="black",
            show="*"
        )
        
        serpapi_api_label = Label(
            ai_settings_frame,
            text="SERP API KEY",
            fg="white",
            bg='black',
            justify=LEFT
        )
        
        serpapi_api_entry = Entry(
            ai_settings_frame,
            textvariable=self.serpapi_api_key,
            fg="white",
            bg="black",
            show="*"
        )
        
        openai_api_label.pack(side=TOP, padx=5)
        openai_api_entry.pack(side=TOP, fill=X, padx=5, pady=5, ipadx=5, ipady=5)
        cohere_api_label.pack(side=TOP, padx=5,)
        cohere_api_entry.pack(side=TOP, fill=X, padx=5, pady=5, ipadx=5, ipady=5)
        serpapi_api_label.pack(side=TOP, padx=5)
        serpapi_api_entry.pack(side=TOP, fill=X, padx=5, pady=5, ipadx=5, ipady=5)
        
        ai_settings_frame.pack(side=TOP, fill=X, padx=5, pady=5, ipadx=5, ipady=5)
        

    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.master.toggle_settings)
        self.wait_window(self)
        return True