#last updates : 23/08/2022, 5pm
from textwrap import indent
from tkinter import Button,Frame,Label,StringVar,Toplevel
from tkinter import Entry,Tk,filedialog,messagebox,ttk
from tkinter import FLAT,SE,SOLID,SUNKEN,SW,CENTER,END,LEFT
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image
from winsound import MessageBeep,MB_ICONHAND,MB_OK
from os import startfile
from textmanipulation import *
from spreadsheetmanipulation import *
from audiovideomanipulation import *
from filemanipulation import *

class Design:
    def __init__(self, master):
        # root window inheriting
        self.designwindow = master
        # getting the screen height and width
        self.height = self.designwindow.winfo_screenheight()
        self.width = self.designwindow.winfo_screenwidth()
        #  width and height place x and y
        self.designwindow.geometry("%dx%d+%d+%d" % (self.width, self.height,0, 0 ))
        # specifying limitation
        if self.width < 720 and self.height < 1000:
            messagebox.showerror("Screen Resolution Problem",
                                 "Sorry for the inconvienence File can't be run on your system")
        else:
            self.designwindow.title("Digital File Manipulation")
            self.designwindow.configure(bg="black")
            # creating one frame in the root
            self.frame1 = Frame(self.designwindow, height=self.height,
                    width=self.width , bg="black")
            self.frame1.pack(side=LEFT)
            # displaying image in frame through label
            front_window_img = Image.open("./res/frontlogo.jpg")
            front_window_img =front_window_img.resize((self.width, self.height)) # two bracket for image sampling
            front_window_img = ImageTk.PhotoImage(front_window_img)
            label_img = Label(self.frame1, image=front_window_img)
            label_img.pack()
            # making these image do not get garbage until label destroy
            label_img.img = front_window_img
            label_img.config(image=label_img.img)

            text_manipulation_button = Button(self.designwindow, width=30,height=3, text="Text Manipulation",
                                  fg="white", bg="black", font=('arial', 12, 'bold'), borderwidth=8,
                                  command=self.text_manipulation,activebackground="black",activeforeground="white")
            text_manipulation_button .place(relx=0.75,rely=0.02)

            spreadsheet_manipulation_button = Button(self.designwindow, width=30, height=3, text="Spreadsheet Manipulation",
                                  fg="white", bg="black", font=('arial', 12, 'bold'), borderwidth=8,
                                  command=self.spreadsheet_manipulate,activebackground="black",activeforeground="white")
            spreadsheet_manipulation_button.place(relx=0.75,rely=0.22)

            video_audio__manipulation_button = Button(self.designwindow, width=30, height=3, text="Audio-Video Manipulation",
                                  fg="white", bg="black", font=('arial', 12, 'bold'), borderwidth=8,
                                  command=self.video_audio_manipulation,activebackground="black",activeforeground="white")
            video_audio__manipulation_button.place(relx=0.75, rely=0.42)

            file_manipulation_button = Button(self.designwindow, width=30, height=3, text="File Manipulation",
                                  fg="white", bg="black", font=('arial', 12, 'bold'), command=self.file_manipulate,
                                  borderwidth=8,activebackground="black",activeforeground="white")
            file_manipulation_button .place(relx=0.75, rely=0.62)

            exit_button = Button(self.designwindow, width=30, height=3, text="EXIT", fg="white", bg="red", font=(
                'arial', 12, 'bold'), borderwidth=8, command=lambda: self.designwindow.destroy(),activebackground="black",activeforeground="white")
            exit_button.place(relx=0.75, rely=0.82)

    def text_manipulation(self):
        # creating child window using Toplevel
        self.module1 = Toplevel(self.designwindow)
        # passing child window along with main window to the class Window1
        self.mod1 = Window1(self.module1, self.designwindow)
        # making window disappear not even appear in taskbar
        self.designwindow.withdraw()

    def spreadsheet_manipulate(self):
        # creating child window using Toplevel
        self.module2 = Toplevel(self.designwindow)
        # passing child window along with main window to the class Window2
        self.mod2 = Window2(self.module2, self.designwindow)
        # making window disappear not even appear in taskbar
        self.designwindow.withdraw()

    def file_manipulate(self):
        # creating child window using Toplevel
        self.module4 = Toplevel(self.designwindow)
        # passing child window along with main window to the class Window1
        self.mod4 = Window4(self.module4, self.designwindow)
        # making window disappear not even appear in taskbar
        self.designwindow.withdraw()

    def video_audio_manipulation(self):
        # creating child window using Toplevel
        self.module3 = Toplevel(self.designwindow)
        # passing child window along with main window to the class Window1
        self.mod3 = Window3(self.module3, self.designwindow)
        # making window disappear not even appear in taskbar
        self.designwindow.withdraw()

#Text Manipulation

class Window1:
    def __init__(self, master, mainwindow):

        #***********************design of first Window********************
        self.view_file1=""
        self.view_file2=""
        self.view_file3=""

        self.var = StringVar()
        # Top level property
        self.first_window = master
        self.first_window.title("Text Manipulation")

        self.design_window = mainwindow
        self.window1_height = self.design_window.winfo_screenheight()
        self.window1_width = self.design_window.winfo_screenwidth()
        self.window1_img = Image.open("./res/topleveltextmanipulation.jpg")
        self.window1_img = self.window1_img.resize((self.window1_width, self.window1_height))
        self.window1_img = ImageTk.PhotoImage(self.window1_img)
        label = Label(self.first_window, image=self.window1_img)
        label.pack()

        self.first_window.protocol("WM_DELETE_WINDOW",self.on_exit)
        # making not to garbage
        self.window1_img.img =self.window1_img
        label.config(image=self.window1_img.img)
         # Creating Buttons in window
        extracting_text_from_img_btn1 = Button(self.first_window, text="Extracting Text from Image", width=30,
                                                    height=3, font=('arial', 12, 'bold'), command=lambda: self.upload_extracting_text_from_image(),
                                                    bg='#FF005E', fg="white",borderwidth=8)
        extracting_text_from_img_btn1.place(relx=0.015,rely=0.2)
        extracting_text_from_region_of_interest_btn2 = Button(
            self.first_window, text="Extracting Text from Region of Interest", width=30, height=3,
            font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.upload_extracting_text_from_region_of_interest(), borderwidth=8)
        extracting_text_from_region_of_interest_btn2.place(relx=0.015,rely=0.4)
        highlighting_text_btn3 = Button(
            self.first_window, text="Highlighting Text ", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.upload_highlighting_text(), borderwidth=8)
        highlighting_text_btn3.place(relx=0.015,rely=0.6)
        exit_btn4 = Button(self.first_window, text="Exit", width=30, height=3,
                                command=self.exit_window, font=('arial', 12, 'bold'), bg='#0055FF', fg="white",
                                borderwidth=8)
        exit_btn4.place(relx=0.015,rely=0.8)
        self.window1_btn1_frame=Frame(self.first_window)
        self.window1_btn2_frame=Frame(self.first_window)
        self.window1_btn3_frame=Frame(self.first_window)

    def exit_window(self):
        self.first_window.destroy()
        self.design_window.deiconify()

    def on_exit(self):
        self.first_window.destroy()
        self.design_window.deiconify()

