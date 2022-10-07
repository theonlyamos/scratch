from tkinter import *

class ToolBar(Frame):
    '''
    Toolbar Frame for all windows
    '''
    def __init__(self, master=None, add_btn=False, add_btn_command=None, close_btn=True, lock_btn=True, **kw):
        super().__init__(master, **kw)
        self.show_close_btn = close_btn
        self.show_add_btn = add_btn
        self.show_lock_btn = lock_btn
        self.add_btn_command = add_btn_command if add_btn_command else lambda e: e
        self.content()
    
    def content(self):
        '''
        Add components
        '''

        if self.show_add_btn:
            add_icon = self.master.icons['plus'] if self.master.__str__() == '.' else self.master.master.icons['plus']
            add_btn = Label(
                self, 
                image=add_icon,
                compound='left',
                name='add',
                bg=self['background']
            )

            add_btn.bind('<Enter>', self.hover)
            add_btn.bind('<Leave>', self.leave)
            add_btn.bind('<ButtonPress-1>', self.add_btn_command)
            add_btn.pack(side=LEFT, padx=5)

        if self.show_close_btn:
            close_icon = self.master.icons['circle-close-r'] if self.master.__str__() == '.' else self.master.master.icons['circle-close-r']
            close_btn = Label(
                self, 
                image=close_icon,
                compound='left',
                name='close',
                bg=self['background']
            )

            close_btn.bind('<Enter>', self.hover)
            close_btn.bind('<Leave>', self.leave)
            close_btn.bind('<ButtonPress-1>', self.close_app)
            close_btn.pack(side=RIGHT, padx=2, ipadx=3, ipady=3)
        
        if self.show_lock_btn:
            lock_btn = Label(
                self, 
                image=self.master.master.icons['lock'] if self.master.locked else self.master.master.icons['unlock'],
                compound='left',
                name='lock',
                bg=self['background']
            )

            lock_btn.bind('<ButtonPress-1>', self.toggle_locked)
            lock_btn.pack(side=RIGHT, padx=2)
        
        # minimize_btn = Label(
        #         self, 
        #         text='-',
        #         bg=self['background'],
        #         fg='white',
        #         font='Helvetica 20 normal'
        #     )

        # minimize_btn.bind('<Enter>', self.hover)
        # minimize_btn.bind('<Leave>', self.leave)
        # minimize_btn.bind('<ButtonPress-1>', self.close_app)
        # minimize_btn.pack(side=RIGHT, ipadx=5)
        
        self.bind('<B1-Motion>', lambda e: self.on_motion(e))
    
    def hover(self, event=None):
        '''
        Change foreground color on mouse enter
        '''
        if '.!toolbar.close' in event.widget.__str__():
            #event.widget.configure(bg='crimson')
            close_icon = self.master.icons['circle-close'] if self.master.__str__() == '.' else self.master.master.icons['circle-close']
            event.widget.configure(image=close_icon)
        elif '.!toolbar.add' in event.widget.__str__():
            add_icon = self.master.icons['plus-square'] if self.master.__str__() == '.' else self.master.master.icons['plus-square']
            event.widget.configure(image=add_icon)
        elif not event.widget.cget('text'):
            event.widget.configure(bg='gold')
        else:
            event.widget.configure(fg='brown')

    def leave(self, event=None):
        '''
        Revert foreground color to default
        '''
        if '.!toolbar.close' in event.widget.__str__():
            #event.widget.configure(bg=self['background'])
            close_icon = self.master.icons['circle-close-r'] if self.master.__str__() == '.' else self.master.master.icons['circle-close-r']
            event.widget.configure(image=close_icon)
        elif '.!toolbar.add' in event.widget.__str__():
            #event.widget.configure(bg=self['background'])
            add_icon = self.master.icons['plus'] if self.master.__str__() == '.' else self.master.master.icons['plus']
            event.widget.configure(image=add_icon)
        elif not event.widget.cget('text'):
            event.widget.configure(bg='white')
        else:
            event.widget.configure(fg='white')
    
    def on_motion(self, event):
        if self.master.__str__() != '.':
            deltax = event.x
            deltay = event.y
            x = self.master.winfo_x()+deltax
            y = self.master.winfo_y()+deltay
            self.master.geometry("+%s+%s" %(x, y))
            self.master.master.save()
    
    def close_app(self, event=None):
        '''
        Close the program
        '''
        toplevel = self.master if self.master.__str__() == '.' else self.master.master
        toplevel.save()
        
        if self.master.__str__() != '.' and 'checklist' in self.master.__str__():
            parent = self.master.to_object()
            if parent['is_sublist']:
                check_item = parent['item_id'].split('.')[-1]
                parent_id = parent['item_id'].split('.')[1]
                
                checklist = self.master.master.children[parent_id]
                checklist.children[check_item].reset()
        
        if toplevel.__str__() != self.master.__str__():
            self.master.destroy()
            toplevel.save()
            toplevel.reload()
        else:
            toplevel.destroy()
    
    def toggle_locked(self, event=None):
        '''
        Toggle item lock
        '''
        if self.master.locked:
            self.master.locked = False
            event.widget.configure(image=self.master.master.icons['unlock'])
        else:
            self.master.locked = True
            event.widget.configure(image=self.master.master.icons['lock'])
          
        
        