from tkinter import (
    Toplevel, Label, Frame, Text, Canvas,
    Scrollbar, LEFT, TOP, BOTH, W, X, Y,
    RIGHT, BOTTOM, NW
)
from threading import Thread
from toolbar import ToolBar

FONT_LUCIDA_CONSOLE = 'Lucida Console'

class Chat(Toplevel):
    '''
    Chat Window
    '''

    def __init__(self, master=None, _id=None,  width=350,  **kw):
        super().__init__(master, **kw)
        self._id = _id
        self.width = width
        screen_width = master.winfo_screenwidth()
        width = (screen_width - (self.width*2))+90
        
        self.geometry(f"+{width}+0")
        self.minsize(width=self.width, height=500)
        self.maxsize(width=self.width, height=650)
        self['background'] = 'black'
        self.overrideredirect(1)
        self.attributes('-alpha', 0.8)

        self.content()
    
    def content(self):
        '''
        Widgets for settings window
        '''

        top_frame = ToolBar(
            self,
            bg='grey60',
            lock_btn=False,
            close_cmd=self.master.toggle_chat_window
        )
        
        chat_btn = Label(
            top_frame,
            image=self.master.icons['chat'],
            compound='left',
            name='settings',
            bg='grey60'
        )

        chat_btn.pack(side=LEFT, padx=5, pady=5)

        self.title = Label(
            top_frame,
            text='AI Prompt Window',
            font='Consolas 12 bold',
            fg='black',
            bg='grey60'
        )
        self.title.pack(side=LEFT, anchor=W, pady=5)
        
        clear_btn = Label(
            top_frame,
            image=self.master.icons['clear'],
            compound='left',
            name='clear',
            bg='grey60',
            cursor='hand2'
        )

        clear_btn.bind(self.master.MOUSE_ENTER_EVENT, self.master.hover)
        clear_btn.bind(self.master.MOUSE_LEAVE_EVENT, self.master.leave)
        clear_btn.bind(self.master.RIGHT_CLICK_EVENT, self.clear_chat)
        clear_btn.pack(side=RIGHT, pady=5)

        top_frame.pack(side=TOP, fill=X)
        
        main_container = Frame(
            self,
            bg='black'
        )
        
        left_scroll = Scrollbar(
            main_container,
            background='grey10',
        )
        
        left_scroll.pack(side=RIGHT, fill=Y)
        
        self.canvas = Canvas(
            main_container, 
            background='black',
            yscrollcommand=left_scroll.set
        )
        
        self.chat_container = Frame(
            self.canvas,
            bg="black",
            height=10
        )
        
        self.canvas.pack(side=LEFT, fill=BOTH)
        left_scroll.config(command=self.canvas.yview)
        self.chat_container.bind('<Configure>', self._configure_chat_frame)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta/60), 'units'))
        self.chat_frame_id = self.canvas.create_window(
            0, 
            0, 
            window=self.chat_container,
            anchor=NW
        )
        
        main_container.pack(side=TOP, fill=BOTH, expand=True)
        
        chat_frame = Frame(
            self,
            bg='white'
        )
        
        self.prompt_entry = Text(
            chat_frame, 
            background='black', 
            highlightthickness=0,
            fg='white', 
            font=(FONT_LUCIDA_CONSOLE, 10, 'normal'),
            height=2,
            width=36, 
            borderwidth=0,
            padx=5,
            pady=5
        )
        
        self.prompt_entry.bind("<Return>", self.get_prompt)
        self.prompt_entry.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)
        
        send_btn = Label(
            chat_frame,
            image=self.master.icons['paper-plane'],
            compound='left',
            name='send_chat',
            bg='white',
            cursor='hand2'
        )
        
        send_btn.bind(self.master.MOUSE_ENTER_EVENT, self.master.hover)
        send_btn.bind(self.master.MOUSE_LEAVE_EVENT, self.master.leave)
        send_btn.bind(self.master.RIGHT_CLICK_EVENT, self.get_prompt)
        send_btn.pack(side=RIGHT, padx=10, pady=5)
        
        chat_frame.pack(side=BOTTOM, fill=BOTH)
    
    def update_canvas(self):
        self.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def _configure_chat_frame(self, event):
        size = (self.chat_container.winfo_reqwidth(), self.chat_container.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        # if self.chat_container.winfo_reqwidth != self.canvas.winfo_width():
        #     self.canvas.config(width=self.chat_container.winfo_reqwidth())
    
    def _configure_canvas(self, event):
        if self.chat_container.winfo_reqwidth != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.chat_frame_id, width=self.canvas.winfo_width())
    
    def get_prompt(self, event=None, reply_type='stdout'):
        '''
        Get text from prompt entry
        '''
        if type(event) is str:
            prompt = event
        else:
            prompt = self.prompt_entry.get('1.0', 'end').strip()
        
        prompt_label = Label(
            self.chat_container,
            text=prompt,
            bg='grey10',
            fg='white',
            font=(FONT_LUCIDA_CONSOLE, 8, 'normal'),
            justify='left',
            wraplength=280,
            padx=5,
            pady=5
        )
        prompt_label.pack(side=TOP, anchor='se', pady=10, padx=10)
        self.prompt_entry.delete('1.0', 'end')
        # self.update_idletasks()
        self.update_canvas()
        
        chat_thread = Thread(target=self.query_chat, args=(prompt,reply_type,))
        chat_thread.daemon = True
        chat_thread.start()
        
    
    def query_chat(self, prompt: str, reply_type=None):
        result = self.master.ai_assistant.chat(prompt, reply_type)
        ai_label = Label(
            self.chat_container,
            text=result,
            bg='grey10',
            fg='white',
            font=(FONT_LUCIDA_CONSOLE, 8, 'normal'),
            justify='left',
            wraplength=280,
            padx=5,
            pady=5
        )
        ai_label.pack(side=TOP, anchor='sw', pady=10, padx=10)
        self.update_canvas()
    
    def clear_chat(self, event=None):
        """Clear memory buffery and chat history"""
        
        for item in self.chat_container.winfo_children():
            item.destroy()
        
        self.master.ai_assistant.memory.clear()
        self.update_canvas()
        
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.master.toggle_chat_window)
        self.wait_window(self)
        return True