# first button extracting text from image
    # ***************Button1*******************
    def upload_extracting_text_from_image(self):
        self.window1_btn2_frame.destroy()
        self.window1_btn3_frame.destroy()
        self.window1_btn1_frame=Frame(self.first_window,width=400, height=400,bg="purple")
        self.window1_btn1_frame.place(relx=0.4, rely=0.2)
        self.window1_btn1_frame.config(relief=FLAT)
        # Image for button
        self.window1_btn1_img= Image.open("./res/file.png")
        self.window1_btn1_img = self.window1_btn1_img.resize((150, 120))
        self.window1_btn1_img = ImageTk.PhotoImage(self.window1_btn1_img)
        # upload button
        button1 = Button(self.window1_btn1_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window1_btn1_img, command=lambda: self.extracting_text_from_image(), bg="black")
        button1.place(relx=0.5,rely=0.2,anchor="center")
        self.window1_btn1_img.img = self.window1_btn1_img
        button1.config(image=self.window1_btn1_img.img)
        # label for upload
        label1=Label(self.window1_btn1_frame, text="Drop file here", font=('arial black', 12, 'bold'), fg="black", width=15, height=1,bg="purple")
        label1.place(relx=0.3,rely=0.4)
        # instruction button
        button2 = Button(self.window1_btn1_frame, text="How to use", width=10, height=2, fg="white", font=('arial black', 12, 'bold'), bg="black", command=lambda: self.text_extract_instruct())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        #view Nutton
        view_button1 = Button(self.window1_btn1_frame, text="view", width=10, height=2, font=('arial black', 12, 'bold'),
                             bg="black", fg="white", activebackground="black", activeforeground="white",
                             command=lambda: self.view_text_file())
        view_button1.place(relx=0.01, rely=0.82)

    def text_extract_instruct(self):
        width=(self.window1_width/2)-100
        height=(self.window1_height/2)-150
        font=("Comic Sans MS",20,"bold")
        msg="Upload the clear image as input and save the file in desired location application retrive the text associated with the image\n max file size is 5MB"
        msg_window=Toplevel(self.first_window)
        msg_window.geometry("%dx%d+%d+%d" %(500,300,width,height))
        msg_window.resizable(0,0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label=Label(msg_window,text=msg,font=font,wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def extracting_text_from_image(self):
        try:
            # important else nothing displays
            self.first_window.grab_set()
            image_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png"), ("webp", "*.webp"),("svg","*.svg"),("raw","*.raw"),("xcf","*.xcf"),("jpx","*.jpx"),
                ("tiff","*.tiff"),("cr2","*.cr2"),("bmp","*.bmp"),("jxr","*.jxr"),("psd","*.psd"),("ico","*.ico"),("heic","*.heic"),("dcm","*.dcm")),parent=self.first_window)
            if image_file:
                saving_file = asksaveasfile(initialfile='Untitled.txt', defaultextension=".txt",
                                            filetypes=[("txt", "*.txt")],parent=self.first_window)
                if saving_file:
                    saving_file.close()
                    progressbar = ttk.Progressbar(self.first_window, length=400, mode="indeterminate")
                    progressbar.place_forget()
                    location = saving_file.name
                    progressbar.place(relx=0.4,rely=0.7)
                    progressbar.start()
                    output = image_to_text(image_file, location)
                    #self.progress_bar.stop()
                    if output["output"] != "":
                        progressbar.stop()
                        progressbar.destroy()
                        #success sound
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.first_window) #path of saved file is output_file
                        self.view_file1=output["output_file"]
                    elif output["error"] != "":
                        #failed sound
                        MessageBeep(type=MB_ICONHAND)
                        progressbar.stop()
                        progressbar.destroy()
                        messagebox.showerror("info",output["error"],parent=self.first_window)
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.first_window)
            else:
                messagebox.askokcancel("warning", "please select the image file for converting",parent=self.first_window)
        except Exception as e:
            messagebox.showerror("error", e)
    def view_text_file(self):
            if self.view_file1!="":
                startfile(self.view_file1)
                self.view_file1=""
            else:
                messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.first_window)

    # 2nd buttonExtracting Text from region of interest
    # *************************Button2***********************
    def upload_extracting_text_from_region_of_interest(self):
        self.window1_btn1_frame.destroy()
        self.window1_btn3_frame.destroy()
        self.window1_btn2_frame =Frame(self.first_window,width=400, height=400,bg="purple")
        self.window1_btn2_frame.place(relx=0.4, rely=0.2)
        self.window1_btn2_frame.config(relief=SOLID)
        # Image for button
        self.window1_btn2_img = Image.open("./res/file.png")
        self.window1_btn2_img = self.window1_btn2_img.resize((150, 120))
        self.window1_btn2_img = ImageTk.PhotoImage(self.window1_btn2_img)
        # upload button
        button1 = Button(self.window1_btn2_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window1_btn2_img, command=lambda: self.extracting_text_from_region_of_interest(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window1_btn2_img.img = self.window1_btn2_img
        button1.config(image=self.window1_btn2_img.img)
        # label for upload
        label1 = Label(self.window1_btn2_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window1_btn2_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_region_of_interest())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button2 = Button(self.window1_btn2_frame, text="view", width=10, height=2,
                                   font=('arial black', 12, 'bold'), bg="black", fg="white",
                                   activebackground="black", activeforeground="white",
                                   command=lambda: self.region_text_file())
        view_button2.place(relx=0.01, rely=0.82)

    def instruction_region_of_interest(self):
        width=(self.window1_width/2)-100
        height=(self.window1_height/2)-150
        font=("Comic Sans MS",20,"bold")
        msg="upload the proper image and save the file in desired location then application pops up the image to select the region of interest" \
            "On  selecting the region  pressing 'Enter' key two times will save the file as png and 'c' button to cancel the selection\n max file size is 5MB "\

        msg_window=Toplevel(self.first_window)
        msg_window.geometry("%dx%d+%d+%d" %(500,400,width,height))
        msg_window.resizable(0,0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label=Label(msg_window,text=msg,font=font,wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def extracting_text_from_region_of_interest(self):
        try:
            # important else nothing displays
            self.first_window.grab_set()
            image_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png"), ("webp", "*.webp"),("svg","*.svg"),("raw","*.raw"),("xcf","*.xcf"),("jpx","*.jpx"),
                ("tiff","*.tiff"),("cr2","*.cr2"),("bmp","*.bmp"),("jxr","*.jxr"),("psd","*.psd"),("ico","*.ico"),("heic","*.heic"),("dcm","*.dcm")),parent=self.first_window)
            if image_file:
                saving_file = asksaveasfile(initialfile='Untitled.txt',
                                            defaultextension=".txt", filetypes=[("txt", "*.txt")],parent=self.first_window)
                if saving_file:
                    saving_file.close()
                    location= saving_file.name
                    output = text_from_region_of_interest(image_file, location)
                    progressbar = ttk.Progressbar(self.first_window, length=400, mode="indeterminate")
                    progressbar.place(relx=0.4, rely=0.78)
                    progressbar.start()
                    if output["output"] != "":
                        progressbar.stop()
                        progressbar.destroy()
                        #success sound
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.first_window)
                        self.view_file2=output["output_file"]
                    elif output["error"] != "":
                        progressbar.stop()
                        progressbar.destroy()
                        #failed sound
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning", output["error"],parent=self.first_window)
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.first_window)
            else:
                messagebox.askokcancel("warning", "please select the image file for converting",parent=self.first_window)
        except Exception as e:
            messagebox.showerror("error", e)
    def region_text_file(self):
        if self.view_file2!="":
                startfile(self.view_file2)
                self.view_file2 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.first_window)

    # 3rd button Highlighting text
    #***********************Button3**************************
    def upload_highlighting_text(self):
        self.window1_btn1_frame.destroy()
        self.window1_btn2_frame.destroy()
        self.window1_btn3_frame=Frame(self.first_window,width=500, height=500, bg="purple")
        self.window1_btn3_frame.place(relx=0.4, rely=0.2)
        self.window1_btn3_frame.config(relief=SUNKEN)
        # Image for button
        self.window1_btn3_img = Image.open("./res/file.png")
        self.window1_btn3_img = self.window1_btn3_img.resize((150, 120))
        self.window1_btn3_img = ImageTk.PhotoImage(self.window1_btn3_img)
        # upload button
        button1 = Button(self.window1_btn3_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window1_btn3_img, command=lambda: self.highlighting_text(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window1_btn3_img.img = self.window1_btn3_img
        button1.config(image=self.window1_btn3_img.img)
        # label for upload
        label1 = Label(self.window1_btn3_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.35, rely=0.35)
        # instruction button
        button2 = Button(self.window1_btn3_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_for_highlight())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        self.view_button3 = Button(self.window1_btn3_frame, text="View", width=10, height=2,
                              font=('arial black', 12, 'bold'), bg="black", fg="white",
                              activebackground="black", activeforeground="white",
                              command=lambda: self.view_highlight_file())
        self.view_button3.place(rely=0.98, relx=0.01, x=0, y=0, anchor=SW)

    def instruction_for_highlight(self):
        width=(self.window1_width/2)-100
        height=(self.window1_height/2)-150
        font=("Comic Sans MS",20,"bold")
        msg="Upload the image and save the file then application ask for the word to search if it's their then pop ups the image and save in the desired location as png file\n max file size is 5MB "
        msg_window=Toplevel(self.first_window)
        msg_window.geometry("%dx%d+%d+%d" %(500,300,width,height))
        msg_window.resizable(0,0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label=Label(msg_window,text=msg,font=font,wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def highlighting_text(self):
        try:
            # important else nothing displays
            self.first_window.grab_set()
            self.input = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png"), ("webp", "*.webp"),("svg","*.svg"),("raw","*.raw"),("xcf","*.xcf"),("jpx","*.jpx"),
                ("tiff","*.tiff"),("cr2","*.cr2"),("bmp","*.bmp"),("jxr","*.jxr"),("psd","*.psd"),("ico","*.ico"),("heic","*.heic"),("dcm","*.dcm")),parent=self.first_window)
            if self.input:
                saving_file = asksaveasfile(initialfile='Untitled.png',
                                            defaultextension=".png", filetypes=([("png", "*.png")]),parent=self.first_window)
                if saving_file:
                    saving_file.close()
                    self.output = saving_file.name
                    self.search_word_label = Label(self.window1_btn3_frame, text="Enter the search word",
                                       font=("times new roman", 15, "bold"),bg="purple")
                    self.search_word_label.place(relx=0.1,rely=0.5)
                    self.search_word = Entry(self.window1_btn3_frame, width=20, textvariable=self.var,
                                             font=("times new roman", 15, "bold"))
                    self.search_word.place(relx=0.5,rely=0.5)
                    self.ok_button = Button(self.window1_btn3_frame, text="Ok",bg="black",fg="white", width=6,font=("times new roman", 15, "bold"),
                                       command=lambda: self.ok())
                    self.ok_button.place(relx=0.4,rely=0.6)
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.first_window)
            else:
                messagebox.askokcancel("warning", "please select the image file for converting",parent=self.first_window)
        except Exception as e:
            messagebox.showerror("error", e)

    def ok(self):
        try:
            self.word = self.search_word.get()
            if self.word == "":
                messagebox.showerror("Error", "please enter the word",parent=self.first_window)
            else:

                output = highlighting_text(self.input, self.output, self.word)

                if output["output"] != "":

                    #success sound
                    MessageBeep(type=MB_OK)
                    messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.first_window)
                    self.view_file3=output["output_file"]
                    self.search_word_label.destroy()
                    self.search_word.delete(0,END)
                    self.search_word.destroy()
                    self.ok_button.destroy()
                elif output["error"] != "":
                    MessageBeep(type=MB_ICONHAND)
                    messagebox.showerror("warning", output["error"],parent=self.first_window)
                    self.search_word_label.destroy()
                    self.search_word.delete(0,END)

                    self.search_word.destroy()
                    self.ok_button.destroy()
                    self.input=""
        except Exception as e:
            messagebox.showerror("error", e)

    def view_highlight_file(self):
        if self.view_file3!="":
                startfile(self.view_file3)
                self.view_file3 = ""
        else:
                messagebox.askokcancel("warning", "Please  Convert the file before viewing")



