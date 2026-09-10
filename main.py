import tkinter
import math
from struct import pack
import time
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 30
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
tick_amount = 0
tick = "✔"
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
#Reset function is a command within the reset tkinter button, it accesses global variables to reset tick amount and reps whilst using .after_cancel to kill the timer variable and reset the clock to "00:00"
def reset():
    global timer, REPS, tick_amount
    if REPS != 0:
        window.after_cancel(timer)
        REPS = 0
        tick_amount = 0
        Tick_Label.config(text="")
        Timer_Label.config(text=f"Timer {REPS}", fg= "#457B9D")
        canvas.itemconfig(stopwatch_num, text= "00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- #
#Works with the tkinter start button to determine at which rep to run a certain time and to incrementally add ticks every 1 work session
def start_timer():
    global REPS
    global tick_amount
    global tick
    #Reps time Configuration
    work_sec = 60 * WORK_MIN
    s_break_sec = 60 * SHORT_BREAK_MIN
    l_break_sec = 60 * LONG_BREAK_MIN

#This conditional adds a tick every 1 work session (1 work session = 1 work/25mins and 1 break/5mins
    if REPS % 2 == 0 and REPS > 1:
        tick_amount += 1
        Tick_Label.config(text=f"{tick_amount * tick}")

# Every 8 sessions it commences a long break
    if REPS % 8 == 7:
        count_down(l_break_sec)
        REPS += 1
        Timer_Label.config(text=f"Break {REPS}", fg="#e7305b")

# Every 2 sessions there's a work session
    elif REPS % 2 == 0:
        count_down(work_sec)
        REPS += 1
        Timer_Label.config(text=f"Work {REPS}", fg="#9bdeac")

# Every other session there's a 5 min break, except for the long breaks
    elif REPS % 2 == 1:
        count_down(s_break_sec)
        REPS += 1
        Timer_Label.config(text=f"Break {REPS}", fg="#e2979c")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
#function that determines clocks countdown functionality
def count_down(starting_num):
        global timer
        count_min = math.floor(starting_num / 60) #controls the minute portion of the clock display
        count_sec = starting_num % 60 #Controls the seconds portion of the clock display

        if count_sec == 0:
            count_sec = "00" # Example of Dynamic Typing: a variable changing what type of value it holds.

        elif count_sec < 10: # Example of Dynamic Typing: a variable changing what type of value it holds.
            count_sec = f"0{count_sec}"

        if starting_num > 0: #Aslong as the number left for the timer is above 0 the the following will happen
            timer = window.after(1000, count_down, starting_num -1 ) #the time will go down by 1 second with a 1 second pause time inbetween each time decrease via the first paramter (1000 milliseconds)
            canvas.itemconfig(stopwatch_num ,text=f"{count_min}:{count_sec}") #as each second goes down .itemconfig will signify this via an assorted f string converting conventional numbers into timed number format 00:00

        if starting_num == 0: #As soon as the timer hits 0 start the next start_timer function immediately (w/o this user will have to manually press a button to start the next (REP)
            start_timer()


# ---------------------------- UI SETUP ------------------------------- #

#Configures the window in which the pomodoro timer will appear: Changes to screen title, window padding relative to widgets and window background colour
window = Tk()
window.title("Abbas Pomodoro App")
window.config(padx=20, pady= 20, bg='#E3E4E8') ## Adds 20px padding around the widgets inside the window

#Tkinter class photoimage which loads an image into a form Tkinter can use
photo = PhotoImage(file= "stopwatch.png")

#Creates a canvas within the window where we can design how our application appears and works
canvas = Canvas(width= 540, height=540, bg='#E3E4E8', highlightthickness= 0)
canvas.create_image(270, 270, image= photo)
stopwatch_num = canvas.create_text(
    270,
    270,
    text= "00:00",
    fill= "#3F3F47",
    font=(FONT_NAME, 32, "bold")
)
canvas.grid(column= 2, row= 2)


#Timer Label
Timer_Label = Label(text= f"Timer {REPS}", font= ("Acme", 30, "bold"), fg= "#457B9D", bg= '#E3E4E8')
Timer_Label.grid(column= 2, row=1)

#Tick Label
Tick_Label = Label(text= "", fg= "#457B9D", bg= '#E3E4E8')
Tick_Label.grid(column= 2, row= 4)

#Start Button
Start = Button(text="Start", padx= 1, pady= 0.5, command= start_timer)
Start.grid(column= 1, row= 3)


#Reset Button
Start = Button(text="Reset", padx= 1, pady= 0.5, command= reset)
Start.grid(column= 3, row= 3)

window.mainloop()