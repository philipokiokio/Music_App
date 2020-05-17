import os
from tkinter import *
import tkinter.messagebox
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import filedialog
import time
import threading
from ttkthemes import themed_tk as tk
from tkinter import ttk



#root window contains the status bar
''' the root contains both leeft and right frame.
The right frame contains top,middle and bottom frame.
while the left frame contains the current playlist'''
root =tk.ThemedTk()
root.get_themes()
root.set_theme('black')
root.config(bg= 'grey')
mixer.init()  # intializing the mixer


root.title('Kio_studio')
root.iconbitmap(r'images/wave.ico')
# root.geometry('300x300')

# create the menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)
# create submenu
sub_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=sub_menu)

def browse_file():
    global filename_path
    filenames_path = filedialog.askopenfilenames()
    for i in filenames_path:
        filename_path= i
        add_to_playlist(filename_path)


sub_menu.add_command(label='Open', command=browse_file)
sub_menu.add_command(label='Exit', command=root.destroy)



status_bar = ttk.Label(root, text='Welcome to Kio\'s Studio', anchor=W, relief=SUNKEN, font=' Times 10')
status_bar.pack(side=BOTTOM, fill=X)


sub_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Help', menu=sub_menu)

def about_us():
    tkinter.messagebox.showinfo('About Us,This is an app built with python, that uses your music files on your local machine and plays them. You can visit the developers portfolio page for more info, philipcodes.pythonanywhere.com')


sub_menu.add_command(label='About_Us', command=about_us)





playlist=[]
# playlist contains the full path + the filename
# current_playlist- contains just the filename
# filepath contains where the file is and to be played





def add_to_playlist(filename):
    filename= os.path.basename(filename)
    index= 0
    current_playlist.insert(index, filename)
    playlist.insert(index,filename_path)
    index +=1

def delete_song():
    selected_song = current_playlist.curselection()

    selected_song = int(selected_song[0])
    current_playlist.delete(selected_song)
    playlist.pop(selected_song)



left_frame= Frame(root,background= 'grey')
left_frame.pack(side= LEFT, pady= 50)

current_playlist = Listbox(left_frame,background= 'grey')
current_playlist.pack()

add = ttk.Button(left_frame, text='Add', command= browse_file)
add.pack(side= LEFT)

del_but= ttk.Button(left_frame, text='Del', command= delete_song)
del_but.pack()



right_frame=Frame(root, background= 'grey')
right_frame.pack()

top_frame=Frame(right_frame,background= 'grey')
top_frame.pack(pady=30)






middle = Frame(right_frame,background= 'grey',relief=SUNKEN)
middle.pack(padx=30, pady=30)
current_time_label=ttk.Label(middle, text='Run Time- --:--', relief= GROOVE, font= 'Arial 10',background= 'grey')
current_time_label.grid(row=0, column= 0)

length_label = ttk.Label(middle, text='Total Length- --:--', relief= GROOVE, font= 'Arial 10',background= 'grey')
length_label.grid(row=0, column =2)
play_image = PhotoImage(file='images/interface (1).png')


def show_detail(play_song):
    file_data = os.path.splitext(play_song)


    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    min,sec = divmod(total_length, 60)
    # it divides total_lenght by 60 and it returns and the mins and sec the reminder to sec
    min = round(min)
    sec = round(sec)
    time_format = '{:02d}:{:02d}'.format(min, sec)
    length_label['text'] = 'Total Length' + '- ' + time_format
    t1= threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    #Mixer.music stops the music, it returns false when we press pause button
    run_time= 0
    while run_time<t and mixer.music.get_busy():
        if paused:
            continue #ignores all the codes if paused
        else:
            min,sec= divmod(run_time, 60)
            min= round(min)
            sec= round(sec)
            time_format= '{:02d}:{:02d}'.format(min,sec)
            current_time_label['text']= 'Current Time' + '- ' + time_format
            time.sleep(1)
            run_time +=1




paused = FALSE


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        paused = FALSE
    else:
        try:

            stop_music()
            time.sleep(1)
            selected_song= current_playlist.curselection()

            selected_song = int(selected_song[0])

            play_it= playlist[selected_song]

            mixer.music.load(play_it)
            mixer.music.play()
            status_bar['text'] = 'Playing' + ' ' + os.path.basename(play_it)
            show_detail(play_it)


        except:
            tkinter.messagebox.showerror('No File Selected or Mp4 file', 'No has been selected or app does not recognize the file')


play_btn = ttk.Button(middle, image=play_image, command=play_music)
play_btn.grid(row=1,column=0)

pause_icon = PhotoImage(file='images/player.png')


def pause():
    global paused
    paused = TRUE
    mixer.music.pause()



pause_btn = ttk.Button(middle, image=pause_icon, command=pause)
pause_btn.grid(row=1, column=1)

stop_image = PhotoImage(file='images/music (1).png')


def stop_music():
    mixer.music.stop()
    status_bar['text'] = 'Stopped playing' + ' ' + os.path.basename(filename_path)



stop_btn = ttk.Button(middle, image=stop_image, command=stop_music)
stop_btn.grid(row=1, column=2)




bottom_frame = Frame(right_frame,background= 'grey',relief=SUNKEN)
bottom_frame.pack()

rewind_i = PhotoImage(file='images/music.png')

# def next(filename):
#     global  index
#     index +=1
#     filename = os.path.basename(filename)
#     mixer.music.load(filename[index])
#     mixer.music.play()

# next= Button(middle, text= 'Next', command= next)
# next.grid(row=0, column=1)

def rewind():
    mixer.music.rewind()
    status_bar['text'] = 'Music rewinded' + ' ' + os.path.basename(filename_path)



rew_but = ttk.Button(bottom_frame, image=rewind_i, command=rewind)
rew_but.grid(row=0, column=0)



def vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=vol)
scale.set(50)  # used to set default value for music
mixer.music.set_volume(.5)
scale.grid(row=0, column=1, padx=30)



muted = FALSE

def mute_unmute():
    global muted
    if muted:
        # unmute the music
        mixer.music.set_volume(0.7)
        unmute_but.configure(image=unmute_p)
        scale.set(50)
        muted = FALSE

    else:  # mute the music
        mixer.music.set_volume(0)
        unmute_but.configure(image=mute_p)
        scale.set(0)
        muted = TRUE


mute_p = PhotoImage(file='images/multimedia.png')

unmute_p = PhotoImage(file='images/interface.png')

unmute_but = ttk.Button(bottom_frame, image=unmute_p, command=mute_unmute)
unmute_but.grid(row=0, column=2)



def on_closing():
    stop_music()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
