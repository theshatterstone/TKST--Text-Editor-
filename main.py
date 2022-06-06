from email.policy import default
from tkinter import *
import tkinter.filedialog
import os

root = Tk()
#Program name
PROGRAM_NAME = root.title('TKST text editor')
root.geometry('600x700')
#all the code goes here
file_name = None
#variables used below
show_line_n = IntVar()
show_line_n.set(1)
show_cursor_locator = BooleanVar(value=True)
to_highlight_line = BooleanVar()

#functions for the program to operate 

def cut():
    textbox_area.event_generate('<<Cut>>')
    on_content_change

def copy():
    textbox_area.event_generate('<<Copy>>')
    on_content_change

def paste():
    textbox_area.event_generate('<<Paste>>')
    on_content_change

def undo():
    textbox_area.event_generate('<<Undo>>')
    on_content_change

def redo(event=None):
    textbox_area.event_generate('<<Redo>>')
    on_content_change
    return 'break'

def select_all(event=None):
    textbox_area.tag_add('sel','1.0','end')
    on_content_change
    return 'break'

def find_text(event=NONE):
    search_window = Toplevel(root)
    search_window.title('Find')
    search_window.transient(root)
    search_window.resizable(False,False)
    Label(search_window, text='Find').grid(row=0, column=0, sticky= 'e')
    search_entry = Entry(search_window, width=25)
    search_entry.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_window.focus_set()
    ignore_case_val = IntVar()
    Checkbutton(search_window, text='Ignore Case', variable=ignore_case_val).grid(row=1, column=1, padx=2, pady=2, sticky='we')
    Button(search_window, text='Find', underline=0, command=lambda: search_output(search_entry.get(), ignore_case_val.get(), textbox_area, search_window, search_entry)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)

def close_search_win():
    textbox_area.tag_remove('match', '1.0', END)
    search_window.destroy()
    search_window.protocol('WM_DELETE_WINDOW', close_search_win)
    return "break"

def search_output(needle, if_ignore_case, textbox_area, search_window, search_box):
    textbox_area
    matches_count = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = textbox_area.search(needle, start_pos, nocase =if_ignore_case, stopindex= END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos,len(needle))
            textbox_area.tag_add('match', start_pos, end_pos)
            matches_count += 1
            start_pos = end_pos
        textbox_area.tag_config('match', foreground = 'red', background = 'yellow')
    search_box.focus_set()
    search_window.title('{} matches found'.format(matches_count))
    
#current line highlighting
def highlight_line(interval=100):
    textbox_area.tag_remove('active_line',1.0,'end')
    textbox_area.tag_add('active_line','insert linestart','insert lineend+1c')
    textbox_area.after(interval, toggle_highlight)

def undo_highlight():
    textbox_area.tag_remove('active line', 1.0, 'end')

def toggle_highlight():
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()

# !!! FILE HANDLING !!!
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - TKST Text Editor'.format(os.path.basename(file_name)))
        textbox_area.delete(1.0, END)
        with open(file_name) as _file:
            textbox_area.insert(1.0, _file.read())

def save_file():
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)

def save_as():
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - TKST Text Editor'.format(os.path.basename(file_name)))
        textbox_area.delete(1.0, END)
        
