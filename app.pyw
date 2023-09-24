__author__ = 'ph4n70m'
__version__ = '0.0.4'

from tkinter import Tk, Label,   \
    LEFT, RIGHT, TOP, X
from tkinter import ttk
from PIL import ImageTk
from threading import Thread

from utils import get_audio
from toolbar import ToolBar
from note import Note
from checklist import CheckList
from addmenu import AddMenu
from reminder import Reminder
from settings import Settings
from ai import AIAssistant
from chat import Chat

from runit_database import Document
from datetime import datetime
from time import sleep
import shelve
    
from icons import icons

# Document.initialize(
#     'http://runit.test:9000/api',
#     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjkzMDQxNCwianRpIjoiOWU5YmIwMDAtOWJkNS00ZWI4LTg4YWEtYWViMjYzNDU3NGI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyYjAxY2E4ZGVmN2YzMTcwMDNiZWUyYiIsIm5iZiI6MTY4NjkzMDQxNCwiZXhwIjoxNjg5NTIyNDE0fQ.OJq8c4DgBI1haEgbS9NHMDxYAQtaFIzTHSopaiZNeSc',
#     '648c7f6886abacf21d21faf2'
# )

class Scratch(Tk):
    '''
    Main self window
    '''
    WIDTH = 250
    HEIGHT = 250
    CHAT_ON = False
    SHOW_NOTES = True
    MENU_OPEN = False
    SHOW_REMINDERS = True
    SETTINGS_OPEN = False
    SHOW_CHECKLISTS = True
    SPEECH_RECOGNITION = True
    
    MOUSE_ENTER_EVENT = '<Enter>'
    MOUSE_LEAVE_EVENT = '<Leave>'
    RIGHT_CLICK_EVENT = '<ButtonPress-1>'

    def __init__(self, **kw):
        super().__init__(**kw)
 
        screen_width = self.winfo_screenwidth()
        self.pos_x = screen_width - Scratch.WIDTH
        self.geometry(f"+{self.pos_x}+0")
        self.overrideredirect(1)
        self.minsize(width=Scratch.WIDTH, height=40)
        self.attributes('-alpha', 0.7)
        self.icons = {}

        self['background'] = '#161a1d'

        self.build_icons()
        self.content()
        #self.after(30, self.start_auto_backup_thread)

    def build_icons(self):
        for key, value in icons.items():
            self.icons[key] = ImageTk.PhotoImage(value)

    def start_auto_backup_thread(self):
        b_thread = Thread(target=self.auto_backup, args=())
        b_thread.daemon = True
        b_thread.start()
    
    def start_backup_thread(self):
        b_thread = Thread(target=self.backup, args=())
        b_thread.daemon = True
        b_thread.start()
    
    def content(self):
        '''
        Main self Components
        '''
        # Load Items from DB
        items = self.load()
        
        self.top_frame = ToolBar(
            self,
            bg='white',
            add_btn=True,
            add_btn_command=self.toggle_add_menu,
            lock_btn=False
        )
        
        settings_btn = Label(
            self.top_frame,
            image=self.icons['settings'],
            compound='left',
            name='settings',
            bg='white',
            cursor='hand2'
        )

        settings_btn.pack(side=RIGHT)
        settings_btn.bind(Scratch.MOUSE_ENTER_EVENT, self.hover)
        settings_btn.bind(Scratch.MOUSE_LEAVE_EVENT, self.leave)
        settings_btn.bind(Scratch.RIGHT_CLICK_EVENT, self.toggle_settings)
        
        calendar_btn = Label(
            self.top_frame,
            image=self.icons['calendar-solid' if Scratch.SHOW_REMINDERS else 'calendar'],
            text='',
            compound='left',
            name='calendar',
            cursor='hand2'
        )

        calendar_btn.pack(side=RIGHT, padx=5)
        calendar_btn.bind(Scratch.MOUSE_ENTER_EVENT, self.hover)
        calendar_btn.bind(Scratch.MOUSE_LEAVE_EVENT, self.leave)
        calendar_btn.bind(Scratch.RIGHT_CLICK_EVENT, lambda e: self.toggle_module(e, 'reminder'))
        
        note_btn = Label(
            self.top_frame,
            image=self.icons['document-solid' if Scratch.SHOW_NOTES else 'document'],
            text='',
            compound='left',
            name='note',
            cursor='hand2'
        )

        note_btn.bind(Scratch.MOUSE_ENTER_EVENT, self.hover)
        note_btn.bind(Scratch.MOUSE_LEAVE_EVENT, self.leave)
        note_btn.bind(Scratch.RIGHT_CLICK_EVENT, lambda e: self.toggle_module(e, 'note'))
        note_btn.pack(side=RIGHT)
        
        check_btn = Label(
            self.top_frame,
            image=self.icons['checkbox-solid'if Scratch.SHOW_CHECKLISTS else 'checkbox'],
            text='',
            compound='left',
            name='check',
            cursor='hand2'
        )

        check_btn.pack(side=RIGHT, padx=5)
        check_btn.bind(Scratch.MOUSE_ENTER_EVENT, self.hover)
        check_btn.bind(Scratch.MOUSE_LEAVE_EVENT, self.leave)
        check_btn.bind(Scratch.RIGHT_CLICK_EVENT, lambda e: self.toggle_module(e, 'checklist'))
        
        speech_btn = Label(
            self.top_frame,
            image=self.icons['mic-solid' if Scratch.SPEECH_RECOGNITION else 'mic'],
            compound='left',
            name='speech',
            bg='white',
            cursor='hand2'
        )

        speech_btn.pack(side=LEFT)
        speech_btn.bind(Scratch.MOUSE_ENTER_EVENT, self.hover)
        speech_btn.bind(Scratch.MOUSE_LEAVE_EVENT, self.leave)
        speech_btn.bind(Scratch.RIGHT_CLICK_EVENT, self.toggle_speech_recognition)

        chat_btn = Label(
            self.top_frame,
            image=self.icons['android-solid' if Scratch.CHAT_ON else 'android'],
            compound='left',
            name='chat',
            bg='white',
            cursor='hand2'
        )

        chat_btn.pack(side=LEFT)
        chat_btn.bind(Scratch.MOUSE_ENTER_EVENT, self.hover)
        chat_btn.bind(Scratch.MOUSE_LEAVE_EVENT, self.leave)
        chat_btn.bind(Scratch.RIGHT_CLICK_EVENT, self.toggle_chat_window)
        
        self.top_frame.pack(side=TOP, ipady=8, fill=X)
        
        self.add_menu_window = None
        self.settings_window = None
        
        ai_settings = {}
        
        for item in items:
            item_type = item['type']
            del item['type']

            if item_type == 'checklist':
                CheckList(self, **item)
            elif item_type == 'note':
                Note(self, **item)
            elif item_type == 'reminder':
                Reminder(self, **item)
            elif item_type == 'settings':
                ai_settings = item
            else:
                print('Not a valid type')
    
        self.settings_window = Settings(
            self,
            **ai_settings
        )
        
        self.settings_window.withdraw()
        
        self.chat_window = Chat(
            self
        )
        self.chat_window.withdraw()
        
        self.ai_assistant = AIAssistant()
        
        speech_thread = Thread(target=self.start_speech_recognition)
        speech_thread.daemon = True

        self.bind('<FocusOut>', self.save)
        self.after(100, lambda: speech_thread.start())
        self.toggle_modules_on_start()
    
    def get_pos_y(self)->int:
        '''
        Calculate next item veritcal positioning
        '''
        last_item = self.children[list(self.children.keys())[-1]]
        screen_y = last_item.winfo_height() + last_item.winfo_y()

        if (self.winfo_screenheight() - screen_y) > 200:
            return screen_y + 10
        return 48
        
    def get_pos_x(self)->int:
        '''
        Calculate next item veritcal positioning
        '''
        last_item = self.children[list(self.children.keys())[-1]]

        screen_y = last_item.winfo_height() + last_item.winfo_y()
        if last_item.winfo_x() == 0:
            return self.pos_x
        if (self.winfo_screenheight() - screen_y) > 200 and last_item.winfo_x() >= self.pos_x:
            return self.pos_x
        
        if (self.winfo_screenheight() - screen_y) > 200:
            return last_item.winfo_x()

        return (last_item.winfo_x() - self.WIDTH)-10
        
    def new_item(self, item='note'):
        '''
        Open Toplevel window for creating \n
        new item
        '''
        pos_y = self.get_pos_y()
        pos_x = self.get_pos_x()
        
        if item == 'note':
            new_note_window = Note(
                self,
                width=Scratch.WIDTH,
                pos_x=pos_x,
                pos_y=pos_y
            )
            self.save()
            new_note_window.show()
        
        elif item == 'checklist':
            checklist_window = CheckList(
                self,
                width=Scratch.WIDTH,
                pos_x=pos_x,
                pos_y=pos_y
            )
            self.save()
            checklist_window.show()
            
        elif item == 'reminder':
            reminder_window = Reminder(
                self,
                width=Scratch.WIDTH,
                pos_x=pos_x,
                pos_y=pos_y
            )
            self.save()
            reminder_window.show()
    
    def toggle_add_menu(self, event=None):
        '''
        Show/Hide Add Menu Frame
        '''

        if Scratch.MENU_OPEN:
            Scratch.MENU_OPEN = False
            self.add_menu_window.destroy()
        else:
            Scratch.MENU_OPEN = True
            self.add_menu_window = AddMenu(
                self
            )
            item = self.add_menu_window.show()
            self.new_item(item=item.strip())

    def toggle_chat_window(self, event=None):
        '''
        Show/Hide Add Menu Frame
        '''

        if Scratch.CHAT_ON:
            Scratch.CHAT_ON = False
            self.chat_window.withdraw()
            # self.chat_window.destroy()
        else:
            Scratch.CHAT_ON = True
            self.chat_window.show()
            
    def toggle_settings(self, event=None):
        '''
        Show/Hide Add Menu Frame
        '''

        if Scratch.SETTINGS_OPEN:
            Scratch.SETTINGS_OPEN = False
            self.settings_window.withdraw()
        else:
            Scratch.SETTINGS_OPEN = True
            self.settings_window.show()

    def toggle_speech_recognition(self, event=None):
        '''
        Toggle Speech Regcognition functionality
        '''
        if Scratch.SPEECH_RECOGNITION:
            Scratch.SPEECH_RECOGNITION = False
        else:
            Scratch.SPEECH_RECOGNITION = True
    
    def start_speech_recognition(self):
        '''
        Start speech recognition
        '''
        
        while True:
            try:
                text = get_audio()
                if text.lower().startswith('computer'):
                    text = ' '.join(text.split(" ")[1::])
                    self.ai_assistant.chat(text, 'audio')
            except Exception as e:
                print(str(e))
                continue

    def hover(self, event=None):
        '''
        Change icon to solid
        '''
        
        if event.widget.__str__() == '.!toolbar.settings':
            event.widget.configure(image=self.icons['settings-solid'])
        
        elif event.widget.__str__() == '.!chat.!toolbar.clear':
            event.widget.configure(image=self.icons['clear-solid'])
        
        elif event.widget.__str__() == '.!toolbar.check':
            if not Scratch.SHOW_CHECKLISTS:
                event.widget.configure(image=self.icons['checkbox-solid'])
            else:
                event.widget.configure(image=self.icons['checkbox'])
        
        elif event.widget.__str__() == '.!toolbar.note':
            if not Scratch.SHOW_NOTES:
                event.widget.configure(image=self.icons['document-solid'])
            else:
                event.widget.configure(image=self.icons['document'])
        
        elif event.widget.__str__() == '.!toolbar.calendar':
            if not Scratch.SHOW_REMINDERS:
                event.widget.configure(image=self.icons['calendar-solid'])
            else:
                event.widget.configure(image=self.icons['calendar'])
        
        elif event.widget.__str__() == '.!toolbar.speech':
            if not Scratch.SPEECH_RECOGNITION:
                event.widget.configure(image=self.icons['mic-solid'])
            else:
                event.widget.configure(image=self.icons['mic'])
        
        elif event.widget.__str__() == '.!toolbar.chat':
            if not Scratch.CHAT_ON:
                event.widget.configure(image=self.icons['android-solid'])
            else:
                event.widget.configure(image=self.icons['android'])
        
        elif event.widget.__str__() == '.!chat.!frame2.send_chat':
            event.widget.configure(image=self.icons['paper-plane-solid'])
        
        else:
            event.widget.configure(bg='red')

    def leave(self, event=None):
        '''
        Revert to default icon
        '''
        
        if event.widget.__str__() == '.!toolbar.settings':
            event.widget.configure(image=self.icons['settings'])
        
        elif event.widget.__str__() == '.!chat.!toolbar.clear':
            event.widget.configure(image=self.icons['clear'])

        elif event.widget.__str__() == '.!toolbar.check':
            if not Scratch.SHOW_CHECKLISTS:
                event.widget.configure(image=self.icons['checkbox'])
            else:
                event.widget.configure(image=self.icons['checkbox-solid'])
        
        elif event.widget.__str__() == '.!toolbar.calendar':
            if not Scratch.SHOW_REMINDERS:
                event.widget.configure(image=self.icons['calendar'])
            else:
                event.widget.configure(image=self.icons['calendar-solid'])
            
        elif event.widget.__str__() == '.!toolbar.note':
            if not Scratch.SHOW_NOTES:
                event.widget.configure(image=self.icons['document'])
            else:
                event.widget.configure(image=self.icons['document-solid'])

        elif event.widget.__str__() == '.!toolbar.speech':
            if not Scratch.SPEECH_RECOGNITION:
                event.widget.configure(image=self.icons['mic'])
            else:
                event.widget.configure(image=self.icons['mic-solid'])
        
        elif event.widget.__str__() == '.!toolbar.chat':
            if not Scratch.CHAT_ON:
                event.widget.configure(image=self.icons['android'])
            else:
                event.widget.configure(image=self.icons['android-solid'])
        
        elif event.widget.__str__() == '.!chat.!frame2.send_chat':
            event.widget.configure(image=self.icons['paper-plane'])
        
        else:
            event.widget.configure(bg='white')
    
    def save(self, event=None):
        '''
        Save current items
        '''
        items = []
        excluded = ['!toolbar', '!chat']
        
        for item in self.children.keys():
            if item not in excluded and '!addmenu' not in item:
                items.append(self.children[item].to_object())

        db = shelve.open('scratch.db')
        db['show_checklists'] = Scratch.SHOW_CHECKLISTS
        db['show_reminders'] = Scratch.SHOW_REMINDERS
        db['show_notes'] = Scratch.SHOW_NOTES
        db['items'] = items
        db.close()

        self.start_backup_thread()
    
    def load(self):
        '''
        Load saved items
        '''
        db = shelve.open('scratch.db')
        items = []
        
        if 'items' in db.keys():
            items = db['items']
        
        if 'show_checklists' in db.keys():
            Scratch.SHOW_CHECKLISTS = db['show_checklists']
        if 'show_reminders' in db.keys():
            Scratch.SHOW_REMINDERS = db['show_reminders']
        if 'show_notes' in db.keys():
            Scratch.SHOW_NOTES = db['show_notes']
            
        db.close()
        return items
    
    def toggle_module(self, event, module: str):
        '''
        Toggle Modules
        '''
        items = self.children.copy()
        
        if module == 'reminder':
            Scratch.SHOW_REMINDERS = False if Scratch.SHOW_REMINDERS else True
            for item in items:
                if module in item.__str__():
                    if not Scratch.SHOW_REMINDERS and not self.children[item].locked:
                        self.children[item].withdraw()
                        self.children[item].is_withdrawn = True
                    else:
                        self.children[item].deiconify()
                        self.children[item].is_withdrawn = False
        elif module == 'checklist':
            Scratch.SHOW_CHECKLISTS = False if Scratch.SHOW_CHECKLISTS else True
            for item in items:
                if module in item.__str__():
                    if not Scratch.SHOW_CHECKLISTS and not self.children[item].locked:
                        self.children[item].withdraw()
                        self.children[item].is_withdrawn = True
                    else:
                        self.children[item].deiconify()
                        self.children[item].is_withdrawn = False
        elif module == 'note':
            Scratch.SHOW_NOTES = False if Scratch.SHOW_NOTES else True
            for item in items:
                if module in item.__str__():
                    if not Scratch.SHOW_NOTES and not self.children[item].locked:
                        self.children[item].withdraw()
                        self.children[item].is_withdrawn = True
                    else:
                        self.children[item].deiconify()
                        self.children[item].is_withdrawn = False
    
    def toggle_modules_on_start(self):
        '''
        Toggle All Modules
        '''
        items = self.children.copy()
        
        for item in items:
            item_id = item.__str__()
            if 'reminder' in item_id or 'checklist' in item_id or 'note' in item_id:
                if self.children[item].is_withdrawn:
                    self.children[item].withdraw()
                    self.children[item].is_withdrawn = True

    def reload(self):
        '''
        Rearrange items on item deletion
        
        @return None
        '''
        pass
        
    def backup(self):
        ''''
        Backup app to online database
        
        @return None
        '''
        try:
            items = self.children.copy()
            
            for item in items:
                if item not in'!toolbar' and item not in '!addmenu':
                    backup_item = self.children[item].to_object()
                    
                    if backup_item['type'] == 'reminder':
                        dt = backup_item['date_time']
                        backup_item['date_time'] = dt.strftime("%a %b %d %Y %H:%M:%S")
                        
                    if backup_item['_id'] is None:
                        result = Document.runnable_db.insert_one(document=backup_item)
                        if (result['status'] == 'success'):
                            self.children[item]._id = result['msg']
                    else:
                        updated = backup_item
                        
                        del updated['_id']
                        result = Document.runnable_db.update(_filter={'id': backup_item['_id']}, update=updated)
                        
        except Exception:
            pass
        
    def auto_backup(self, interval=18000):
        while True:
            try:
                self.backup()
                sleep(interval)
            except Exception:
                pass


if __name__ == '__main__':
    App = Scratch()

    style = ttk.Style()
    style.theme_use('xpnative')
    style.configure('TCheckButton', bg='black')
    style.configure('TEntry', bg='black')

    App.mainloop()
