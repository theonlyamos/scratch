__author__ = 'ph4n70m'
__version__ = '0.01'

from tkinter import *
from tkinter import ttk

from toolbar import ToolBar
from note import Note
from checklist import CheckList
from addmenu import AddMenu
    
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

        self.add_menu_window = None

        items = self.load()

        for index, item in enumerate(items):
            item_type = item['type']
            del item['type']

            if item_type == 'checklist':
                CheckList(self, **item)
            elif item_type == 'note':
                Note(self, **item)
            else:
                print('Not a valid type')

        self.bind('<FocusOut>', self.save)
    
    def get_posY(self)->int:
        '''
        Calculate next item positioning
        '''
        posY = 0
        for item in self.children.values():
            posY += item.winfo_height()
        
        posY += len(self.children.values())*10
        return posY

    def new_item(self, event=None, item='note'):
        '''
        Open Toplevel window for creating \n
        new item
        '''
        # toggle_add_menu()
        
        if item == 'note':
            posY = self.get_posY()

            new_note_window = Note(
                self,
                width=Scratch.WIDTH,
                posX=self.posX,
                posY=posY
            )
            self.save()
            new_entry = new_note_window.show()
            # save_note(new_entry.strip())
        
        elif item == 'checklist':
            posY = self.get_posY()
            
            checklist_window = CheckList(
                self,
                width=Scratch.WIDTH,
                posX=self.posX,
                posY=posY
            )
            self.save()
            new_checklist = checklist_window.show()
            # save_note(new_checklist.strip())
    
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
            if  '!toolbar' in item:
                pass 
            elif '!addmenu' in item:
                pass
            else:
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


if __name__ == '__main__':
    App = Scratch()

    style = ttk.Style()
    style.theme_use('xpnative')
    style.configure('TCheckButton', bg='black')
    style.configure('TEntry', bg='black')

    App.mainloop()