#Spread Sheet Manipulation
class Window2:
    def __init__(self, master, mainwindow):
        #************Design Window2*********************
        self.view_file4=""
        self.view_file5=""
        self.view_file6=""
        self.view_file7=""
        self.var1 = StringVar
        self.var2 = StringVar
        self.var3 = StringVar
        # Top level property
        self.second_window = master
        self.second_window.title("Spread Sheet Manipulation")
        self.design_window = mainwindow
        self.window2_height = self.design_window.winfo_screenheight()
        self.window2_width = self.design_window.winfo_screenwidth()
        self.window2_img = Image.open("./res/toplevelspreadsheetmanipulation.jpg")
        self.window2_img = self.window2_img.resize((self.window2_width, self.window2_height))
        self.window2_img = ImageTk.PhotoImage(self.window2_img)
        label = Label(self.second_window, image=self.window2_img)
        label.pack()
        # making not to garbage
        self.window2_img.img = self.window2_img
        label.config(image=self.window2_img.img)
        self.window2_btn1_frame = Frame(self.second_window)
        self.window2_btn2_frame = Frame(self.second_window)
        self.window2_btn3_frame = Frame(self.second_window)
        self.window2_btn4_frame = Frame(self.second_window)
        self.xls_to_txt = Button(
            self.second_window, text="Excel To Text", width=30, height=3,
            command=lambda: self.upload_xls_to_text_file(), font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            borderwidth=8)
        self.csv_to_text = Button(
            self.second_window, text="Csv To Text", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white", command=lambda: self.upload_csv_to_text(),
            borderwidth=8)
        self.xls_to_csv = Button(
            self.second_window, text="Excel To Csv ", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white", command=lambda: self.upload_xls_to_csv(),
            borderwidth=8)
        self.search_columns = Button(
            self.second_window, text="Search Columns", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white", command=lambda: self.upload_search_columns_in_xls(),
            borderwidth=8)
        self.exit_btn2 = Button(self.second_window, text="Exit", width=30, height=3,
                                command=self.exit_window, font=('arial', 12, 'bold'), bg='#0055FF', fg="white",
                                borderwidth=8)
        self.xls_to_txt.place(relx=0.02,rely=0.2)
        self.csv_to_text.place(relx=0.02,rely=0.35)
        self.xls_to_csv.place(relx=0.02,rely=0.5)
        self.search_columns.place(relx=0.02,rely=0.65)
        self.exit_btn2.place(relx=0.02,rely=0.8)
        self.second_window.protocol("WM_DELETE_WINDOW", self.on_exit)

    def exit_window(self):
        self.second_window.destroy()
        self.design_window.deiconify()

    def on_exit(self):
        self.second_window.destroy()
        self.design_window.deiconify()

    # first button code xls to text
    #*********************Button1*************************
    def upload_xls_to_text_file(self):
        self.window2_btn2_frame.destroy()
        self.window2_btn3_frame.destroy()
        self.window2_btn4_frame.destroy()
        self.window2_btn1_frame = Frame(self.second_window, width=400, height=400, bg="purple")
        self.window2_btn1_frame.place(relx=0.4, rely=0.2)
        self.window2_btn1_frame.config(relief=SUNKEN)
        # Image for button
        self.window2_btn1_img = Image.open("./res/file.png")
        self.window2_btn1_img = self.window2_btn1_img.resize((150, 120))
        self.window2_btn1_img = ImageTk.PhotoImage(self.window2_btn1_img)
        # upload button
        button1 = Button(self.window2_btn1_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window2_btn1_img,
                         command=lambda: self.xls_to_text_file(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window2_btn1_img.img = self.window2_btn1_img
        button1.config(image=self.window2_btn1_img.img)
        # label for upload
        label1 = Label(self.window2_btn1_frame, text="Drop file here", font=('arial black', 12, 'bold'),bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window2_btn1_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_xls_to_text())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button4 = Button(self.window2_btn1_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_xls_to_text_file())
        view_button4.place(relx=0.01, rely=0.82)

    def instruction_xls_to_text(self):
        width = (self.window2_width / 2) - 100
        height = (self.window2_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the xls or xlsx file application will convert the uploaded file into text file\n max file size is 10MB"
        msg_window = Toplevel(self.second_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def xls_to_text_file(self):
        try:
            # important else nothing displays
            self.second_window.grab_set()
            xls_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("xlsx file", "*.xlsx"), ("xls file", "*.xls")),parent=self.second_window)
            if xls_file:
                textfile = asksaveasfile(initialfile='Untitled.txt',
                                      defaultextension=".txt", filetypes=[("txt file", "*.txt")],parent=self.second_window)
                if textfile:
                    textfile.close()
                    # write the code

                    output_file = textfile.name

                    output = xls_to_text(xls_file, output_file)
                    if output["output"] != "":
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.second_window)
                        self.view_file4 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning",output["error"],parent=self.second_window)
                else:
                    messagebox.showerror("warning", "Please save the file",parent=self.second_window)
            else:
                messagebox.showerror("error!", "please select the xls file",parent=self.second_window)
        except Exception as e:
            messagebox.showerror("error", e)

    def view_xls_to_text_file(self):
        if self.view_file4 != "":
            startfile(self.view_file4)
            self.view_file4 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.second_window)
  
        # 2nd button csv to text
  #*******************Button2*************
    def upload_csv_to_text(self):
        self.window2_btn1_frame.destroy()
        self.window2_btn3_frame.destroy()
        self.window2_btn4_frame.destroy()
        self.window2_btn2_frame = Frame(self.second_window, width=400, height=400, bg="purple")
        self.window2_btn2_frame.place(relx=0.4, rely=0.2)
        self.window2_btn2_frame.config(relief=SUNKEN)
        # Image for button
        self.window2_btn2_img = Image.open("./res/file.png")
        self.window2_btn2_img = self.window2_btn2_img.resize((150, 120))
        self.window2_btn2_img = ImageTk.PhotoImage(self.window2_btn2_img)
        # upload button
        button1 = Button(self.window2_btn2_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window2_btn2_img,
                         command=lambda: self.csv_text(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window2_btn2_img.img = self.window2_btn2_img
        button1.config(image=self.window2_btn2_img.img)
        # label for upload
        label1 = Label(self.window2_btn2_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window2_btn2_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_csv_to_text())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button4 = Button(self.window2_btn2_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_csv_to_text())
        view_button4.place(relx=0.01, rely=0.82)

    def instruction_csv_to_text(self):
        width = (self.window2_width / 2) - 100
        height = (self.window2_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "Upload the csv file then application convert the uploaded file into text file\n max file size is 10MB"
        msg_window = Toplevel(self.second_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def csv_text(self):
            try:
                # important else nothing displays
                self.second_window.grab_set()
                csv_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                    ("All","*.*"),("csv file", "*.csv"), ("csv file", "*.csv")),parent=self.second_window)
                if csv_file:
                    text_file = asksaveasfile(initialfile='Untitled.txt',
                                              defaultextension=".txt", filetypes=[("text file", "*.txt")],parent=self.second_window)
                    if text_file:
                        text_file.close()
                        # write the code
                        output_file = text_file.name
                        output = csv_to_text(csv_file, output_file)
                        if output["output"] != "":
                            MessageBeep(type=MB_OK)
                            messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.second_window)
                            self.view_file5 = output["output_file"]
                        elif output["error"] != "":
                            MessageBeep(type=MB_ICONHAND)
                            messagebox.showerror("warning", output["error"],parent=self.second_window)
                    else:
                        messagebox.showerror("error!", "please save the  file",parent=self.second_window)
                else:
                    messagebox.showerror("error!", "please select the csv file",parent=self.second_window)
            except Exception as e:
                messagebox.showerror("error", e)

    def view_csv_to_text(self):
        if self.view_file5 != "":
            startfile(self.view_file5)
            self.view_file5= ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.second_window)

    # 3rd button code xls to csv
    #*************************Button3*********************
    def upload_xls_to_csv(self):
        self.window2_btn1_frame.destroy()
        self.window2_btn2_frame.destroy()
        self.window2_btn4_frame.destroy()
        self.window2_btn3_frame = Frame(self.second_window, width=450, height=400, bg="purple")
        self.window2_btn3_frame.place(relx=0.4, rely=0.2)
        self.window2_btn3_frame.config(relief=SUNKEN)
        # Image for button
        self.window2_btn3_img = Image.open("./res/file.png")
        self.window2_btn3_img = self.window2_btn3_img.resize((150, 120))
        self.window2_btn3_img = ImageTk.PhotoImage(self.window2_btn3_img)
        # upload button
        button1 = Button(self.window2_btn3_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window2_btn3_img,
                         command=lambda: self.xls_csv(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window2_btn3_img.img = self.window2_btn3_img
        button1.config(image=self.window2_btn3_img.img)
        # label for upload
        label1 = Label(self.window2_btn3_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window2_btn3_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_xls_csv())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button6 = Button(self.window2_btn3_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_xls_to_csv())
        view_button6.place(relx=0.01, rely=0.82)


    def instruction_xls_csv(self):
        width = (self.window2_width / 2) - 100
        height = (self.window2_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the xls file and save the file\n where you want to save after that application \nwill ask for sheename which is in your selected xls file then it will be converted into csv file\n max file size is 10MB "
        msg_window = Toplevel(self.second_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def xls_csv(self):
        try:
            # important else nothing displays
            self.second_window.grab_set()
            self.xls_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("xlsx file", "*.xlsx"), ("xls file", "*.xls")),parent=self.second_window)
            if self.xls_file:
                self.csv_file= asksaveasfile(initialfile='Untitled.csv',
                                               defaultextension=".csv", filetypes=[("csv file", "*.csv")],parent=self.second_window)
                
                if self.csv_file:
                    self.csv_file.close()
                    # write the code
                    self.sheetname_label = Label(self.window2_btn3_frame, text="Enter the sheetname",bg="purple",font=("times new roman", 15, "bold"))
                    self.sheetname_label.place(relx=0,rely=0.5)
                    self.sheetname3 = Entry(self.window2_btn3_frame, width=25, textvariable=self.var3)
                    self.sheetname3.place(relx=0.5,rely=0.51)
                    self.sheetname3.focus()
                    self.submit3_button = Button(self.window2_btn3_frame, text="submit", bg="black", fg="white",
                                            command=lambda: self.submit_btn3(), width=10, height=2)
                    self.submit3_button.place(relx=0.3,rely=0.6)
                else:
                    messagebox.showerror("error!", "please save the csv file",parent=self.second_window)
            else:
                messagebox.showerror("error!", "please select the xls file",parent=self.second_window)
        except Exception as e:
            messagebox.showerror("error", e)

    def submit_btn3(self):
        try:
            sheetname = self.sheetname3.get()
            output_file = self.csv_file.name
            if sheetname == "":
                messagebox.showerror("Entry invalid", "please Provide the sheetname",parent=self.second_window)
            else:
                output = xls_to_csv(self.xls_file, output_file, sheetname)
                if output["output"] != "":
                    MessageBeep(type=MB_OK)
                    messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.second_window)
                    self.sheetname_label.destroy()
                    self.sheetname3.delete(0, END)
                    self.sheetname3.destroy()
                    self.submit3_button.destroy()
                    self.view_file6 = output["output_file"]

                elif output["error"] != "":
                    MessageBeep(type=MB_ICONHAND)
                    messagebox.showerror("warning", output["error"],parent=self.second_window)
                    self.sheetname_label.destroy()
                    self.sheetname3.delete(0, END)
                    self.sheetname3.destroy()
                    self.submit3_button.destroy()
        except Exception as e:
            messagebox.showerror("error", e,parent=self.second_window)

    def view_xls_to_csv(self):
        if self.view_file6 != "":
            startfile(self.view_file6)
            self.view_file6 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.second_window)



    # *******************Button4*********************
    def upload_search_columns_in_xls(self):
        self.window2_btn1_frame.destroy()
        self.window2_btn2_frame.destroy()
        self.window2_btn3_frame.destroy()
        self.window2_btn4_frame = Frame(self.second_window, width=450, height=400, bg="purple")
        self.window2_btn4_frame.place(relx=0.4, rely=0.2)
        self.window2_btn4_frame.config(relief=SUNKEN)
        # Image for button
        self.window2_btn4_img = Image.open("./res/file.png")
        self.window2_btn4_img = self.window2_btn4_img.resize((150, 120))
        self.window2_btn4_img = ImageTk.PhotoImage(self.window2_btn4_img)
        # upload button
        button1 = Button(self.window2_btn4_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window2_btn4_img,
                         command=lambda: self.search_columns_in_xls(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window2_btn4_img.img = self.window2_btn4_img
        button1.config(image=self.window2_btn4_img.img)
        # label for upload
        label1 = Label(self.window2_btn4_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window2_btn4_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_search_column())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button7= Button(self.window2_btn4_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_columns())
        view_button7.place(relx=0.01, rely=0.82)
        self.clear_button3 = Button(self.window2_btn4_frame, text="Clear", width=10, height=2,
                              font=('arial black', 12, 'bold'), bg="black", fg="white",
                              activebackground="black", activeforeground="white",
                              command=lambda: self.clear_columns_data())
        self.clear_button3.place_forget()

    def instruction_search_column(self):
        width = (self.window2_width / 2) - 100
        height = (self.window2_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the xls file and save the text file\n where you want to save after that application \nwill ask for sheetname and columname you want to\n retrive from the xls file\n max file size is 10MB"
        msg_window = Toplevel(self.second_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def search_columns_in_xls(self):
        try:
            # important else nothing displays
            self.second_window.grab_set()
            self.xls_file4 = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("xlsx file", "*.xlsx"), ("xls file", "*.xls")),parent=self.second_window)
            if self.xls_file4:
                self.textfile = asksaveasfile(initialfile='Untitled.txt',
                                              defaultextension=".txt", filetypes=[("txt file", "*.txt")],parent=self.second_window)
                if self.textfile:
                    self.textfile.close()
                    self.label_sheetname = Label(self.window2_btn4_frame, text="Enter the sheet name",bg="purple")
                    self.label_sheetname.place(relx=0.2,rely=0.5)
                    self.sheetname = Entry(self.window2_btn4_frame, textvariable=self.var1)
                    self.sheetname.place(relx=0.5,rely=0.5)
                    self.label_column = Label(self.window2_btn4_frame, text="Enter the column name",bg="purple")
                    self.label_column.place(relx=0.2,rely=0.6)
                    self.columnname = Entry(self.window2_btn4_frame, textvariable=self.var2)
                    self.columnname.place(relx=0.5,rely=0.6)
                    self.ok_button_btn4 = Button(self.window2_btn4_frame, width=20, height=2,
                                       command=lambda: self.submit(), text="Submit",bg="black",fg="white")
                    self.ok_button_btn4.place(relx=0.3,rely=0.7)
                else:
                    messagebox.showerror("warning", "Please save the file",parent=self.second_window)
            else:
                messagebox.showerror("error!", "please select the xls file",parent=self.second_window)
        except Exception as e:
            print(e)

    def submit(self):
        sheetname = self.sheetname.get()
        columnname = self.columnname.get()
        outputfile = self.textfile.name
        if sheetname == "" or columnname == "":
            messagebox.showerror("file name error", "enter both column name and sheet name",parent=self.second_window)
        else:
            # write the code
            output = search_columns(self.xls_file4, outputfile, sheetname, columnname)
            if output["output"] != "":
                MessageBeep(type=MB_OK)
                messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.second_window)
                self.label_sheetname.destroy()
                self.sheetname.delete(0, END)
                self.columnname.delete(0, END)
                self.sheetname.destroy()
                self.label_column.destroy()
                self.columnname.destroy()
                self.ok_button_btn4.destroy()
                self.view_file7 = output["output_file"]
            elif output["error"] != "":
                MessageBeep(type=MB_ICONHAND)
                messagebox.showerror("warning",output["error"],parent=self.second_window)
                self.label_sheetname.destroy()
                self.sheetname.delete(0,END)
                self.columnname.delete(0,END)
                self.sheetname.destroy()
                self.label_column.destroy()
                self.columnname.destroy()
                self.ok_button_btn4.destroy()

    def view_columns(self):
        if self.view_file7 != "":
            startfile(self.view_file7)
            self.view_file7 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.second_window)



