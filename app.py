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
        self.font_size=10
        self.show_status_bar=tk.BooleanVar(value=True) # object linked to the "Status Bar" checkbutton; True = checked, False = unchecked

        self.text_box()
        self.menu_bar()
        self.set_icon()

    def check_selection_status(self):
        # if text is selected
        if self.text_area.tag_ranges("sel"): 
            self.edit_menu.entryconfig("Delete",state="normal")
        #if nothing is selected
        else:
            self.edit_menu.entryconfig("Delete",state="disabled")

    def check_textbox(self):
        # Checks the text box right before the menu drops down (empty or not)
        if not self.text_area.get("1.0","end-1c"):
            self.edit_menu.entryconfig("Cut",state="disabled")
            self.edit_menu.entryconfig("Copy",state="disabled")
        else:
            self.edit_menu.entryconfig("Cut",state="normal")
            self.edit_menu.entryconfig("Copy",state="normal")

    def check_clipboard(self):
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
        self.check_clipboard() # checks if the clipboard contains text and enables/disables the "paste" menu accordingly
        self.check_textbox() # checks if the text area contains text and enables/disables "cut" and "copy" menu accordingly
        self.check_selection_status() # checks if any text is selected or not abd enables/disables "delete" menu accordingly

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
        try:
            self.title(os.path.basename(self.file_path)+" - Notepad") # returns the file name from a file path
            self.text_area.delete("1.0","end") # clears current content
            with open (self.file_path,"r") as f:
                self.text_area.insert("1.0",f.read()) # reads the file and inserts into notepad
        except UnicodeDecodeError:
            msg.showerror("Notepad","This file cannot be opened as plain text")

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
        if not self.file_path:
            msg.showerror("Notepad","Please save the file before printing")
            return
        try:
            os.startfile(self.file_path,"print")
        except OSError:
            msg.showerror("Notepad","This file type is not supported")
            
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

        try:
            self.text_area.delete("sel.first","sel.last")
        except tk.TclError:
            return
        
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
        if self.font_size==72:
            return
        self.font_size+=1
        self.text_area.config(font=f"consolas {self.font_size}")
    
    def zoom_out(self):
        if self.font_size==8:
            return
        self.font_size-=1
        self.text_area.config(font=f"consolas {self.font_size}")
    
    def default_zoom(self):
        self.font_size=10
        self.text_area.config(font=f"consolas {self.font_size}")

    def update_status_bar(self,event=None):

        line,column=self.text_area.index("insert").split(".")
        self.status_label.config(text=f"Line {line}, Column {column}")
    
    def status_bar(self):
        # if checkbutton is ticked
        if self.show_status_bar.get():
            self.status_label.pack(side="bottom",fill="x")
            self.update_status_bar()
        # if checkbutton is not ticked
        else:
            self.status_label.pack_forget() # hides a widget that was packed using pack()
            

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

        self.view_menu.add_checkbutton(label="Status bar",command=self.status_bar,variable=self.show_status_bar) # keeps track of the checkbutton state
        
        menu_bar.add_cascade(label="View",menu=self.view_menu)
        
        self.config(menu=menu_bar)

    def text_box(self):
        
        frame=tk.Frame(self)
        frame.pack(fill="both",expand=True)

        # scroll bar
        scroll_bar=tk.Scrollbar(frame)
        scroll_bar.pack(side="right",fill="y")
        # text area
        self.text_area=tk.Text(frame,font=f"consolas {self.font_size}",yscrollcommand=scroll_bar.set,undo=True)
        self.text_area.pack(side="left",fill="both",expand=True)
        
        scroll_bar.config(command=self.text_area.yview)
        # status bar
        self.status_label=tk.Label(self,text="Line 1, Column 0",anchor="w")
        self.status_label.pack(side="bottom",fill="x") # by default the status bar is visible

        self.text_area.bind("<KeyRelease>",self.update_status_bar)
        self.text_area.bind("ButtonRelease>",self.update_status_bar)

if __name__=="__main__":
    gui=NotepadGui()
    gui.mainloop()