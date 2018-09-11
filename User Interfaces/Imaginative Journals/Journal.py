# Daniel Neamati
# 10 December 2017

import random
import time
from tkinter import *

def read_prompts(filename):
    '''This function reads a file that contains journal prompts and returns
    a list of those prompts.'''
    prompt_file = open(filename, 'r')
    prompts = list(prompt_file)
    prompt_file.close()
    return prompts

def move_prompts(filename_full, filename_empty):
    '''This function moves prompts from a full file (e.g. Finished Journals.txt)
    to an empty file (e.g. Journal Prompts.txt).'''
    full = open(filename_full, 'r')
    lines = full.readlines()
    full.close()
    
    empty = open(filename_empty, 'w')
    for line in lines:
        empty.write(line)
    empty.close()

def rand_prompt(prompts):
    '''This function will randomly select a prompt from a list of prompts.'''
    assert type(prompts) == list
    if prompts == []:
        move_prompts('Finished Journals.txt', 'Journal Prompts.txt')
        pass
    return prompts[random.randint(0, len(prompts) - 1)]

def random_color():
    '''This function generates a random 6 digit string corresponding with a
    hexidecimal number and returns it with a #.'''    
    colorstring = '#'
    for digit in range(6):
        value = random.choice('0123456789abcdef')
        colorstring += value
    return colorstring

def accept(filename_current, filename_dest, prompt):
    '''This function is run if the user accepts the prompt.'''
    global color
    T.config(background = '#99ff99')
    
    current = open(filename_current, 'r')
    lines = current.readlines()
    current.close()

    assert isinstance(lines, list)
    
    current = open(filename_current, 'w')
    for line in lines:
        if line != prompt:
            current.write(line)
    current.close()

    dest = open(filename_dest, 'a')
    dest.write(prompt + '\n')
    print('Written!')
    dest.close()

def skip():
    '''This function is run if the user skips the prompt.'''
    global color
    T.config(background = random_color())

    T.delete('1.0', END)
    main()

def delete(filename_current, prompt):
    '''This function is run if the user deletes the prompt.'''
    global color
    T.config(background = '#ff794d')

    # Same as Accept, except not printed to another file
    current = open(filename_current, 'r')
    lines = current.readlines()
    current.close()

    assert isinstance(lines, list)
    
    current = open(filename_current, 'w')
    for line in lines:
        if line != prompt:
            current.write(line)
    current.close()
    print('Deleted')

def key_handler(event):
    '''Quits program'''
    '''Handle key presses.'''
    # q matches quiting the program
    if event.keysym == 'q':
        quit()
    # c matches a color change
    elif event.keysym == 'c':
        T.config(background = random_color())
    # a matches accept
    elif event.keysym == 'a':
        accept('Journal Prompts.txt', 'Finished Journals.txt', prompt)
    # s matches skip
    elif event.keysym == 's':
        skip()
    # d matches delete
    elif event.keysym == 'd':
        delete('Journal Prompts.txt', prompt)

def main():
    '''This function will execute the program in which a journal prompt is
    chosen, displayed to the screen, and allows the user to accept
    the prompt.'''
    global prompt
    
    prompts_list = read_prompts('Journal Prompts.txt')
    prompt = rand_prompt(prompts_list)

    # display random prompt
    # To Terminal
    print('Prompt choosen: ', prompt)

    # To GUI
    T.insert(END, prompt)
    T.config(font=('Papyrus', 14, 'bold'))
    T.tag_configure('center', justify = 'center')
    T.tag_add('center', 1.0, 'end')

    # display accept, skip, delete
    T.insert(END, 'Accept' + ' ' * int(win_width / 20)
             + 'Skip' + ' ' * int(win_width / 20)
             + 'Delete')



# TKinter display
if __name__ == '__main__':
    root = Tk()
    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())
    win_width = int(screen_width / 3)
    win_height = int(screen_height / 3)

    root.geometry('{}x{}'.format(win_width, win_height))
    root.bind('<Key>', key_handler)
##    Entry(root, justify = 'center')

    prompt = ''
    
    T = Text(root, width = win_width,
             height = win_height,
             wrap = WORD,
             background = random_color(),
             borderwidth = 5,
             spacing1 = win_height / 5)
    T.pack()
    main()

    root.mainloop()