#Audio-Video Manipulation
class Window3:
    def __init__(self, master, mainwindow):
        self.view_file8=""
        self.view_file9=""
        self.view_file10=""

        self.start_min=StringVar()
        self.start_sec=StringVar()
        self.end_min=StringVar()
        self.end_sec=StringVar()
        self.third_window = master
        self.third_window.title("Audio-Video Manipulation")
        self.design_window = mainwindow
        self.window3_height = self.design_window.winfo_screenheight()
        self.window3_width = self.design_window.winfo_screenwidth()
        self.window3_img = Image.open("./res/toplevelaudiovideomanipulation.jpg")
        self.window3_img = self.window3_img.resize((self.window3_width, self.window3_height))
        self.window3_img = ImageTk.PhotoImage(self.window3_img)
        label = Label(self.third_window, image=self.window3_img)
        label.pack()
        # making not to garbage
        self.window3_img.img = self.window3_img
        label.config(image=self.window3_img.img)

        # Creating Buttons in btn_frame
        self.text_to_audio_btn1 = Button(self.third_window, text="Text To Audio", width=30,
                                             height=3, font=(
                'arial', 12, 'bold'), command=lambda: self.text_upload_btn_for_audio(), bg='#FF005E', fg="white",
                                             borderwidth=8)
        self.audio_extract_from_video_btn2 = Button(
            self.third_window, text="Extracting Audio from Video", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.video_upload_btn_for_audio(), borderwidth=8)
        self.trim_audio_btn3 = Button(
            self.third_window, text="Trim Audio", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.audio_upload_for_trim_btn(), borderwidth=8)
        self.exit_btn4 = Button(self.third_window, text="Exit", width=30, height=3,
                                command=self.exit_window, font=('arial', 12, 'bold'), bg='#0055FF', fg="white",
                                borderwidth=8)
        self.text_to_audio_btn1.place(relx=0.02,rely=0.2)
        self.audio_extract_from_video_btn2.place(relx=0.02,rely=0.35)
        self.trim_audio_btn3.place(relx=0.02,rely=0.5)
        self.exit_btn4.place(relx=0.02,rely=0.65)
        self.window3_btn1_frame=Frame(self.third_window)
        self.window3_btn2_frame = Frame(self.third_window)
        self.window3_btn3_frame = Frame(self.third_window)
        self.third_window.protocol("WM_DELETE_WINDOW", self.on_exit)

    def exit_window(self):
        self.third_window.destroy()
        self.design_window.deiconify()


    def on_exit(self):
        self.third_window.destroy()
        self.design_window.deiconify()


    # first button code extracting text from video
    # need net
    # *************************************Button1**********************************************
    def text_upload_btn_for_audio(self):
        self.window3_btn2_frame.destroy()
        self.window3_btn3_frame.destroy()
        self.window3_btn1_frame = Frame(self.third_window, width=400, height=400, bg="purple")
        self.window3_btn1_frame.place(relx=0.4, rely=0.2)
        self.window3_btn1_frame.config(relief=SUNKEN)
        # Image for button
        self.window3_btn1_img = Image.open("./res/file.png")
        self.window3_btn1_img = self.window3_btn1_img.resize((150, 120))
        self.window3_btn1_img = ImageTk.PhotoImage(self.window3_btn1_img)
        # upload button
        button1 = Button(self.window3_btn1_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window3_btn1_img, command=lambda: self.upload_text_for_audio(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window3_btn1_img.img = self.window3_btn1_img
        button1.config(image=self.window3_btn1_img.img)
        # label for upload
        label1 = Label(self.window3_btn1_frame, text="Drop file here", font=('arial black', 12, 'bold'),bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window3_btn1_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_text_audio())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button8 = Button(self.window3_btn1_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_text_to_audio())
        view_button8.place(relx=0.01, rely=0.82)

    def instruction_text_audio(self):
        width = (self.window3_width / 2) - 100
        height = (self.window3_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the text file  and save the file\n where you want to save after that application \nwill convert the text to audio\n max file size is 1MB"
        msg_window = Toplevel(self.third_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def upload_text_for_audio(self):
        try:
            # important else nothing displays
            self.third_window.grab_set()
            text_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("text format", "*.txt"),("text format", "*.txt")),parent=self.third_window)
            if text_file:
                textfile = asksaveasfile(initialfile='Untitled.mp3',
                                         defaultextension=".mp3", filetypes=[("mp3","*.mp3"),("wav","*.wav"),("aiff","*.aiff"),("aac","*.aac"),
                                                                            ("ogg","*.ogg"),("wma","*.wma"),("flac","*.flac"),("alac","*.alac")],parent=self.third_window)
                
                if textfile:
                    textfile.close()

                    output_file = textfile.name
                    output = text_to_audio(text_file, output_file)
                    if output["output"] != "":

                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success","file is saved..  \nin "+ output['output_file'],parent=self.third_window)
                        self.view_file8 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning",output["error"],parent=self.third_window )
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.third_window)
            else:
                messagebox.askokcancel("warning", "please select the video file for converting",parent=self.third_window)

        except Exception as e:
            messagebox.showerror("error", e)
    def view_text_to_audio(self):
        if self.view_file8 != "":
            startfile(self.view_file8)
            self.view_file8= ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.third_window)
    # 2nd button video from audio
    #*************************************Button2********************************************
    def video_upload_btn_for_audio(self):

        self.window3_btn2_frame.destroy()
        self.window3_btn3_frame.destroy()
        self.window3_btn1_frame = Frame(self.third_window, width=400, height=400, bg="purple")
        self.window3_btn1_frame.place(relx=0.4, rely=0.2)
        self.window3_btn1_frame.config(relief=SUNKEN)

        # Image for button
        self.window3_btn1_img = Image.open("./res/file.png")
        self.window3_btn1_img = self.window3_btn1_img.resize((150, 120))
        self.window3_btn1_img = ImageTk.PhotoImage(self.window3_btn1_img)
        # upload button
        button1 = Button(self.window3_btn1_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window3_btn1_img, command=lambda: self.upload_video_for_audio(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window3_btn1_img.img = self.window3_btn1_img
        button1.config(image=self.window3_btn1_img.img)
        # label for upload
        label1 = Label(self.window3_btn1_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window3_btn1_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_video_audio())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button9 = Button(self.window3_btn1_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_video_to_audio())
        view_button9.place(relx=0.01, rely=0.82)

    def instruction_video_audio(self):
        width = (self.window3_width / 2) - 100
        height = (self.window3_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the video file and save the audio file\n where you want to save after that application \nwill retrive the audio  within the video file\n max file size is 100MB"
        msg_window = Toplevel(self.third_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def upload_video_for_audio(self):
        try:
            # important else nothing displays
            self.third_window.grab_set()
            video_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("mp4","*.mp4"),("mkv","*.mkv"),("mov","*.mov"),("avi","*.avi"),("mpeg","*.mpeg"),("webm","*.webm"),
		        ("wmv","*.wmv"),("flv","*.flv"),("ogg","*.ogg"),("3gp","*.3gp"),("avchd","*.avchd"),("m4v","*.m4v")),parent=self.third_window)
            if video_file:
                audio_file = asksaveasfile(initialfile='Untitled.wav',
                                           defaultextension=".wav", filetypes=[("wav","*.wav"),("mp3","*.mp3"),("aiff","*.aiff"),("aac","*.aac"),
                                                                            ("ogg","*.ogg"),("wma","*.wma"),("flac","*.flac"),("alac","*.alac")],parent=self.third_window)
                if audio_file:
                    audio_file.close()
                    output_file = audio_file.name
                    output = video_to_audio(video_file, output_file)
                    if output["output"] != "":
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.third_window)
                        self.view_file9 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning",output["error"],parent=self.third_window)
                else:
                    messagebox.askokcancel("warning", "please save the audio file for accessing content",parent=self.third_window)
            else:
                messagebox.askokcancel("warning", "please select the video file for converting",parent=self.third_window)
        except Exception as e:
            messagebox.showerror("error", e)
    
    def view_video_to_audio(self):
        if self.view_file9 != "":
            startfile(self.view_file9)
            self.view_file9 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.third_window)
    
    #**********************************************Button3********************************
    # 3rd button
    def audio_upload_for_trim_btn(self):
        # need net
        self.window3_btn2_frame.destroy()
        self.window3_btn1_frame.destroy()
        self.window3_btn3_frame = Frame(self.third_window, width=400, height=450, bg="purple")
        self.window3_btn3_frame.place(relx=0.4, rely=0.2)
        self.window3_btn3_frame.config(relief=SUNKEN)
        # Image for button
        self.window3_btn3_img = Image.open("./res/file.png")
        self.window3_btn3_img = self.window3_btn3_img.resize((150, 120))
        self.window3_btn3_img = ImageTk.PhotoImage(self.window3_btn3_img)
        # upload button
        button1 = Button(self.window3_btn3_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window3_btn3_img, command=lambda: self.upload_audio_to_trim(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window3_btn3_img.img = self.window3_btn3_img
        button1.config(image=self.window3_btn3_img.img)
        # label for upload
        label1 = Label(self.window3_btn3_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.3)
        # instruction button
        button2 = Button(self.window3_btn3_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_trim_audio())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button10 = Button(self.window3_btn3_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_trim_audio())
        view_button10.place(relx=0.01, rely=0.98,x=0,y=0,anchor=SW)

    def instruction_trim_audio(self):
        width = (self.window3_width / 2) - 100
        height = (self.window3_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the audio file and give start and end time to trim audio and save the file\n where you want to save after that application \nwill trim the audio\n max file size is 20MB"
        msg_window = Toplevel(self.third_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def upload_audio_to_trim(self):
        try:
            # important else nothing displays
            self.third_window.grab_set()
            self.trim_audio_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("wav","*.wav"),("mp3","*.mp3"),("ogg","*.ogg"),("flv","*.flv"),("raw","*.raw")),parent=self.third_window)
                                                                                                                            
            if self.trim_audio_file:
                self.trimmed_audio_save = asksaveasfile(initialfile='Untitled.wav',
                                          defaultextension=".wav", filetypes=[("wav","*.wav"),("mp3","*.mp3"),("ogg","*.ogg"),("flv","*.flv"),("raw","*.raw"),("aiff",".aiff"),("aac",".aac")],parent=self.third_window)
                if self.trimmed_audio_save:
                    self.trimmed_audio_save.close()


                    self.start_min_label=Label(self.window3_btn3_frame,text="Start min",bg="purple",font=("times new roman", 13, "bold"))

                    self.start_min_data= Entry(self.window3_btn3_frame, width=5, textvariable=self.start_min,
                                             font=("times new roman", 14, "bold"),justify='right')

                    self.start_sec_label = Label(self.window3_btn3_frame,text="Start Sec",bg="purple", font=("times new roman", 13, "bold"))

                    self.start_sec_data = Entry(self.window3_btn3_frame, width=5, textvariable=self.start_sec,
                                                font=("times new roman", 14, "bold"))

                    self.end_min_label = Label(self.window3_btn3_frame,text="End min",bg="purple", font=("times new roman", 13, "bold"))

                    self.end_min_data = Entry(self.window3_btn3_frame, width=5, textvariable=self.end_min,
                                                font=("times new roman", 14, "bold"),justify='right')

                    self.end_sec_label = Label(self.window3_btn3_frame,text="End sec",bg="purple", font=("times new roman", 13, "bold"))

                    self.end_sec_data = Entry(self.window3_btn3_frame, width=5, textvariable=self.end_sec,
                                                font=("times new roman", 14, "bold"))

                    self.start_min_label.place(relx=0.32,rely=0.35)
                    self.start_min_data.place(relx=0.34,rely=0.4)
                    self.start_sec_label.place(relx=0.52, rely=0.35)
                    self.start_sec_data.place(relx=0.54, rely=0.4)

                    self.end_min_label.place(relx=0.32, rely=0.45)
                    self.end_min_data.place(relx=0.34, rely=0.5)
                    self.end_sec_label.place(relx=0.52, rely=0.45)
                    self.end_sec_data.place(relx=0.54, rely=0.5)

                    self.submit_data=Button(self.window3_btn3_frame,text="submit",command=lambda:self.submit(),bg="black",fg="white",
                                        width=10, height=2,font=("arial black",12,"bold"))
                    self.submit_data.place(relx=0.35,rely=0.57)
                else:
                    messagebox.askokcancel("warning", "please save the audio file for accessing content",parent=self.third_window)
            else:
                messagebox.askokcancel("warning", "please select the audio file for converting",parent=self.third_window)
        except Exception as e:
            messagebox.showerror("error", e, parent=self.third_window)
    def submit(self):
        try:
            startmin=self.start_min_data.get()
            startsec=self.start_sec_data.get()
            endmin=self.end_min_data.get()
            endsec=self.end_sec_data.get()
            if(startmin=="" or startsec=="" or endmin=="" or endsec==""):
                messagebox.showerror("error","please enter start and end time",parent=self.third_window)
            else:
                startmin=int(startmin)
                startsec=int(startsec)
                endmin=int(endmin)
                endsec=int(endsec)
                output_file = self.trimmed_audio_save.name
                output = trim_audio(self.trim_audio_file, output_file,startmin,startsec,endmin,endsec)
                if output["output"] != "":
                    MessageBeep(type=MB_OK)
                    messagebox.showinfo("success", "file is saved in\n" + output['output_file'], parent=self.third_window)
                    self.view_file10 = output["output_file"]
                    self.start_min_label.destroy()
                    self.start_sec_data.delete(0,END)
                    self.end_sec_data.delete(0, END)
                    self.start_min_data.delete(0, END)
                    self.end_min_data.delete(0, END)
                    self.submit_data.destroy()
                    self.start_min_data.destroy()
                    self.start_sec_label.destroy()
                    self.start_sec_data.destroy()
                    self.end_min_label.destroy()
                    self.end_min_data.destroy()
                    self.end_sec_label.destroy()
                    self.end_sec_data.destroy()

                elif output["error"] != "":
                    MessageBeep(type=MB_ICONHAND)
                    messagebox.showerror("warning", output["error"], parent=self.third_window)

        except ValueError:
            messagebox.showerror("error","please enter only numbers for time", parent=self.third_window)
            self.start_min_data.delete(0,END)
            self.start_sec_data.delete(0,END)
            self.end_min_data.delete(0,END)
            self.end_sec_data.delete(0,END)
        except Exception as e:
            messagebox.showerror("error",e, parent=self.third_window)

    def view_trim_audio(self):
        if self.view_file10 != "":
            startfile(self.view_file10)
            self.view_file10 = ""
        else:
            messagebox.askokcancel("warning", "Please Convert the file before viewing",parent=self.third_window)

#file manipulation
class Window4:
    def __init__(self, master, mainwindow):
        self.view_file11=""
        self.view_file12=""
        self.view_file13=""
        self.view14_file14=""
        self.fourth_window = master
        self.fourth_window.title("File Manipulation")
        self.design_window = mainwindow
        self.window4_height = self.design_window.winfo_screenheight()
        self.window4_width = self.design_window.winfo_screenwidth()
        self.window4_img = Image.open("./res/toplevelfilemanipulation.jpg")
        self.window4_img = self.window4_img.resize((self.window4_width, self.window4_height))
        self.window4_img = ImageTk.PhotoImage(self.window4_img)
        label = Label(self.fourth_window, image=self.window4_img)
        label.pack()
        # making not to garbage
        self.window4_img.img = self.window4_img
        label.config(image=self.window4_img.img)

        # Creating Buttons in btn_frame
        self.pdf_to_text_btn = Button(self.fourth_window, text="Pdf To Text", width=30,
                                      height=3, font=(
                'arial', 12, 'bold'), command=lambda: self.upload_pdf_file(), bg='#FF005E', fg="white",
                                      borderwidth=8)
        self.doc_to_text_btn = Button(
            self.fourth_window, text="Docx To Text", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.upload_doc_file(), borderwidth=8)
        self.pdf_to_doc_btn = Button(
            self.fourth_window, text="Pdf To Docx", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.upload_pdf_file_2doc(), borderwidth=8)
        self.text_to_doc_btn = Button(
            self.fourth_window, text="Text To Docx", width=30, height=3, font=('arial', 12, 'bold'),
            bg='#FF005E', fg="white",
            command=lambda: self.upload_text_file_2doc(), borderwidth=8)
        self.exit_btn4 = Button(self.fourth_window, text="Exit", width=30, height=3,
                                command=self.exit_window, font=('arial', 12, 'bold'), bg='#0055FF', fg="white",
                                borderwidth=8)
        self.pdf_to_text_btn.place(relx=0.02, rely=0.2)
        self.doc_to_text_btn.place(relx=0.02, rely=0.35)
        self.pdf_to_doc_btn.place(relx=0.02, rely=0.5)
        self.text_to_doc_btn.place(relx=0.02, rely=0.65)
        self.exit_btn4.place(relx=0.02, rely=0.80)
        self.window4_btn1_frame = Frame(self.fourth_window)
        self.window4_btn2_frame = Frame(self.fourth_window)
        self.window4_btn3_frame = Frame(self.fourth_window)
        self.window4_btn4_frame = Frame(self.fourth_window)
        self.fourth_window.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        self.fourth_window.destroy()
        self.design_window.deiconify()

    def exit_window(self):
        self.fourth_window.destroy()
        self.design_window.deiconify()


    #*************************************Button1*************************************
    def upload_pdf_file(self):
        self.window4_btn2_frame.destroy()
        self.window4_btn3_frame.destroy()
        self.window4_btn4_frame.destroy()
        self.window4_btn1_frame = Frame(self.fourth_window, width=400, height=400,bg="purple")
        self.window4_btn1_frame.place(relx=0.4, rely=0.2)
        self.window4_btn1_frame.config(relief=SUNKEN)
        # Image for button
        self.window4_btn1_img = Image.open("./res/file.png")
        self.window4_btn1_img = self.window4_btn1_img.resize((150, 120))
        self.window4_btn1_img = ImageTk.PhotoImage(self.window4_btn1_img)
        # upload button
        button1 = Button(self.window4_btn1_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window4_btn1_img, command=lambda: self.pdf_to_text(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window4_btn1_img.img = self.window4_btn1_img
        button1.config(image=self.window4_btn1_img.img)
        # label for upload
        label1 = Label(self.window4_btn1_frame, text="Drop file here", font=('arial black', 12, 'bold'),bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window4_btn1_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_pdf_text())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button11= Button(self.window4_btn1_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_pdf_to_text())
        view_button11.place(relx=0.01, rely=0.82)

    def instruction_pdf_text(self):
        width = (self.window4_width / 2) - 100
        height = (self.window4_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the pdf file and save the file\n where you want to save after that application \nwill convert the pdf file into  text file\n max file size is 10MB"
        msg_window = Toplevel(self.fourth_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def pdf_to_text(self):
        try:
            # important else nothing displays
            self.fourth_window.grab_set()
            pdf_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("pdf file", "*.pdf"), ("pdf file", "*.pdf")),parent=self.fourth_window)
            if pdf_file:
                textfile = asksaveasfile(initialfile='Untitled.txt',
                                         defaultextension=".txt", filetypes=[("txt file", "*.txt")],parent=self.fourth_window)
                if textfile:
                    textfile.close()
                    output_file = textfile.name
                    output = pdf_to_text(pdf_file, output_file)
                    if output["output"] != "":
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success","file is saved..  \nin "+ output['output_file'],parent=self.fourth_window)
                        self.view_file11 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning", output["error"],parent=self.fourth_window)
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.fourth_window)
            else:
                messagebox.askokcancel("warning", "please select the pdf file for converting",parent=self.fourth_window)
        except Exception as e:
            messagebox.showerror("error", e)

    def view_pdf_to_text(self):
        if self.view_file11 != "":
            startfile(self.view_file11)
            self.view_file11= ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.fourth_window)

        # 2nd button video from audio
    #****************************************Button2********************************
    def upload_doc_file(self):
        self.window4_btn1_frame.destroy()
        self.window4_btn3_frame.destroy()
        self.window4_btn4_frame.destroy()
        self.window4_btn2_frame = Frame(self.fourth_window, width=400, height=400, bg="purple")
        self.window4_btn2_frame.place(relx=0.4, rely=0.2)
        self.window4_btn2_frame.config(relief=SUNKEN)
        # Image for button
        self.window4_btn2_img = Image.open("./res/file.png")
        self.window4_btn2_img = self.window4_btn2_img.resize((150, 120))
        self.window4_btn2_img = ImageTk.PhotoImage(self.window4_btn2_img)
        # upload button
        button1 = Button(self.window4_btn2_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window4_btn2_img, command=lambda: self.doc_to_text(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window4_btn2_img.img = self.window4_btn2_img
        button1.config(image=self.window4_btn2_img.img)
        # label for upload
        label1 = Label(self.window4_btn2_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window4_btn2_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_doc_text())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button12 = Button(self.window4_btn2_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_doc_to_text())
        view_button12.place(relx=0.01, rely=0.82)

    def instruction_doc_text(self):
        width = (self.window4_width / 2) - 100
        height = (self.window4_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the doc file and save the file\n where you want to save after that application \nwill convert the doc file into  text file\n max file size is 10MB"
        msg_window = Toplevel(self.fourth_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def doc_to_text(self):
        try:
            # important else nothing displays
            self.fourth_window.grab_set()
            doc_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("docx file", "*.docx"), ("doc file", "*.doc")),parent=self.fourth_window)
            if doc_file:
                text_file = asksaveasfile(initialfile='Untitled.txt',
                                          defaultextension=".txt", filetypes=[("text file", "*.txt")],parent=self.fourth_window)
                if text_file:
                    text_file.close()
                    output_file = text_file.name
                    output = doc_to_text(doc_file, output_file)
                    if output["output"] != "":
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success","file is saved..  \nin "+ output['output_file'],parent=self.fourth_window)
                        self.view_file12 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning", output["error"],parent=self.fourth_window)
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.fourth_window)
            else:
                messagebox.askokcancel("warning", "please select the doc file for converting",parent=self.fourth_window)
        except Exception as e:
            messagebox.showerror("error", e)

    def view_doc_to_text(self):
        if self.view_file12 != "":
            startfile(self.view_file12)
            self.view_file12 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.fourth_window)

    #*************************************Button3***************************
    def upload_pdf_file_2doc(self):
        self.window4_btn1_frame.destroy()
        self.window4_btn2_frame.destroy()
        self.window4_btn4_frame.destroy()
        self.window4_btn3_frame = Frame(self.fourth_window, width=400, height=400, bg="purple")
        self.window4_btn3_frame.place(relx=0.4, rely=0.2)
        self.window4_btn3_frame.config(relief=SUNKEN)
        # Image for button
        self.window4_btn3_img = Image.open("./res/file.png")
        self.window4_btn3_img = self.window4_btn3_img.resize((150, 120))
        self.window4_btn3_img = ImageTk.PhotoImage(self.window4_btn3_img)
        # upload button
        button1 = Button(self.window4_btn3_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window4_btn3_img, command=lambda: self.pdf_to_doc(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window4_btn3_img.img = self.window4_btn3_img
        button1.config(image=self.window4_btn3_img.img)
        # label for upload
        label1 = Label(self.window4_btn3_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window4_btn3_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_text_pdf())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button13 = Button(self.window4_btn3_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_pdf_to_doc())
        view_button13.place(relx=0.01, rely=0.82)
    
    def instruction_text_pdf(self):
        width = (self.window4_width / 2) - 100
        height = (self.window4_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the text file and save the file\n where you want to save after that application \nwill convert text file into pdf file\n max file size is 10MB"
        msg_window = Toplevel(self.fourth_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def pdf_to_doc(self):
        try:
            # error
            # important else nothing displays
            self.fourth_window.grab_set()
            text_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("pdf file", "*.pdf"), ("pdf file", "*.pdf")),parent=self.fourth_window)
            if text_file:
                pdf_file = asksaveasfile(initialfile='Untitled.docx',
                                         defaultextension=".docx", filetypes=[("docx format", "*.docx"),("doc format", "*.doc")],parent=self.fourth_window)
               
                if pdf_file:
                    pdf_file.close()
                    output_file = pdf_file.name
                    output = pdf_to_doc(text_file, output_file)
                    if output["output"] != "":
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.fourth_window)
                        self.view_file13 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)
                        messagebox.showerror("warning",output["error"],parent=self.fourth_window )
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.fourth_window)
            else:
                messagebox.askokcancel("warning", "please select the pdf file for converting",parent=self.fourth_window)
        except Exception as e:
            messagebox.showerror("error", e)

    def view_pdf_to_doc(self):
        if self.view_file13 != "":
            startfile(self.view_file13)
            self.view_file13 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.fourth_window)


    # 4th button
    def upload_text_file_2doc(self):
        self.window4_btn1_frame.destroy()
        self.window4_btn3_frame.destroy()
        self.window4_btn2_frame.destroy()
        self.window4_btn4_frame = Frame(self.fourth_window, width=400, height=400, bg="purple")
        self.window4_btn4_frame.place(relx=0.4, rely=0.2)
        self.window4_btn4_frame.config(relief=SUNKEN)
        # Image for button
        self.window4_btn4_img = Image.open("./res/file.png")
        self.window4_btn4_img = self.window4_btn4_img.resize((150, 120))
        self.window4_btn4_img = ImageTk.PhotoImage(self.window4_btn4_img)
        # upload button
        button1 = Button(self.window4_btn4_frame, text="Upload", width=150, height=120, fg="white", font=(
            'arial', 10, 'bold'), image=self.window4_btn4_img, command=lambda: self.text_to_doc(),
                         bg="black")
        button1.place(relx=0.5, rely=0.2, anchor="center")
        self.window4_btn4_img.img = self.window4_btn4_img
        button1.config(image=self.window4_btn4_img.img)
        # label for upload
        label1 = Label(self.window4_btn4_frame, text="Drop file here", font=('arial black', 12, 'bold'), bg="purple",
                       fg="black", width=15, height=1)
        label1.place(relx=0.3, rely=0.4)
        # instruction button
        button2 = Button(self.window4_btn4_frame, text="How to use", width=10, height=2, fg="white",
                         font=('arial black', 12, 'bold'), bg="black", command=lambda: self.instruction_text_doc())
        button2.place(rely=0.98, relx=0.98, x=0, y=0, anchor=SE)
        view_button14 = Button(self.window4_btn4_frame, text="view", width=10, height=2,
                             font=('arial black', 12, 'bold'), bg="black", fg="white",
                             activebackground="black", activeforeground="white",
                             command=lambda: self.view_text_to_doc())
        view_button14.place(relx=0.01, rely=0.82)

    def instruction_text_doc(self):
        width = (self.window4_width / 2) - 100
        height = (self.window4_height / 2) - 150
        font = ("Comic Sans MS", 20, "bold")
        msg = "upload the text file and save the doc file\n where you want to save after that application \nwill convert the given text into normal text file\n max file size is 10MB"
        msg_window = Toplevel(self.fourth_window)
        msg_window.geometry("%dx%d+%d+%d" % (500, 300, width, height))
        msg_window.resizable(0, 0)
        msg_window.focus_set()
        msg_window.iconbitmap("./res/hint.ico")
        msg_window.title("Instruction")
        msg_label = Label(msg_window, text=msg, font=font, wraplength=450)
        msg_label.place(relx=0, rely=0.1)
        msg_window.mainloop()

    def text_to_doc(self):
        try:
            # important else nothing displays
            self.fourth_window.grab_set()
            text_file = filedialog.askopenfilename(initialdir="c:\\", title="select a file", filetypes=(
                ("All","*.*"),("text file", "*.txt"), ("text file", "*.txt")),parent=self.fourth_window)
            if text_file:
                doc_file = asksaveasfile(initialfile='Untitled.docx',
                                         defaultextension=".docx", filetypes=[("doc format", "*.doc"),("docx format","*.docx")],parent=self.fourth_window)
                
                if doc_file:
                    doc_file.close()
                    output_file = doc_file.name
                    output = text_to_doc(text_file, output_file)
                    if output["output"] != "":
                        MessageBeep(type=MB_OK)
                        messagebox.showinfo("success", "file is saved..  \nin "+ output['output_file'],parent=self.fourth_window)
                        self.view_file14 = output["output_file"]
                    elif output["error"] != "":
                        MessageBeep(type=MB_ICONHAND)

                        messagebox.showerror("warning", output["error"], parent=self.fourth_window)
                else:
                    messagebox.askokcancel("warning", "please save the file for accessing content",parent=self.fourth_window)
            else:
                messagebox.askokcancel("warning", "please select the text file for converting",parent=self.fourth_window)
        except Exception as e:
            messagebox.showerror("error", e)
    
    def view_text_to_doc(self):
        if self.view_file14 != "":
            startfile(self.view_file14)
            self.view_file14 = ""
        else:
            messagebox.askokcancel("warning", "Please  Convert the file before viewing",parent=self.fourth_window)

def main():
    root = Tk()
    root.iconbitmap('./res/hint.ico')
    obj = Design(root)


    root.mainloop()
if __name__ == "__main__": main()
