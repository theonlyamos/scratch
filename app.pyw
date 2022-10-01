__author__ = 'ph4n70m'
__version__ = '0.0.4'

from tkinter import *
from tkinter import ttk
from PIL import ImageTk

from toolbar import ToolBar
from note import Note
from checklist import CheckList
from addmenu import AddMenu
from reminder import Reminder
    
import shelve

from icons import BarsIcon, GearIcon, CalendarPlusIcon,\
                    CalendarCheckIcon, CalendarDaysIcon, \
                    PlusIcon, SquareIcon, SquareCheckIcon, \
                    SquarePlusIcon, TrashCanIcon, CheckIcon, \
                    XMarkIcon, SquareXMarkIcon, NoteStickyIcon, \
                    CheckDoubleIcon


class Scratch(Tk):
    '''
    Main self window
    '''
    WIDTH = 250
    HEIGHT = 250
    MENU_OPEN = False
    SHOW_CHECKLISTS = True
    SHOW_NOTES = True
    SHOW_REMINDERS = True

    def __init__(self, **kw):
        super().__init__(**kw)
 
        screen_width = self.winfo_screenwidth()
        self.posX = screen_width - Scratch.WIDTH
        self.geometry(f"+%d+0" % self.posX)
        self.overrideredirect(1)
        self.minsize(width=Scratch.WIDTH, height=40)
        self.attributes('-alpha', 0.7)

        self['background'] = '#161a1d'

        self.build_icons()
        self.content()

    def build_icons(self):
        self.icons = {
            'settings'  : ImageTk.PhotoImage(GearIcon.resize((12, 12))),
            'menu'      : ImageTk.PhotoImage(BarsIcon.resize((12, 12))),
            'trash'     : ImageTk.PhotoImage(TrashCanIcon.resize((12, 12))),
            'close'     : ImageTk.PhotoImage(XMarkIcon.resize((8, 12))),
            'plus'      : ImageTk.PhotoImage(PlusIcon.resize((12, 12))),
            'check'      : ImageTk.PhotoImage(CheckIcon.resize((12, 12))),
            'check-double'      : ImageTk.PhotoImage(CheckDoubleIcon.resize((9, 9))),
            'note'   : ImageTk.PhotoImage(NoteStickyIcon.resize((12, 12))),
            'square'    : ImageTk.PhotoImage(SquareIcon.resize((12, 12))),
            'square-plus'    : ImageTk.PhotoImage(SquarePlusIcon.resize((12, 12))),
            'square-check'   : ImageTk.PhotoImage(SquareCheckIcon.resize((12, 12))),
            'square-close'   : ImageTk.PhotoImage(SquareXMarkIcon.resize((12, 12))),
            'calendar'       : ImageTk.PhotoImage(CalendarDaysIcon.resize((12, 12))),
            'calendar-plus'  : ImageTk.PhotoImage(CalendarPlusIcon.resize((12, 12))),
            'calendar-check' : ImageTk.PhotoImage(CalendarCheckIcon.resize((12, 12)))}

    def content(self):
        '''
        Main self Components
        '''

        self.top_frame = ToolBar(
            self,
            bg='white',
            add_btn=True,
            add_btn_command=self.toggle_add_menu
        )
        
        

        self.top_frame.pack(side=TOP, ipady=8, fill=X)
        
        settings_btn = Label(
            self.top_frame,
            image=self.icons['settings'],
            compound='left',
            name='settings',
            bg='white'
        )

        settings_btn.pack(side=RIGHT, ipadx=3, ipady=3)
        settings_btn.bind('<Enter>', self.hover)
        settings_btn.bind('<Leave>', self.leave)
        # settings_btn.bind('<ButtonPress-1>', self.close_app)
        
        calendar_btn = Label(
            self.top_frame,
            image=self.icons['calendar'],
            text='',
            compound='left',
            name='calendar',
            bg='violet' if Scratch.SHOW_CHECKLISTS else 'white'
        )

        calendar_btn.pack(side=RIGHT, padx=5, ipadx=3, ipady=3)
        calendar_btn.bind('<Enter>', self.hover)
        calendar_btn.bind('<Leave>', self.leave)
        calendar_btn.bind('<ButtonPress-1>', lambda e: self.toggle_module(e, 'reminder'))
        
        note_btn = Label(
            self.top_frame,
            image=self.icons['note'],
            text='',
            compound='left',
            name='note',
            bg='lime' if Scratch.SHOW_CHECKLISTS else 'white'
        )

        note_btn.bind('<Enter>', self.hover)
        note_btn.bind('<Leave>', self.leave)
        note_btn.bind('<ButtonPress-1>', lambda e: self.toggle_module(e, 'note'))
        note_btn.pack(side=RIGHT, ipadx=3, ipady=3)
        
        check_btn = Label(
            self.top_frame,
            image=self.icons['check'],
            text='',
            compound='left',
            name='check',
            bg='#66FFFF' if Scratch.SHOW_CHECKLISTS else 'white'
        )

        check_btn.pack(side=RIGHT, padx=5, ipadx=3, ipady=3)
        check_btn.bind('<Enter>', self.hover)
        check_btn.bind('<Leave>', self.leave)
        check_btn.bind('<ButtonPress-1>', lambda e: self.toggle_module(e, 'checklist'))

        self.add_menu_window = None

        items = self.load()
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

        self.bind('<FocusOut>', self.save)
    
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
    
    def hover(self, event=None):
        '''
        Change foreground color on mouse enter
        '''
        if event.widget.__str__() == '.!toolbar.settings':
            event.widget.configure(bg='gold')
        elif event.widget.__str__() == '.!toolbar.check':
            event.widget.configure(bg='#66FFFF')
        elif event.widget.__str__() == '.!toolbar.note':
            event.widget.configure(bg='lime')
        elif event.widget.__str__() == '.!toolbar.calendar':
            event.widget.configure(bg='violet')
        else:
            event.widget.configure(bg='red')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        if event.widget.__str__() == '.!toolbar.check':
            if not Scratch.SHOW_CHECKLISTS:
                event.widget.configure(bg='white')
        elif event.widget.__str__() == '.!toolbar.calendar':
            if not Scratch.SHOW_REMINDERS:
                event.widget.configure(bg='white')
        elif event.widget.__str__() == '.!toolbar.note':
            if not Scratch.SHOW_NOTES:
                event.widget.configure(bg='white')
        else:
            event.widget.configure(bg='white')
    
    def save(self, event=None):
        '''
        Save current items
        '''
        items = []
        for item in self.children.keys():
            if not '!toolbar' in item and not '!addmenu' in item:
                items.append(self.children[item].to_object())

        db = shelve.open('scratch.db')
        db['items'] = items
        db.close()
    
    def load(self, event=None):
        '''
        Load saved items
        '''
        db = shelve.open('scratch.db')
        items = []
        if 'items' in db.keys():
            items = db['items']
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
                    if not Scratch.SHOW_REMINDERS:
                        self.children[item].withdraw()
                    else:
                        self.children[item].deiconify()
        elif module == 'checklist':
            Scratch.SHOW_CHECKLISTS = False if Scratch.SHOW_CHECKLISTS else True
            for item in items:
                if module in item.__str__():
                    if not Scratch.SHOW_CHECKLISTS:
                        self.children[item].withdraw()
                    else:
                        self.children[item].deiconify()
        elif module == 'note':
            Scratch.SHOW_NOTES = False if Scratch.SHOW_NOTES else True
            for item in items:
                if module in item.__str__():
                    if not Scratch.SHOW_NOTES:
                        self.children[item].withdraw()
                    else:
                        self.children[item].deiconify()
    
    def reload(self):
        '''
        Rearrange items on item deletion
        '''
        pass
        # items = self.children.copy()
        
        # for item in items.keys():
        #     if self.children[item]:
        #         self.children[item].destroy()
        
        # self.content()


if __name__ == '__main__':
    App = Scratch()

    style = ttk.Style()
    style.theme_use('xpnative')
    style.configure('TCheckButton', bg='black')
    style.configure('TEntry', bg='black')

    App.mainloop()
