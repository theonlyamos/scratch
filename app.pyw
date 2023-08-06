__author__ = 'ph4n70m'
__version__ = '0.0.4'

from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from threading import Thread

from toolbar import ToolBar
from note import Note
from checklist import CheckList
from addmenu import AddMenu
from reminder import Reminder
from settings import Settings
from speech import speech, get_audio

from runit_database import Document
from datetime import datetime
from time import sleep
import shelve
    
from icons import icons

Document.initialize(
    'http://runit.test:9000/api',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjkzMDQxNCwianRpIjoiOWU5YmIwMDAtOWJkNS00ZWI4LTg4YWEtYWViMjYzNDU3NGI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyYjAxY2E4ZGVmN2YzMTcwMDNiZWUyYiIsIm5iZiI6MTY4NjkzMDQxNCwiZXhwIjoxNjg5NTIyNDE0fQ.OJq8c4DgBI1haEgbS9NHMDxYAQtaFIzTHSopaiZNeSc',
    '648c7f6886abacf21d21faf2'
)

class Scratch(Tk):
    '''
    Main self window
    '''
    WIDTH = 250
    HEIGHT = 250
    SHOW_NOTES = True
    MENU_OPEN = False
    SHOW_REMINDERS = True
    SETTINGS_OPEN = False
    SHOW_CHECKLISTS = True
    SPEECH_RECOGNITION = True

    def __init__(self, **kw):
        super().__init__(**kw)
 
        screen_width = self.winfo_screenwidth()
        self.posX = screen_width - Scratch.WIDTH
        self.geometry(f"+%d+0" % self.posX)
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
            bg='white'
        )

        settings_btn.pack(side=RIGHT)
        settings_btn.bind('<Enter>', self.hover)
        settings_btn.bind('<Leave>', self.leave)
        settings_btn.bind('<ButtonPress-1>', self.toggle_settings)
        
        calendar_btn = Label(
            self.top_frame,
            image=self.icons['calendar-solid' if Scratch.SHOW_REMINDERS else 'calendar'],
            text='',
            compound='left',
            name='calendar'
        )

        calendar_btn.pack(side=RIGHT, padx=5)
        calendar_btn.bind('<Enter>', self.hover)
        calendar_btn.bind('<Leave>', self.leave)
        calendar_btn.bind('<ButtonPress-1>', lambda e: self.toggle_module(e, 'reminder'))
        
        note_btn = Label(
            self.top_frame,
            image=self.icons['document-solid' if Scratch.SHOW_NOTES else 'document'],
            text='',
            compound='left',
            name='note',
        )

        note_btn.bind('<Enter>', self.hover)
        note_btn.bind('<Leave>', self.leave)
        note_btn.bind('<ButtonPress-1>', lambda e: self.toggle_module(e, 'note'))
        note_btn.pack(side=RIGHT)
        
        check_btn = Label(
            self.top_frame,
            image=self.icons['checkbox-solid'if Scratch.SHOW_CHECKLISTS else 'checkbox'],
            text='',
            compound='left',
            name='check'
        )

        check_btn.pack(side=RIGHT, padx=5)
        check_btn.bind('<Enter>', self.hover)
        check_btn.bind('<Leave>', self.leave)
        check_btn.bind('<ButtonPress-1>', lambda e: self.toggle_module(e, 'checklist'))

        speech_btn = Label(
            self.top_frame,
            image=self.icons['mic-solid' if Scratch.SPEECH_RECOGNITION else 'mic'],
            compound='left',
            name='speech',
            bg='white'
        )

        speech_btn.pack(side=LEFT)
        speech_btn.bind('<Enter>', self.hover)
        speech_btn.bind('<Leave>', self.leave)
        speech_btn.bind('<ButtonPress-1>', self.toggle_speech_recognition)

        self.top_frame.pack(side=TOP, ipady=8, fill=X)
        
        self.add_menu_window = None
        self.settings_window = None

        # Show Loaded Items
        new_pos = 0
        
        for index, item in enumerate(items):
            item_type = item['type']
            del item['type']
            

            # if not index:
            #     item['posY'] = 50
                
            # item['posX'] = self.posX

            if item_type == 'checklist':
                CheckList(self, **item)
            elif item_type == 'note':
                Note(self, **item)
            elif item_type == 'reminder':
                Reminder(self, **item)
            else:
                print('Not a valid type')
        
        speech_thread = Thread(target=self.start_speech_recognition)
        speech_thread.daemon = True

        self.bind('<FocusOut>', self.save)
        self.after(100, lambda: speech_thread.start())
        self.toggle_modules_on_start()
    
    def get_posY(self)->int:
        '''
        Calculate next item veritcal positioning
        '''
        last_item = self.children[list(self.children.keys())[-1]]
        screen_y = last_item.winfo_height() + last_item.winfo_y()

        if (self.winfo_screenheight() - screen_y) > 200:
            return screen_y + 10
        return 48
        
    def get_posX(self)->int:
        '''
        Calculate next item veritcal positioning
        '''
        last_item = self.children[list(self.children.keys())[-1]]

        screen_y = last_item.winfo_height() + last_item.winfo_y()
        if last_item.winfo_x() == 0:
            return self.posX
        if (self.winfo_screenheight() - screen_y) > 200 and last_item.winfo_x() >= self.posX:
            return self.posX
        
        if (self.winfo_screenheight() - screen_y) > 200:
            return last_item.winfo_x()

        # return (self.winfo_screenwidth() - (last_item.winfo_width()+last_item.winfo_x()))-10
        return (last_item.winfo_x() - self.WIDTH)-10
        

    def new_item(self, event=None, item='note'):
        '''
        Open Toplevel window for creating \n
        new item
        '''
        posY = self.get_posY()
        posX = self.get_posX()
        
        if item == 'note':
            new_note_window = Note(
                self,
                width=Scratch.WIDTH,
                posX=posX,
                posY=posY
            )
            self.save()
            new_entry = new_note_window.show()
            # save_note(new_entry.strip())
        
        elif item == 'checklist':
            checklist_window = CheckList(
                self,
                width=Scratch.WIDTH,
                posX=posX,
                posY=posY
            )
            self.save()
            new_checklist = checklist_window.show()
            # save_note(new_checklist.strip())
            
        elif item == 'reminder':
            reminder_window = Reminder(
                self,
                width=Scratch.WIDTH,
                posX=posX,
                posY=posY
            )
            self.save()
            new_reminder = reminder_window.show()
    
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
            Scratch.MENU_OPEN = False
            self.new_item(item=item.strip())

    def toggle_settings(self, event=None):
        '''
        Show/Hide Add Menu Frame
        '''

        if Scratch.SETTINGS_OPEN:
            Scratch.SETTINGS_OPEN = False
            self.settings_window.destroy()
        else:
            Scratch.SETTINGS_OPEN = True
            self.settings_window = Settings(
                self
            )
            item = self.settings_window.show()

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

        while Scratch.SPEECH_RECOGNITION:
            try:
                text = get_audio()
                speech(text)
            except Exception as e:
                print(str(e))
                pass

    def hover(self, event=None):
        '''
        Change foreground color on mouse enter
        '''

        if event.widget.__str__() == '.!toolbar.settings':
            event.widget.configure(image=self.icons['settings-solid'])
        
        elif event.widget.__str__() == '.!toolbar.check':
            if not Scratch.SHOW_CHECKLISTS:
                event.widget.configure(image=self.icons['checkbox'])
            else:
                event.widget.configure(image=self.icons['checkbox-solid'])
        
        elif event.widget.__str__() == '.!toolbar.note':
            if not Scratch.SHOW_NOTES:
                event.widget.configure(image=self.icons['document'])
            else:
                event.widget.configure(image=self.icons['document-solid'])
        
        elif event.widget.__str__() == '.!toolbar.calendar':
            if not Scratch.SHOW_REMINDERS:
                event.widget.configure(image=self.icons['calendar'])
            else:
                event.widget.configure(image=self.icons['calendar-solid'])
        
        elif event.widget.__str__() == '.!toolbar.speech':
            if not Scratch.SPEECH_RECOGNITION:
                event.widget.configure(image=self.icons['mic-solid'])
            else:
                event.widget.configure(image=self.icons['mic'])
        
        else:
            event.widget.configure(bg='red')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''

        if event.widget.__str__() == '.!toolbar.settings':
            event.widget.configure(image=self.icons['settings'])

        elif event.widget.__str__() == '.!toolbar.check':
            if not Scratch.SHOW_CHECKLISTS:
                event.widget.configure(image=self.icons['checkbox-solid'])
            else:
                event.widget.configure(image=self.icons['checkbox'])
        
        
        elif event.widget.__str__() == '.!toolbar.calendar':
            if not Scratch.SHOW_REMINDERS:
                event.widget.configure(image=self.icons['calendar-solid'])
            else:
                event.widget.configure(image=self.icons['calendar'])
            
        elif event.widget.__str__() == '.!toolbar.note':
            if not Scratch.SHOW_NOTES:
                event.widget.configure(image=self.icons['document-solid'])
            else:
                event.widget.configure(image=self.icons['document'])

        elif event.widget.__str__() == '.!toolbar.speech':
            if not Scratch.SPEECH_RECOGNITION:
                event.widget.configure(image=self.icons['mic'])
            else:
                event.widget.configure(image=self.icons['mic-solid'])

        else:
            event.widget.configure(bg='white')
    
    def save(self, event=None):
        '''
        Save current items
        '''
        items = []
        excluded = ['!toolbar', '!settings']
        for item in self.children.keys():
            if not item in excluded and not '!addmenu' in item:
                items.append(self.children[item].to_object())

        db = shelve.open('scratch.db')
        db['show_checklists'] = Scratch.SHOW_CHECKLISTS
        db['show_reminders'] = Scratch.SHOW_REMINDERS
        db['show_notes'] = Scratch.SHOW_NOTES
        db['items'] = items
        db.close()

        self.start_backup_thread()
    
    def load(self, event=None):
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
        # items = self.children.copy()
        
        # for item in items.keys():
        #     if self.children[item]:
        #         self.children[item].destroy()
        
        # self.content()
    
    def backup(self):
        ''''
        Backup app to online database
        
        @return None
        '''
        try:
            items = self.children.copy()
            
            for item in items:
                if not '!toolbar' in item and not '!addmenu' in item:
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
                        
        except:
            pass
        
    def auto_backup(self, interval=18000):
        while True:
            try:
                self.backup()
                sleep(interval)
            except:
                pass


if __name__ == '__main__':
    App = Scratch()

    style = ttk.Style()
    style.theme_use('xpnative')
    style.configure('TCheckButton', bg='black')
    style.configure('TEntry', bg='black')

    App.mainloop()
