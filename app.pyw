__author__ = 'ph4n70m'
__version__ = '0.01'

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from toolbar import ToolBar
from note import Note
from checklist import CheckList
from addmenu import AddMenu
from reminder import Reminder
    
import shelve


class Scratch(Tk):
    '''
    Main self window
    '''
    WIDTH = 250
    HEIGHT = 250
    MENU_OPEN = False

    def __init__(self, **kw):
        super().__init__(**kw)
 
        screen_width = self.winfo_screenwidth()
        self.posX = screen_width - Scratch.WIDTH
        self.geometry(f"+%d+0" % self.posX)
        self.overrideredirect(1)
        self.minsize(width=Scratch.WIDTH, height=40)
        self.attributes('-alpha', 0.7)

        self['background'] = '#161a1d'

        self.content()

    def content(self):
        '''
        Main self Components
        '''

        self.top_frame = ToolBar(
            self,
            bg='black',
            add_btn=True,
            add_btn_command=self.toggle_add_menu
        )
        
        

        self.top_frame.pack(side=TOP, fill=X)
        
        # settings_icon = Image.open('images/gear.png').convert('RGBA')
        # #settings_icon = ImageOps.invert(settings_icon)
        # settings_icon = ImageTk.PhotoImage(settings_icon.resize((20,20)))
        
        # settings_btn = Button(
        #     self.top_frame,
        #     image=settings_icon,
        #     text='',
        #     compound='left'
        # )

        # #settings_btn.pack(side=RIGHT, ipadx=5)

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

        screen_width = self.winfo_screenwidth()
        width = screen_width - ((last_item['width'] + last_item['posX']).WIDTH*2)
        
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

        return (self.winfo_screenwidth() - (last_item.winfo_width()*2))-10
        

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
        if event.widget.cget('text') == '+':
            event.widget.configure(bg='turquoise')
        else:
            event.widget.configure(bg='brown')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        event.widget.configure(bg='black')
    
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