import threading
from tkinter import *
from CTU_Assistant import shothand, greeting, content
from Voice_Pytts3 import speak
from Voice_regi import listen

#define properties
#color of UI
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

#Font of UI
FONT = "Helvetica 13"
FONT_BOLD = "Helvetica 13 bold"

#text of state
ERROR_LABEL = "Không nhận diện được giọng nói. Vui lòng thử lại!"
PROCESSING_LABEL = "Đang lắng nghe yêu cầu ..."
NOT_ENTER = "Vui lòng không nhập câu lệnh trống!"
MORE_REQUEST = "Bạn cần tôi giúp thêm điều gì không?"


#on commands typing
def on_enter(event):
    sms = msg_box.get()
    if sms and not sms.isspace():
        responce = shothand(sms)
        # insert_msg(sms, "Bạn",responce)
        t1 = threading.Thread(target=insert_msg,args=(sms, "Bạn",responce,))
        t2 = threading.Thread(target=speak, args=(responce,))
        t1.start()
        t2.start()
    else:
        msg_box.delete(0,END)
        t3 = threading.Thread(target=show_state, args=(NOT_ENTER,"BOT",))
        t4 = threading.Thread(target=speak, args=(NOT_ENTER,))
        t3.start()
        t4.start()

#show error state
def show_state(sms,sender):
    chatbox.configure(state=NORMAL)
    chatbox.insert(END,f"{sender}: {sms}\n\n")
    chatbox.configure(state=DISABLED)

#show listen processing state
def show_processing():
    chatbox.configure(state=NORMAL)
    chatbox.insert(END, PROCESSING_LABEL + "\n\n")
    chatbox.configure(state=DISABLED)

#on click voice button
def on_voice():
    try:
        sms = listen()
        if sms:
            responce = shothand(sms)
            t3 = threading.Thread(target=insert_msg,args=(sms, "Bạn",responce,))
            t4 = threading.Thread(target=speak, args=(responce,))
            t3.start()
            t4.start()
        else:
            t1 = threading.Thread(target=show_state, args=(ERROR_LABEL,"BOT",))
            t2 = threading.Thread(target=speak, args=(ERROR_LABEL,))
            t1.start()
            t2.start()
    except RuntimeError:
        # messagebox.showerror("Lỗi!","Thao tác quá nhanh.")
        show_state("Thao tác quá nhanh!","BOT")

#merge function
def  merge_func():
    thread1 = threading.Thread(target=show_processing)
    thread2 = threading.Thread(target=on_voice)
    thread1.start()
    thread2.start()

#show help function
def show_Help():
    helpWindow = Toplevel(window)
    helpWindow.title('Hướng Dẫn Sử Dụng')
    helpWindow.resizable(0,0)
    helpWindow.configure(width=400, height=500)
    helpWindow.iconbitmap('Database/Images/bot.ico')
    
    with open("Database/Help.txt","r",encoding='UTF-8') as f:
        text = f.read()
    help_label = Text(helpWindow,width=70,padx=10,pady=10)
    help_label.grid()
    help_label.insert(END,text)
    help_label.configure(cursor='arrow',state=DISABLED)


#show about function
def show_About():
    aboutWindow = Toplevel(window)
    aboutWindow.title('Giới thiệu về ...')
    aboutWindow.resizable(0,0)
    aboutWindow.configure(width=400, height=300)
    aboutWindow.iconbitmap('Database/Images/bot.ico')

    with open("Database/About.txt","r",encoding='UTF-8') as f:
        text = f.read()
    about_button = Text(aboutWindow,width=62,padx=10,pady=10)
    about_button.grid()
    about_button.insert(END,text)
    about_button.configure(cursor='arrow',state=DISABLED)
    
# create window
window = Tk()
window.title("CTU Assistant")
window.resizable(0, 0)
window.configure(width=470, height=550, bg=BG_COLOR)
window.iconbitmap('Database/Images/bot.ico')

# header
header = Label(window, bg=BG_COLOR)
header.place(relheight=1,relwidth=1)

head_label = Label(
    header,
    text="Chào mừng đến với CTU Assistant",
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=FONT_BOLD,
    pady=10,
)
head_label.place(relwidth=0.74)

#help button
help_ico = PhotoImage(file="Database/Images/help-icon.png")
help_button = Button(header,width=25,
                    image=help_ico, borderwidth=0, command=show_Help)
help_button.place(relx=0.78, rely=0.01)

#about button
about_ico = PhotoImage(file="Database/Images/about_ico.png")
about_button = Button(header,width=25, image=about_ico, borderwidth=0, 
                    command=show_About)
about_button.place(relx=0.88, rely=0.01)

# line
line = Label(window, width=450, bg=BG_GRAY)
line.place(relwidth=1, rely=0.07, relheight=0.012)

# chatbox
chatbox = Text(window, width=20, height=2, bg=BG_COLOR, padx=5, pady=5, 
        fg=TEXT_COLOR, font= FONT)
chatbox.place(relheight=0.745, relwidth=1, rely=0.08)
chatbox.configure(cursor='arrow', state=DISABLED)

#scollbar
scollbal = Scrollbar(chatbox)
scollbal.place(relheight=1, relx=0.974)
scollbal.configure(command=chatbox.yview)


#bottom line
line_bottom = Label(window, width=450, bg=BG_GRAY)
line_bottom.place(relwidth=1, rely=0.825,relheight=0.012)

#bottom
bottom = Label(window, height=80, bg=BG_COLOR)
bottom.place(relwidth=1, rely=0.835)

#msgbox
msg_box = Entry(bottom, bg="#fff", fg="#333", font=FONT)
msg_box.insert(0,"Vui lòng nhập yêu cầu")
msg_box.configure(state=DISABLED)
msg_box.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
# msg_box.focus()
msg_box.bind("<Return>",on_enter)

#voice button
imgs = PhotoImage(file="Database/Images/button.png")
voice_button = Button(bottom, width=20, image=imgs, borderwidth=0, 
                    command=merge_func, activebackground="red")
voice_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

#place holder
def onclick(event):
    msg_box.configure(state=NORMAL)
    msg_box.delete(0, END)
    msg_box.unbind('<Button-1>',on_click_id)

on_click_id  = msg_box.bind('<Button-1>', onclick)

#show greeting
def greeting_first():
    sms = greeting(content)
    sms1 = f"BOT: {sms}\n\n"
    chatbox.configure(state=NORMAL)
    chatbox.insert(END, sms1)
    chatbox.configure(state=DISABLED)

greeting_first()


#insert to chatbox
def insert_msg(sms, sender, label):
    if not sms:
        return

    msg_box.delete(0,END)
    sms1 = f"{sender}: {sms}\n\n"
    chatbox.configure(state=NORMAL)
    chatbox.insert(END, sms1)
    chatbox.configure(state=DISABLED)
    
    msg_box.delete(0,END)
    sms2 = f"BOT: {label}\n\n"
    chatbox.configure(state=NORMAL)
    chatbox.insert(END, sms2)
    chatbox.configure(state=DISABLED) 


#start UI
window.mainloop()