def write_to_file():
    try:
        content = textbox_area.get('1.0', 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass

def new_file():
    root.title('Untitled')
    global file_name
    file_name = None
    textbox_area.delete('1.0', END)

#cursor info bar at bottom right
def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_locator.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()

def update_cursor_info_bar(event=NONE):
    row, col = textbox_area.index(INSERT).split('.')
    line_num, col_num = str(int(row)),str(int(col)+1) #col starts at 0
    infotext = 'Line: {0} | Column: {1}'.format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

top_bar = Menu(root)
'''
    !!!!!WARNING!!!!!
    The items in the menus below do not have function callbacks, 
    functions for them are to be created above and added later

'''
file_menu = Menu(top_bar, tearoff=0)
#file menu items
file_menu.add_command(label='New', accelerator='Ctrl + N', compound='left', command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl + O', compound='left', command=open_file)
file_menu.add_command(label='Save', accelerator='Ctrl + S', compound='left', command=save_file)
file_menu.add_command(label='Save As', accelerator='Ctrl + Shift + S', compound='left', command= save_as)

edit_menu = Menu(top_bar, tearoff=0)
#edit menu items
edit_menu.add_command(label='Undo', accelerator='Ctrl + Z', compound='left', command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl + Y', compound='left', command=redo)
edit_menu.add_command(label='Cut', accelerator='Ctrl + X', compound='left', command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl + C', compound='left', command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl + V', compound='left', command=paste)
edit_menu.add_command(label='Select All', accelerator='Ctrl + A', compound='left', command=select_all)
edit_menu.add_command(label='Find', accelerator='Ctrl + F', compound='left', command=find_text)

view_menu = Menu(top_bar, tearoff=0)
#view menu items
view_menu.add_checkbutton(label='Show line number', variable=show_line_n) 
view_menu.add_checkbutton(label='Show Cursor Location at the bottom', variable=show_cursor_locator, command=show_cursor_info_bar)
view_menu.add_checkbutton(label='Highlight current line', onvalue=1, offvalue=0, variable=to_highlight_line, command=toggle_highlight)

#themes menu (WIP, to be added when I have ideas for themes)
#theme_menu = Menu(view_menu, tearoff=0)
#view_menu.add_cascade(label='Themes',menu=theme_menu)

about_menu = Menu(top_bar, tearoff=0)
#about menu items
about_menu.add_command(label='About', compound='left')
about_menu.add_command(label='Licence', compound='left')

#Adding the menus to the menubar
top_bar.add_cascade(label='File', menu=file_menu) 
top_bar.add_cascade(label='Edit', menu=edit_menu) 
top_bar.add_cascade(label='View', menu=view_menu) 
top_bar.add_cascade(label='About', menu=about_menu) 
root.config(menu=top_bar)

second_bar = Frame(root, height= 30, background='light grey')
second_bar.pack(expand='no', fill='x')

#label below uses grid geometry manager, instead of pack, so throws an error
#Label(root, text='This is the area, where I will build a text editor.').grid(row=1, column=0, sticky='e') #filler label, so the window isn't empty

#linecount bar
linecount_bar = Text(root, width=5, padx=2, takefocus=0, border=0, background='khaki', state='disabled', wrap='none')
linecount_bar.pack(side='left', fill='y')

#linecount functionality
def on_content_change(event=NONE):
    update_line_numbers()
    update_cursor_info_bar()

def update_line_numbers(event=NONE):
    line_numbers = get_line_numbers()
    linecount_bar.config(state='normal')
    linecount_bar.delete('1.0','end')
    linecount_bar.insert('1.0',line_numbers)
    linecount_bar.config(state='disabled')

def get_line_numbers():
    output=''
    if show_line_n.get():
        row, col = textbox_area.index("end").split('.')
        for i in range (1, int(row)):
            output += str(i)+ '\n'
    return output

#current line highlighting
def highlight_line(interval=100):
    textbox_area.tag_remove('active_line',1.0,'end')
    textbox_area.tag_add('active_line','insert linestart','insert lineend+1c')
    textbox_area.after(interval, toggle_highlight)

def undo_highlight():
    textbox_area.tag_remove('active_line', 1.0, 'end')

def toggle_highlight():
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()

#text box + scroll bar
textbox_area = Text(root, wrap='word',undo=1)
textbox_area.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(textbox_area)
textbox_area.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=textbox_area.yview)
scroll_bar.pack(side='right', fill='y')
textbox_area.bind('<Any-KeyPress>', on_content_change)
textbox_area.tag_configure('active_line', background='ivory2')

#cursor info bar at the bottom right
cursor_info_bar = Label(textbox_area, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

#keybinds
#NOTE: Cut, Copy, Paste have already been implemented by default in Tkinter text boxes. Redo has to be redone because of some weird Tkinter binding
textbox_area.bind('<Control-y>', redo) 
textbox_area.bind('<Control-Y>', redo)
textbox_area.bind('<Control-a>', select_all) 
textbox_area.bind('<Control-A>', select_all)
textbox_area.bind('<Control-F>', find_text)
textbox_area.bind('<Control-N>', new_file)
textbox_area.bind('<Control-O>', open_file)
textbox_area.bind('<Control-S>', save_file)
textbox_area.bind('<Control-Shift-S>', save_as)

#test
file_object = tkinter.filedialog.askopenfile(mode='r')

root.mainloop()