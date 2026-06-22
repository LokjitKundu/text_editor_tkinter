import tkinter as tk
from tkinter import filedialog as fd, simpledialog as sd
from tkinter import messagebox as msg

import os

class NotepadGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Notepad")
        self.file_path=None
        self.text_box()
        self.menu_bar()
        self.set_icon()

    def check_textbox_state(self):
        # Checks the text box state right before the menu drops down (empty or not)
        if not self.text_area.get("1.0","end-1c"):
            self.edit_menu.entryconfig("Cut",state="disabled")
            self.edit_menu.entryconfig("Copy",state="disabled")
        else:
            self.edit_menu.entryconfig("Cut",state="normal")
            self.edit_menu.entryconfig("Copy",state="normal")

    def check_clipboard_state(self):
        # Checks the clipboard right before menu drops down (empty or not)
        try:
            # Tries to get clipboard text
            clipboard_contains=self.text_area.clipboard_get()
            # when the clipboard is not empty
            if not clipboard_contains:
                self.edit_menu.entryconfig("Paste",state="disabled")
            # If text is an empty string ""
            else:
                self.edit_menu.entryconfig("Paste",state="normal")
        # when the clipboard is empty / non-text clipboard
        except tk.TclError:
            self.edit_menu.entryconfig("Paste",state="disabled")
            
    def combined_func(self):
        self.check_clipboard_state() # checks if the clipboard contains text and enables/disables the paste menu accordingly
        self.check_textbox_state() # checks if the text area contains text and enables/disables cut and paste menu accordingly

    def new_file(self):
        # deletes the text of text_area 
        self.text_area.delete("1.0", "end")
        self.title("Untitled - Notepad")
        self.file_path=None

    def open_file(self):
        # opens the file path picker window
        self.file_path=fd.askopenfilename(filetypes=[("All Files","*.*"),("Text Documents","*.txt")]) # returns an empty string if user cancels else returns the file path as a string
        #if user clicks cancel
        if not self.file_path:
            self.file_path=None
            return
        #if user clicks open
        self.title(os.path.basename(self.file_path)+" - Notepad") # returns the file name from a file path
        self.text_area.delete("1.0","end") # clears current content
        with open (self.file_path,"r") as f:
            self.text_area.insert("1.0",f.read()) # reads the file and inserts into notepad
                
    def save_file(self):
        # if the current document does not have a file path
        if not self.file_path:
            self.save_as()
            return
        # if the current document does have a file path
        current_content=self.text_area.get("1.0","end")
        with open (self.file_path,"w") as f:
            f.write(current_content)
        self.title(os.path.basename(self.file_path)+" - Notepad") # returns filename


    def save_as(self):

        current_content=self.text_area.get("1.0","end")
        new_path=fd.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Documents","*.txt"),("All Files","*.*")],confirmoverwrite=True) # returns an empty string if user cancels else returns the file path as a string
        # if user clicks cancel
        if not new_path:
            return
        # if user clicks save
        self.file_path=new_path
        with open (self.file_path,"w") as f:
            f.write(current_content)
        self.title(os.path.basename(self.file_path)+" - Notepad") # returns file name

    
    def print_file(self):
        pass
    
    def quit_app(self):
        # permanently closes the application window
        self.destroy()
    
    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            return
        
    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            return

    def cut(self):
        self.text_area.event_generate(("<<Cut>>"))
    
    def copy(self):
        self.text_area.event_generate(("<<Copy>>"))
    
    def paste(self):
        self.text_area.event_generate(("<<Paste>>"))
    
    def delete(self):
        # incomplete
        self.text_area.delete("1.0","end")
    
    def go_to(self):

        line_num=sd.askinteger("Go To Line","Enter line number:") # returns None if pressed cancel or close button
        
        if line_num is None:
            return
        # line number starts from 1 in tkinter, less than that is invalid
        if line_num<=0:
            msg.showwarning("Notepad","Please enter a positive line number")
            return
        
        target_index=f"{line_num}.0" # text index format - line.character

        # checks if inputted line num exceeds last last line num
        last_line_num=int(self.text_area.index("end-1c").split(".")[0]) 
        if last_line_num<line_num:
            msg.showwarning("Notepad","The line number is beyond total number of lines")
            return
            
        self.text_area.focus_set() # moves keyboard focus to text_area
        self.text_area.mark_set("insert",target_index) # insert refers to "the blinking cursor", moves the cursor to target_index
        self.text_area.see(target_index) # automatically scroll to target_index
    
    def select_all(self):
        # selects all
        self.text_area.tag_add("sel","1.0","end")
        
        last_char_index=self.text_area.index("end-1c") 
        self.text_area.mark_set("insert",last_char_index) # moves the cursor to last_char_index
        self.text_area.focus_set() # moves keyboard focus to text_area
        self.text_area.see(last_char_index) # automatically scroll to last_char_index
    
    def zoom_in(self):
        pass
    
    def zoom_out(self):
        pass
    
    def default_zoom(self):
        pass
    
    def status_bar(self):
        pass

    def set_icon(self):

        icon_path=os.path.join(os.path.dirname(__file__),"assets","text_editor_icon.ico")
        self.wm_iconbitmap(icon_path)

    def menu_bar(self):
        
        # creating a new file every time the app is opened
        self.new_file()

        menu_bar=tk.Menu(self)

        # file menu 
        self.file_menu=tk.Menu(menu_bar,tearoff=0)
        
        self.file_menu.add_command(label="New",command=self.new_file)
        self.file_menu.add_command(label="Open",command=self.open_file)
        self.file_menu.add_command(label="Save",command=self.save_file)
        self.file_menu.add_command(label="Save as",command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Print",command=self.print_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",command=self.quit_app)
        
        menu_bar.add_cascade(label="File",menu=self.file_menu)

        # edit menu
        self.edit_menu=tk.Menu(menu_bar,tearoff=0,postcommand=self.combined_func) # postcommand pauses the menu from rendering for microsecond and checks textbox is empty or not

        self.edit_menu.add_command(label="Undo",command=self.undo)
        self.edit_menu.add_command(label="Redo",command=self.redo)
        self.edit_menu.add_command(label="Cut",command=self.cut)
        self.edit_menu.add_command(label="Copy",command=self.copy)
        self.edit_menu.add_command(label="Paste",command=self.paste)
        self.edit_menu.add_command(label="Delete",command=self.delete)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Go to",command=self.go_to)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select all",command=self.select_all)
        
        menu_bar.add_cascade(label="Edit",menu=self.edit_menu)

        # view menu
        self.view_menu=tk.Menu(menu_bar,tearoff=0)

        self.zoom_submenu=tk.Menu(self.view_menu,tearoff=0)
        self.zoom_submenu.add_command(label="Zoom in",command=self.zoom_in)
        self.zoom_submenu.add_command(label="Zoom out",command=self.zoom_out)
        self.zoom_submenu.add_command(label="Restore default zoom",command=self.default_zoom)
        self.view_menu.add_cascade(label="Zoom",menu=self.zoom_submenu)

        self.view_menu.add_checkbutton(label="Status bar",command=self.status_bar)   
        
        menu_bar.add_cascade(label="View",menu=self.view_menu)
        
        self.config(menu=menu_bar)

    def text_box(self):
        
        frame=tk.Frame(self)
        frame.pack(fill="both",expand=True)

        #scroll bar
        scroll_bar=tk.Scrollbar(frame)
        scroll_bar.pack(side="right",fill="y")
        #text area
        self.text_area=tk.Text(frame,font="consolas 10",yscrollcommand=scroll_bar.set,undo=True)
        self.text_area.pack(side="left",fill="both",expand=True)
        
        scroll_bar.config(command=self.text_area.yview)

if __name__=="__main__":
    gui=NotepadGui()
    gui.mainloop()